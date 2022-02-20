''' Generate DISARM sql databases

# Author: SJ Terp, Twitter @bodaceacat
# License: GPL-3

'''

import pandas as pd
import sqlite3 as sql
import os
from sqlalchemy import create_engine
from generate_DISARM_pages import Disarm



def generate_disarm_sql(dbasetype='sqlite'):
	''' Generate SQL
	Expected database types include 
		'sqlite': used to export database to other apps
		'postgresql_local': used in local instances of the DISARM explorer
		'heroku': used in Heroku-based instances of the DISARM explorer, although current 
		practice at DISARM is to post a dump of the postgresql database to it instead. 
	'''

	# Generate DISARM datasets
	disarm = Disarm()


	# Create connection to database
	if dbasetype == 'sqlite':
	    # Generate minimal sqlite database from the  variables
	    conn = sql.connect('../generated_files/DISARM_database.sqlite')
	elif dbasetype == 'postgresql_local':
	    conn = create_engine('postgresql://sara:@localhost:5432/disarmsite')

	    
	# Add table to database    
	def add_table(dataframe, tablename, columns):    
	    # Create sql-appropriate table from dataframe
	    colnames = ', '.join(['{} TEXT NOT NULL'.format(col) for col in columns])
	    newtable = dataframe[columns].copy().applymap(str)
	    newtable['id'] = range(1,len(newtable)+1)
	    
	    # send to database
	    if dbasetype == 'sqlite':
	        conn.execute("DROP TABLE IF EXISTS {}".format(tablename))
	        conn.execute('''CREATE TABLE {} (id INTEGER PRIMARY KEY AUTOINCREMENT, {});'''.format(tablename, colnames))
	        newtable.to_sql(tablename, conn, index=False, if_exists='append')
	        conn.commit()
	    elif dbasetype == 'postgresql_local':
	        newtable.to_sql(tablename, conn, index=False, if_exists='replace')
	    return newtable


	# Build a cross-table
	def object_tactics_techniques(objectcol, objecttable, crosstable):
	    # objects to techniques
	    ctech = crosstable.copy()
	    ctech = ctech[(ctech['technique_id'] != '') & (~ctech['technique_id'].str.startswith('TA'))]
	    ctech.rename(columns={'disarm_id':objectcol}, inplace=True)
	    ctech['summary'] = 'N/A'

	    # objects to tactics
	    ctact = crosstable[crosstable['technique_id'].str.startswith('TA')].copy()
	    ctact.rename(columns={'disarm_id':objectcol, 'technique_id': 'tactic_id'}, inplace=True)
	    ctact['main_tactic'] = 'N'
	    ctactmain = objecttable[['disarm_id', 'tactic_id']].copy()
	    ctactmain.rename(columns={'disarm_id':objectcol}, inplace=True)
	    ctactmain['main_tactic'] = 'Y'
	    ctact = pd.concat([ctact, ctactmain], ignore_index=True, sort=False)
	    ctact['summary'] = 'N/A'
	    return(ctech, ctact)

	#Load all the tables - Heroku needs them in correct order... 

	# -- frameworks --

	#newtable = add_table(disarm.df_actortypes, 'actor_type', ['disarm_id', 'sector_id', 'framework_id', 'name', 'summary'])
	newtable = add_table(disarm.df_counters, 'counter', ['disarm_id', 'tactic_id', 'metatechnique_id', 'name', 'summary'])
	newtable = add_table(disarm.df_detections, 'detection', ['disarm_id', 'tactic_id', 'name', 'summary'])
	newtable = add_table(disarm.df_frameworks, 'framework', ['disarm_id', 'name', 'summary'])
	newtable = add_table(disarm.df_metatechniques, 'metatechnique', ['disarm_id', 'name', 'summary'])
	newtable = add_table(disarm.df_phases, 'phase', ['disarm_id', 'name', 'rank', 'summary'])
	newtable = add_table(disarm.df_playbooks, 'playbook', ['disarm_id', 'object_id', 'name', 'summary'])
	newtable = add_table(disarm.df_resources, 'resource', ['disarm_id', 'name', 'summary', 'resource_type'])
	newtable = add_table(disarm.df_responsetypes, 'responsetype', ['disarm_id', 'name', 'summary'])
	#newtable = add_table(disarm.df_sector, 'sector', ['disarm_id', 'name', 'summary'])
	newtable = add_table(disarm.df_tactics, 'tactic', ['disarm_id', 'phase_id', 'name', 'rank', 'summary'])
	newtable = add_table(disarm.df_tasks, 'task', ['disarm_id', 'tactic_id', 'framework_id', 'name', 'summary'])
	newtable = add_table(disarm.df_techniques, 'technique', ['disarm_id', 'tactic_id', 'name', 'summary'])

	(ctech, ctact) = object_tactics_techniques('counter_id', disarm.df_counters, disarm.cross_counterid_techniqueid)
	newtable = add_table(ctech, 'counter_technique', ['counter_id', 'technique_id', 'summary'])
	newtable = add_table(ctact, 'counter_tactic', ['counter_id', 'tactic_id', 'main_tactic', 'summary'])

	(dtech, dtact) = object_tactics_techniques('detection_id', disarm.df_detections, disarm.cross_detectionid_techniqueid)
	newtable = add_table(dtech, 'detection_technique', ['detection_id', 'technique_id', 'summary'])
	newtable = add_table(dtact, 'detection_tactic', ['detection_id', 'tactic_id', 'main_tactic', 'summary'])

	# -- datasets --

	newtable = add_table(disarm.df_examples, 'example', ['disarm_id', 'object_id', 'name', 'summary'])

	# dataset
	# reference - create this from other tables. 
	# Also need incidentcounter etc - create from data
	newtable = add_table(disarm.df_externalgroups, 'externalgroup', ['disarm_id', 'name', 'url', 'summary', 
	                                                'sector', 'primary_role', 'secondary_role', 
	                                                'primary_subject', 'secondary_subject', 
	                                                'volunteers', 'region', 'country', 
	                                                'twitter_handle'])
	newtable = add_table(disarm.df_incidents, 'incident', ['disarm_id', 'name', 'summary', 
	                                                      'year_started', 'attributions_seen', 
	                                                      'found_in_country', 'objecttype'])
	newtable = add_table(disarm.df_tools, 'tool', ['disarm_id', 'name', 'summary',
	                                              'externalgroup', 'url', 'category', 
	                                              'disinformation_use', 'cogseccollab_use', 
	                                              'function', 'code_url', 'artifacts', 
	                                              'automation', 'platform', 'accessibility'])
	# incidenttechnique crosstable
	it = vars(disarm)['it'][['disarm_id', 'name', 'summary', 'disarm_id_incident', 'disarm_id_technique']].copy()
	it.rename(columns={'disarm_id_incident':'incident_id', 'disarm_id_technique': 'technique_id'}, inplace=True)
	newtable = add_table(it, 'incident_technique', ['disarm_id', 'name', 'summary', 
	                                                'incident_id', 'technique_id'])

	# Load in users table, and close connection
	if dbasetype == 'sqlite':
	    conn.execute("DROP TABLE IF EXISTS {}".format('users'))
	    conn.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL);''')
	    conn.close()
	else:
	    dfusers = pd.DataFrame([['test','testing']], columns=['username', 'password'])
	    usertable = add_table(dfusers, 'users', ['username', 'password'])

	    return



''' main, if we need it
'''
def main():
    generate_disarm_sql()


if __name__ == "__main__":
    main()

