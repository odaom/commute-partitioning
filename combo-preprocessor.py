'''
Commutes to Combo Preprocessor
Garrett Dash Nelson and Alasdair Rae, 2016

Read the paper: http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0166083

Generalized for arbitrary commute data sources.
'''

import csv
import time 
from os import remove, path


debug = False # set to True for debug throttling

startTime = time.time() 


sourceDatabaseFile = 'data-src/commutes.csv'			# Source file: CSV file with columns origin,destination,flow
nodesDatabaseFile = 'data-stage1/area_code_table.csv' 	# Output file: Lookup table matching area code to serialized ID used in Combo
pajekFile = 'data-stage1/commutes.net' 					# Output file: Pajek format for feeding into Combo 

if not path.isfile(sourceDatabaseFile):
	print('Failed: No source file in ./data-src/commutes.csv')
	exit()

if not path.isdir('data-stage1'):
	print('Failed: Requires an output directory data-stage1')
	exit()

# Look for a file ./data-src/subselection.txt
# If it's there, we're running an extract; create a set from FIPS in that file
if path.isfile('data-src/subselection.txt'):
	subSelection = True
	subSet = set(line.strip() for line in open('data-src/subselection.txt'))
else:
	subSelection = False


# Initialize a dict which will hold the area codes and their serialized ID for Combo
serializedAreaCodes = {}


# Function to lookup/add area code to serialization list
def getAreaCodeSerialId(area_code):

	if area_code not in serializedAreaCodes:

		serialId = len(serializedAreaCodes) + 1
		serializedAreaCodes[area_code] = serialId

		return serialId

	else:
		return serializedAreaCodes[area_code]


# Create a temporary file to hold the arcs (commutes)

arcTmp = open('arctmp.tmp','w+')
arcTmp.write('*Arcs\n')


# Begin building the list of arcs (commutes) here


i = 0 # rowcounter


reader = csv.reader(open(sourceDatabaseFile,'r'))
next(reader) # skip header

print('Beginning reading through commutes database')

for row in reader:

	# for debug throttling, limit to 1000 rows
	if debug:
		if i > 200: break
	i = i+1

	origin = row[0]
	dest = row[1]

	if subSelection:
		if origin not in subSet or dest not in subSet:
			continue
			
	origId = getAreaCodeSerialId(origin)
	destId = getAreaCodeSerialId(dest)

	strength = float(row[2])

	arcTmp.write(f' {origId} {destId} {strength}\n')

	if i % 10000 == 0:
		print(str(i) + ' rows processed, total time ' + str(time.time()-startTime))


# Create a temporary file to hold the vertices (the area codes)
verticesTmp = open('verttmp.tmp','w+')
verticesTmp.write(f'*Vertices {len(serializedAreaCodes)}\n')


# Initialize the lookup table CSV and give it a header row
nodesDatabase = open(nodesDatabaseFile,'w')
nodesDatabase.write('serial_id,area_code\n')


# Loop through all the vertices we created and write them into both verttmp.tmp and the lookup csv
for areaCode, serialId in sorted(serializedAreaCodes.items(), key=lambda item: item[1]):
	verticesTmp.write(' ' + str(serialId) + ' "' + areaCode + '"\n')
	nodesDatabase.write(str(serialId) + ',' + areaCode + '\n')


# Join the two temporary files to make a Pajek file
outFile = open(pajekFile, 'w')

verticesTmp.seek(0)
outFile.write(verticesTmp.read())

arcTmp.seek(0)
outFile.write(arcTmp.read())

remove('verttmp.tmp')
remove('arctmp.tmp')


print(f'done, total time {time.time()-startTime}')