import json
import csv
Relationships = csv.reader(open('in18trf.txt'))
List = [csv.reader(open('DEC_00_PL_PL002_with_ann.csv')), csv.reader(open('ACS_09_5YR_DP5YR5_with_ann.csv')), csv.reader(open('ACS_12_5YR_DP05_with_ann.csv'))]
Dicts = {}
Years = ['2000', '2009', '2012']
Indexes = {'2000': {'Pop': 3, 'Hisp': 4, 'NHW': 7, 'AA': 8, 'Asian': 10}, '2009': {'Pop': 3, 'Hisp': 263, 'NHW': 287,'AA': 291,'Asian':299}, '2012': {'Pop': 3, 'Hisp': 263, 'NHW': 287, 'AA': 291, 'Asian': 299}}
Indy = json.load(open('Indy.json'))
Dict2000 = {}
Dict2012 = {}
for i in range(3):
	for x in List[i]:
		if x[0] not in ['GEO.id', 'Id']:
			Dicts[x[1]+'-'+Years[i]] = {}
			for y in Indexes[Years[i]]:
				Dicts[x[1]+'-'+Years[i]][y] = float(x[Indexes[Years[i]][y]])
Tree = {}
def FindRoot(i):
	Root = Tree[i]
	while Root != Tree[Root]:
		Root = Tree[Root]
	return Root
for x in Relationships:
	if x[-6] != '0' and (x[3][:5] == '18097' or x[12][:5]=='18097'):
		Tuple = (x[3]+'-2000', x[12]+'-2012')
		if Tuple[0] not in Tree and Tuple[1] not in Tree:
			Tree[Tuple[0]] = max(Tuple)
			Tree[Tuple[1]] = max(Tuple)
		if Tuple[0] in Tree and Tuple[1] not in Tree:
			Tree[Tuple[1]] = Tuple[0]
		if Tuple[1] in Tree and Tuple[0] not in Tree:
			Tree[Tuple[0]] = Tuple[1]
		if Tuple[1] in Tree and Tuple[0] in Tree:
			MaxRoot = max(FindRoot(Tuple[1]), FindRoot(Tuple[0]))
			Tree[FindRoot(Tuple[1])] = MaxRoot
			Tree[FindRoot(Tuple[0])] = MaxRoot
Clusters = {}
for x in Dicts:
	if x[-4:]=='2009':
		try:
			Tree[x] = Tree[x[:-5]+'-2000']
		except:
			print x
for x in Tree:
	for z in Indexes[x[-4:]]:
		if FindRoot(x) not in Clusters:
			Clusters[FindRoot(x)] = {}
		if z+'-'+x[-4:] not in Clusters[FindRoot(x)]:
			Clusters[FindRoot(x)][z+'-'+x[-4:]] = 0.0
		Clusters[FindRoot(x)][z+'-'+x[-4:]] = Clusters[FindRoot(x)][z+'-'+x[-4:]]+Dicts[x][z]
for x in Indy['features']:
	try:
		for z in Clusters[FindRoot(x['properties']['GEOID10']+'-2012')]:
			x['properties'][z] = Clusters[FindRoot(x['properties']['GEOID10']+'-2012')][z]
	except:
		print x['properties']['GEOID10']
		for y in Indexes:
			for z in Indexes[y]:
				x['properties'][z+'-'+y] = 0.0
with open("IndyEdited.json", 'wb') as file:
	json.dump(Indy, file)
