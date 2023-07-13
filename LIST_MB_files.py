import os

basePath = 'F:/Users/joão/Documents/TRABALHO/Transfer'

for root, folders, files in os.walk(basePath):
	mayaFiles = [x for x in files if x.endswith('.ma')]

	for file in mayaFiles:
		filePath = os.path.abspath(os.path.join(root, file))

		print(filePath)