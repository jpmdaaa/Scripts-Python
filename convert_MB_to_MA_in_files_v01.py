import os, re

basepath = 'C:/Users/Lucas/Desktop/TAF_WORKFOLDER/assets/'

linksOnFile = set()


for root, folders, files in os.walk(basepath):

    mayaFiles = [x for x in files if x.endswith('.ma')]

    for fileName in mayaFiles:

        # print(f"\nVerificando o arquivo:\t\t{fileName}")

        filePath = os.path.abspath(f'{root}/{fileName}')
        print(f'Verificando arquivo:    {filePath} ...', end='\t')

        with open(filePath, 'r', encoding='latin-1') as file:
            content = file.read()

            # continue

            pattern1 = re.compile(r'-typ \"mayaBinary\" (\".*)\.mb\"')
            content, var1 =  re.subn(pattern1, r'-typ "mayaAscii" \1.ma"', content)

            pattern2 = re.compile(r'(file.*/.*)\.mb')
            content, var2 =  re.subn(pattern2, r'\1.ma', content)

            pattern3 = re.compile(r'([A-Za-z]:/.*?)\.mb')
            content, var3 =  re.subn(pattern3, r'\1.ma', content)

            pattern4 = re.compile(r'\"mayaBinary\"')
            content, var4 =  re.subn(pattern4, r'"mayaAscii"', content)

            # pattern5 = re.compile(r'(//\d{3}.*)\.mb"')
            # content, var5 =  re.subn(pattern5, r'\1.ma"', content)

            patternSearch = re.compile(r'([A-Za-z]:/.*?\..*)\"')
            for link in patternSearch.finditer(content):
                linksOnFile.add(link.group(1))

        # continue

        with open(filePath, 'w') as openFile:
            fileContent = openFile.write(content)

        WINDOWS_LINE_ENDING = b'\r\n'
        UNIX_LINE_ENDING = b'\n'

        with open(filePath, 'rb') as openFile:
            fileContent = openFile.read()

        # Windows -> Unix:
        fileContent = fileContent.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)

        with open(filePath, 'wb') as openFile:
            openFile.write(fileContent)
            print(f'\tok')


            # print(var1)
            # print(var2)
            # print(var3)
            # print(var4)
            # print(linksOnFile)

print('\n\n\n\n\n-----------------------\n\n')

for i in linksOnFile:
    print(i)
