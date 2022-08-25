
import pandas as pd
import os

MASTERDATA_DIR = '../DISARM_MASTER_DATA/'

    
frameworkfile = MASTERDATA_DIR + 'DISARM_FRAMEWORKS_MASTER.xlsx' 
datafile = MASTERDATA_DIR + 'DISARM_DATA_MASTER.xlsx'
#commentsfile = MASTERDATA_DIR + 'DISARM_COMMENTS_MASTER.csv'
        
# Get basic datasets from files
metadata = {}
for filein in [frameworkfile, datafile]:
    xlsx = pd.ExcelFile(filein)
    for sheetname in xlsx.sheet_names:
        print('{} sheet {}'.format(filein, sheetname))
        metadata[sheetname] = xlsx.parse(sheetname)
        metadata[sheetname].fillna('', inplace=True)
        metadata[sheetname].to_csv(MASTERDATA_DIR + sheetname + '.csv', index=False)

# Then use existing code to create the crosstable files. 
