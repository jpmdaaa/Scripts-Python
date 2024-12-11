import os
import shutil
import json
import sys
from workflow import get_shot_ranges_from_file_v02 as get_shot_ranges


workflow_path = os.path.abspath("./workflow").replace("\\","/")
project_path = os.path.abspath(".").replace("\\","/")

sys.path.append(workflow_path)
sys.path.append(project_path)


with open('./resources/paths.json', 'r') as file:
    pathsDict: dict[str, str] = json.load(file)


projectPath: str = pathsDict['projectFolder']
projectPath = projectPath.replace('\\', '/')

# Garante que o script esteja trabalhando na pasta onde o script se localiza
path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

get_shot_ranges.make_dict_from_files(dictPath='./resources/shots_dict.json', shotsFolderPath='./shots/')

# command = f'''mayabatch -proj "{projectPath}" -command "python(\\"from workflow import maya_caller\\") "'''
# p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# output, errors = p.communicate()
# print(output.decode('utf-8'))
# print(errors.decode('utf-8'))

os.system(f'''mayabatch -proj "{projectPath}" -command "python(\\"import sys;sys.path.append({workflow_path});sys.path.append({project_path});from workflow import maya_caller\\") "''')

print('AlembicGen concluido com sucesso')

