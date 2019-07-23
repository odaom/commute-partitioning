'''
QGIS CSV File Preprocessor
'''

from os import path
import pandas as pd

commutes_path = 'data-src/commutes.csv'
community_assignments_path = 'data-final/area_code_table_with_community_assignments.csv'
out_path = 'data-final/qgis-source.csv'

# Check if area code table is available
if not path.isfile(community_assignments_path):
    print(f'Failed: Could not find final area code table with community assignments at "{community_assignments_path}"')
    exit()

# Check if commute source file is available
if not path.isfile(commutes_path):
    print(f'Failed: Could not find commute source file at "{commutes_path}".')
    exit()

if not path.isdir('data-final'):
    print('Failed: Requires an output directory "data-final"')
    exit()


df_commutes = pd.read_csv(commutes_path)
df_assigned = pd.read_csv(community_assignments_path)

df_merged = pd.merge(left=df_commutes, right=df_assigned, how='left', left_on='destination', right_on='area_code').drop('area_code', axis=1)

df_merged.to_csv(out_path, index=False)