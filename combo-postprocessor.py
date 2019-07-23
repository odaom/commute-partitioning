'''
Commutes to Combo Postprocessor
Garrett Dash Nelson and Alasdair Rae, 2016

Read the paper: http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0166083

Generalized for arbitrary commute data sources.
'''

from os import path

# Check if Combo results are available
if not path.isfile('data-stage1/commutes_comm_comboC++.txt'):
	print('Failed: Could not find Combo output file at ./data-stage1/commutes_comm_comboC++.txt')
	exit()

if not path.isdir('data-final'):
	print('Failed: Requires an output directory data-final')
	exit()

with open('data-stage1/commutes_comm_comboC++.txt') as comboRawOutput:
	communities = comboRawOutput.readlines()

with open('data-final/area_code_table_with_community_assignments.csv','w') as outFile:

	with open('data-stage1/area_code_table.csv') as areaCodeRawInput:

		next(areaCodeRawInput) # skip header

		outFile.write('serial_id,area_code,community\n')

		i = 0
		for line in areaCodeRawInput:
			outFile.write(line.rstrip() + ',' + str(communities[i]))
			i += 1
