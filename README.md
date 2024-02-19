# DISARM Disinformation TTP (Tactics, Techniques and Procedures) Framework

DISARM is a framework designed for describing and understanding disinformation incidents.  DISARM is part of work on adapting information security (infosec) practices to help track and counter disinformation and other information harms, and is designed to fit existing infosec practices and tools.

DISARM's style is based on the [MITRE ATT&amp;CK framework](https://github.com/mitre-attack/attack-website/). STIX templates for DISARM objects are available in the [DISARM_CTI repo](https://github.com/DISARMFoundation/DISARM_cti) - these make it easy for DISARM data to be passed between ISAOs and similar bodies using standards like TAXII.

## What's in this folder

DISARM DOCUMENTATION:
* [DISARM_DOCUMENTATION](DISARM_DOCUMENTATION): DISARM user guides, design guides, and more detailed TTP documentation.
* [DISARM_HISTORY](DISARM_DOCUMENTATION/DISARM_HISTORY): earlier models and reports.

DISARM FRAMEWORKS:
* [DISARM Red Team Framework](generated_pages/disarm_red_framework.md) - Disinformation creator TTPs, listed by tactic stage. This is the classic "DISARM Framework" that's bundled with MISP.  The [clickable](generated_files/disarm_red_framework_clickable.html) version is for rapidly creating lists of TTPs.
* [DISARM Blue Team Framework](generated_pages/disarm_blue_framework.md) - Disinformation responder TTPs, listed by tactic stage. These are countermeasures, listed by the earliest tactic stages they're likely to be used in.
* The set of dsinformation responder TTPs in the DISARM Blue Team Framework was derived in 2019 by volunteers in a workshop.  It includes TTPs seen in countries with different ethical values (such as “censorship”, an action observed in countries with authoritarian governments). We will continue to make this “Blue” workshop output available as we develop an alternative based on democratic values and ethical principles, but we advise caution to anyone using it and have created a Companion Guide for those users (see under DISARM DOCUMENTATION). Of course, every user must consider for themselves what actions would be ethical, relevant, proportionate, and appropriate, given the unique legal, cultural, and normative context in which they are operating.

DISARM OBJECTS: all the entities used to create the Red Team and Blue Team frameworks:
* [Phases](generated_pages/phases_index.md): higher-level groupings of tactics, created so we could check we didn't miss anything
* [Tactics](generated_pages/tactics_index.md): stages that someone running a misinformation incident is likely to use
* [Techniques](generated_pages/techniques_index.md): activities that might be seen at each stage
* [Tasks](generated_pages/tasks_index.md): things that need to be done at each stage.  In Pablospeak, tasks are things you do, techniques are how you do them.
* [Counters](generated_pages/counters_index.md): countermeasures to DISARM TTPs.  
* [Actor Types](generated_pages/actortypes_index.md): resources needed to run countermeasures
* [Response types](generated_pages/responsetype_index.md): the course-of-action categories we used to create counters
* [Metatechniques](generated_pages/metatechniques_index.md): a higher-level grouping for countermeasures
* [Incidents](generated_pages/incidents_index.md): incident descriptions used to create the DISARM frameworks

There's a directory for each of these, containing a datasheet for each individual entity (e.g. [technique T0046 Search Engine Optimization](generated_pages/techniques/T0046.md)).  There's also a directory [generated_files](generated_files) containing any files (CSVs, sqlite etc) we generate from the above tables.

## Updating DISARM

Major changes: Any major changes to DISARM models are agreed on by the DISARM Foundation.

Minor changes: We love any and all suggestions for improvements, comments and offers of help - reach out to us using [this google form](https://docs.google.com/forms/d/e/1FAIpQLSdZuyKFp1UZzk6qUE4IN1O14HaJ-F4TH9thxR3hrRU-Mu7QUQ/viewform). (We're also going back through earlier issues lists: [AMITT issues list](https://github.com//DISARM/issues) and [Misinfosec issues list](https://github.com/misinfosecproject/DISARM_framework/issues))

Using your own datasets: DISARM is open source.  If you want to do your own thing with DISARM data, these will help:
* all the master data for DISARM is in directory [DISARM_MASTER_DATA](DISARM_MASTER_DATA). Look for the [DISARM_FRAMEWORKS_MASTER.xlsx](DISARM_MASTER_DATA/DISARM_FRAMEWORKS_MASTER.xlsx) spreadsheet. This contains disinformation creators' tactics, techniques, tasks, phases, and counters.

* The [DISARM TTP Guide](https://docs.google.com/document/d/1Kc0O7owFyGiYs8N8wSq17gRUPEDQsD5lLUL_3KGCgRE/edit#) has more detailed information on each technique.

* The code to create all the HTML datasheets is in directory [CODE](CODE): you'll need generate_DISARM_pages.py and all the template files.

If you have your own version of this repository and update DISARM_FRAMEWORKS_MASTER.xlsx, typing "python generate_DISARM_pages.py" will update all the files above from it.  If you want to update the DISARM github file, DISARM databases, and DISARM STIX bundle at the same time, run file generate_DISARM_pages.ipynb from Jupyter. 


## Who's Responsible for DISARM (and a little history)

* Now: **[DISARM Foundation](https://www.disarm.foundation/)** maintains and updates the DISARM family of models: DISARM-STIX, the DISARM Red framework (of disinformation creation), and the DISARM Blue framework (of disinformation countermeasures and mitigations).  

* In 2022, **MITRE, FIU, and CogSecCollab teams** worked to merge the AMITT and SPICE framework models together to create the DISARM frameworks, led by SJ, Pablo, Mark, and Jon Brewer (who keeps us all organized).  This team created the DISARM FOUNDATION. 

* 2020? **[MITRE](https://www.mitre.org/) and [FIU: Florida International University](https://www.fiu.edu/)** forked the AMITT RED model to create the SPICE framework, led by Mark Finlayson at FIU. 

* 2020-2022: **[CogSecCollab](http://cogsec-collab.org/)** maintained and updated the original AMITT models.  CogSecCollab is the nonprofit that spun out of MisinfosecWG. CogSecCollab used AMITT in the CTI League's Covid19 responses, and tested it in trials with NATO, the EU, and several other countries' disinformation units. SJ Terp and Pablo Breuer held the design authority for the AMITT models.

* 2018-2020: **[MisinfosecWG](https://github.com/credcoalition/community-site/wiki/Working-Groups)**, aka the Credibility Coalition's Misinfosec working group created the original DISARM frameworks. The Credibility Coalition is a natural fit for the standards part of this (because in 2017 every group - media, military, advertising, public etc - had a different set of words for disinformation components), and since SJ was there when the Credibility Coalition was created, they were a natural place to do this work.  The Red Framework was started in December 2018, refined in a Credibility Coalition Misinfosec seminar, and argued into shape by SJ and Pablo at SOFTWERX over an unreasonable amount of coffee; the Blue Framework was started as a collection of potential disinformation countermeasures, at a Coalition Misinfosec seminar in November 2019. This work was led jointly by SJ and Christopher Walker ("Walker") from Marvelous.AI, later joined by John Grey from MentionMapp, but it was really a CredCo community effort, with contributions from many people and places, including Roger Johnston, who joined after we presented at ATT&CKcon, and started building many of the tools and connections to systems like STIX and MISP.  

* 2017-2018: SJ Terp starts working on adapting information security tools, processes, and procedures for disinformation use.  She links up with JJ Snow, Pablo Breuer, the usual collection of infosec geeks, and the SOFWERX team to work on characterising and countering hybrid incidents (cybersecurity plus disinformation, noting that information operations have always included this).  

* **Everyone who contributes to DISARM** (and there are many of you). Thank you to everyone who contributes to DISARM, and has contributed to DISARM over the years.

* **You**. Thank you for being here.

DISARM is licensed under [CC-BY-4.0](LICENSE.md)
