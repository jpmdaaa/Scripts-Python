import os
import json
import requests
from typing import Any

try:
    from ftrack_api import Session
except ImportError:
    print("Foi detectado que a API do ftrack não está instalada em seu sistema. Tentando instalar:")
    os.system("python -m pip install ftrack-python-api")
    from ftrack_api import Session



def get_ftrack_session():

    credentialsFolder: str = os.path.abspath('./resources/credentials')
    selectedCredential: str = 'credentials-admin.json'
    credentialPath: str = os.path.join(credentialsFolder, selectedCredential)

    # puxando a credencial e iniciando a sessão
    with open(credentialPath, 'r') as f:
        data = json.load(f)

    print("Fazendo login no ftrack...")
    session = Session(
        server_url ="https://hype.ftrackapp.com",
        api_key = data["key"],
        api_user = data["user"]
    )

    return session



def download_video_assets(serverLocation, fileName, assetToDownload, downloadFolder, videoFormats):

    componentToDownload = [
        component for component in assetToDownload['components']
        if component['file_type'].lower().endswith(videoFormats)
        and 'ftrackreview' not in component['name']
        ]

    for component in componentToDownload:
        link = serverLocation.get_url(component)

        extension = component['file_type']
        name = fileName + extension
        filepath = os.path.join(downloadFolder, name)

        content = requests.get(link)

        if content:
            write_content_to_file(filepath, content)



def write_content_to_file(filepath, downloadContent):

    if not os.path.exists( os.path.dirname(filepath) ):
        os.makedirs( os.path.dirname(filepath) )

    with open(filepath, 'wb') as file:
        file.write(downloadContent.content)



def get_tasks_ids_from_search(projectID: str, projectName: str = '', parentName: str = '', taskType: str = '', taskName: str = '', session: Session = ...):

    if not session:
        print("Por favor faça login no ftrack antes de acessar essa função.")
        return

    filtersDict = {
        'project_id is': projectID,
        'projectName is': projectName,
        'parent.name is': parentName,
        'type.name is': taskType,
        'name is': taskName,
    }

    filters = [f'{key} "{filtersDict[key]}"' for key in filtersDict if filtersDict[key] != '']
    filtersQuery = ' and '.join(filters)

    tasks = session.query(
        "select id from Task where " + filtersQuery
        ).all()

    ids = []

    for task in tasks:
        ids.append(task['id'])

    return ids



def download_lastest_asset_from_task(taskID, session: Session):

    assetToDownload = session.query(
    f'''select version, components, asset.name, asset.id
        from AssetVersion
        where task_id is {taskID}
        order by date descending
        ''').first()

    task: Any = session.get("Task", taskID)

    name = task['name']
    name = name.replace('/', '_')
    name = name.replace('\\', '_')

    if assetToDownload:
        download_video_assets(serverLocation, fileName=name, assetToDownload=assetToDownload, downloadFolder='./downloads/', videoFormats=VIDEO_FORMATS)

    else:
        print(f"AVISO: o arquivo [{task['name']}] cujo parent é [{task['parent']['name']}] não possui componentes")




if __name__ == "__main__":


    session: Session = get_ftrack_session()
    serverLocation = session.query('Location where name is "ftrack.server"').one()


    # ------------------------   parâmetros   ------------------------
    VIDEO_FORMATS: tuple = ('.mov', '.mp4', '.avi')
    taskTypes: list = ['Layout', 'Animation', 'Animatic']
    shotName: str = 'VMB102_SH0030'
    projectCode: str = 'sr010_vamos_brincar'
    # ------------------------   parâmetros   ------------------------


    projectIdQuery: Any = session.query(
        f'select id from Project where name is "{projectCode}"'
    ).first()

    projectId = projectIdQuery['id']

    tasksToDownload = []

    for _type in taskTypes:
        tasks = get_tasks_ids_from_search(projectID=projectId, parentName=shotName, taskType=_type, session=session)

        if tasks:
            tasksToDownload.extend(tasks)

    if tasksToDownload:
        for taskID in tasksToDownload:
            download_lastest_asset_from_task(taskID, session)


