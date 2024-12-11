import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

try:
    from ftrack_api import Session
except ImportError:
    print("Foi detectado que a API do ftrack não está instalada em seu sistema. Tentando instalar:")
    os.system("python -m pip install ftrack-python-api")
    from ftrack_api import Session

try:
    import requests
except ImportError:
    print("Foi detectado que o módulo 'requests' não está instalada em seu sistema. Tentando instalar:")
    os.system("python -m pip install requests")
    import requests

from resources.typeHints import *


class window():

    def __init__(self) -> None:

        self.window = tk.Tk()
        self.window.title('ftrack Video Downloader')
        self.window.geometry('400x500')

        self.credential: str = ''
        self.cretendialPath: str = ''
        self.contentType: (str) = ''
        self.selectedFolder: str = ''
        self.selectedCredentialLabel = tk.StringVar()
        self.selectedProjectLabel = tk.StringVar()
        self.selectedContentLabel = tk.StringVar()
        self.selectedShotGroupTypeLabel = tk.StringVar()


        # Garante que o script esteja trabalhando na pasta onde o script se localiza
        try:
            scriptPath: str = os.path.dirname(os.path.realpath(__file__))
            os.chdir(scriptPath)
        except NameError:
            pass


        # separa o nome das credenciais disponíveis
        self.availableCredentials: (dict[str, dict[str, str]]) = self.list_available_credentials()
        self.credentialsName: list[str] = []
        self.availableProjects: list[str] = []
        self.availableContents: list[str] = []

        if self.availableCredentials == None:
            messagebox.showwarning("Aviso!", "Nenhuma credencial disponível. Verifique se existe uma pasta junto do script "
                "chamada 'resources', e dentro dela existe uma pasta de 'credentials' com alguma credencial dentro.\n"
                "Qualquer dúvida, favor solicitar uma credencial ao setor de Produção ou de Pipeline")

        else:
            for cred in self.availableCredentials:
                x: str = self.availableCredentials[cred]['display_name']
                self.credentialsName.append(x)

        self.main_Window = ttk.Frame(self.window)

        self.main_topRow = ttk.Frame(self.main_Window)
        self.main_body = ttk.Frame(self.main_Window)
        self.main_bottomRow = ttk.Frame(self.main_Window, style='test.TFrame')

        self.config_Window = ttk.Frame(self.window)

        self.windows: list[ttk.Frame] = [self.main_Window, self.config_Window,]



        # # GERAÇÃO DA INTERFACE - TELA INICIAL -----------------------------------
        self.credentialsLabel = ttk.Label(self.main_topRow, text='Credencial',)
        self.credentialsList = ttk.OptionMenu(self.main_topRow, self.selectedCredentialLabel, self.credentialsName[0], *self.credentialsName, command=self.on_credential_changed, style='credential.TMenubutton')
        self.credentialsList.pack(side='right')
        self.credentialsLabel.pack(side='right')


        self.main_body.grid_columnconfigure(0, minsize=100)
        self.main_body.grid_columnconfigure(1, minsize=200)

        ttk.Label(self.main_body, text='Primeiro, escolha o projeto e a sequência ou episódio para baixar.', wraplength=350).grid(column=0, row=0, columnspan=2)

        self.projectsListLabel = ttk.Label(self.main_body, text='Projeto')
        self.projectsList = ttk.OptionMenu(self.main_body, self.selectedProjectLabel, 'Escolha um projeto', *self.availableProjects, command=self.on_project_changed, direction='right', style='main.TMenubutton')
        self.projectsListLabel.grid(row=2, column=0, sticky='e')
        self.projectsList.grid(row=2, column=1, ipadx=10, ipady=5, sticky='w', pady=5)

        self.contentListLabel = ttk.Label(self.main_body, text='Conteúdo')
        self.contentList = ttk.OptionMenu(self.main_body, self.selectedContentLabel, 'Escolha um conteúdo', *self.availableContents, command=lambda selection: self.on_content_changed(selection), direction='right', style='main.TMenubutton')
        self.contentListLabel.grid(row=3, column=0, sticky='e')
        self.contentList.grid(row=3, column=1, ipadx=10, ipady=5, sticky='w', pady=5)

        ttk.Separator(self.main_body, orient='horizontal').grid(row=5, column=0, columnspan=2, sticky='ew', pady=10)

        self.selectedFolderLabel = ttk.Label(self.main_body, text='( Nenhuma pasta selecionada )')
        self.selectFolderButton = ttk.Button(self.main_body, text="Escolher local", command=self.select_folder)
        self.selectFolderButton.grid(row=7, column=0, columnspan=2, ipady=10, ipadx=10)
        self.selectedFolderLabel.grid(row=8, column=0, columnspan=2, ipady=10)

        self.next_configButton = ttk.Button(self.main_bottomRow, text='Próximo', command=lambda: self.go_to(self.config_Window))
        self.next_configButton.pack(side='bottom', pady=15, padx=10, ipadx=20, ipady=5, expand=True, fill='both')


        self.main_topRow.pack(anchor='e', padx=10, side='top')
        ttk.Separator(self.main_Window, orient='horizontal').pack(fill='x', anchor='w', pady=5)
        self.main_bottomRow.pack(side='bottom')
        ttk.Separator(self.main_Window, orient='horizontal').pack(fill='x', anchor='w', side='bottom',)
        self.main_body.pack(fill='both', side='bottom', expand=True)

        self.main_Window.pack(fill='y', expand=True)



        # # GERAÇÃO DA INTERFACE - TELA DE CONFIGURAÇÕES -----------------------------------

        ## Configurações de download -----------------------------------
        downloadTypeFrame = ttk.LabelFrame(self.config_Window, text='O que você quer que seja baixado?')

        self.downloadType_var = tk.StringVar()
        self.downloadType_var.set('type_dependent')

        ttk.Radiobutton(downloadTypeFrame, text='Os uploads mais recentes de cada tipo de task',
                        variable=self.downloadType_var, value='type_dependent',
                        command = lambda: self.checkbox_set_state('enabled', CB_dict=self.cb_shotsDict),
                        ).pack(anchor='w')
        ttk.Radiobutton(downloadTypeFrame, text='Só o único upload mais recente do shot',
                        variable=self.downloadType_var, value='only_most_recent',
                        command = lambda: self.checkbox_set_state('disabled', CB_dict=self.cb_shotsDict),
                        ).pack(anchor='w')

        downloadTypeFrame.pack(pady=10, anchor='w', fill='x')


        ## Escolha de tipos de task pra baixar -----------------------------------
        self.taskTypeFrame = ttk.LabelFrame(self.config_Window, text='Tipos de tarefas')
        self.taskTypeFrame.pack(pady=10, anchor='w', fill='x')

        shotButtonsFrame = ttk.Frame(self.taskTypeFrame)
        shotButtonsFrame.grid(row=100, column=0)

        ttk.Button(shotButtonsFrame, text='Selecionar tudo',
                    command = lambda: self.checkbox_set_all(True, CB_dict=self.cb_shotsDict)
                    ).grid(column=0, row=101)
        ttk.Button(shotButtonsFrame, text='Deselecionar tudo',
                    command = lambda: self.checkbox_set_all(False, CB_dict=self.cb_shotsDict)
                    ).grid(column=1, row=101)
        # ttk.Button(shotButtonsFrame, text='Get values',
        #             command= lambda: self.checkbox_get_values(CB_dict=self.cb_shotsDict)
        #             ).grid(column=0, row=102, columnspan=2)


        otherOptionsFrame = ttk.LabelFrame(self.config_Window, text='Configurações dos vídeos baixados')
        otherOptionsFrame.pack(pady=10, anchor='w', fill='x')

        self.is_groupByShot = tk.BooleanVar()
        self.is_groupByShot.set(True)

        self.is_replaceUploadName = tk.BooleanVar()
        self.is_replaceUploadName.set(True)

        self.is_removeVersionFromName = tk.BooleanVar()
        self.is_removeVersionFromName.set(True)

        ttk.Checkbutton(otherOptionsFrame, text='Cada shot vai ter sua própria pasta', variable=self.is_groupByShot).pack(anchor='w')
        ttk.Checkbutton(otherOptionsFrame, text='Substituir os nomes pelo padrão da Hype', variable=self.is_replaceUploadName).pack(anchor='w')
        ttk.Checkbutton(otherOptionsFrame, text='Remover a versão do nome do arquivo', variable=self.is_removeVersionFromName).pack(anchor='w')


        self.config_bottomRow = ttk.Frame(self.config_Window)
        self.config_bottomRow.pack(side='bottom')

        ttk.Separator(self.config_Window, orient='horizontal').pack(fill='x', anchor='w', side='bottom')
        ttk.Button(self.config_bottomRow, text='Voltar', command=lambda: self.go_to(self.main_Window)).grid(row=0, column=0, pady=15, padx=10, ipadx=20, ipady=5)
        ttk.Button(self.config_bottomRow, text='Baixar!', width=20, command=self.prepare_to_download).grid(row=0, column=1, pady=15, padx=10, ipadx=20, ipady=5)



        # Personalização de tema pra Debug
        style = ttk.Style()
        # style.configure('TLabel', background='#b5ffbb')
        style.configure('TMenubutton', background='#cad4df')
        style.configure('main.TMenubutton', width=30)

        # style.configure('test.TFrame', background='#222222')

        # self.bottomRow.configure(style='test.TFrame')
        # style.configure('credential.TMenubutton', width=15)


    # # MÉTODOS DA INTERFACE -------------------------------------------------------

    def populate_task_types_cb(self) -> None:
        if self.taskTypes:

            try:
                if self.cb_shotsDict:
                    for checkbox in self.cb_shotsDict.keys():
                        self.cb_shotsDict[checkbox]['obj'].destroy()
            except AttributeError:
                pass

            self.cb_shotsDict = {}

            for index, task in enumerate(self.taskTypes):
                self.cb_shotsDict[task] = {
                    'check': tk.BooleanVar(),
                    'name': task,
                    'state': 'enabled',
                }
                self.cb_shotsDict[task]['obj'] = ttk.Checkbutton(self.taskTypeFrame, text=self.cb_shotsDict[task]['name'],
                                                                 variable=self.cb_shotsDict[task]['check'],
                                                                 state=self.cb_shotsDict[task]['state'],
                                                                 command=lambda: self.checkbox_get_values(CB_dict=self.cb_shotsDict))
                self.cb_shotsDict[task]['obj'].grid(row=index, sticky='w')

        else:
            try:
                if self.cb_shotsDict:
                    for checkbox in self.cb_shotsDict.keys():
                        self.cb_shotsDict[checkbox]['obj'].destroy()
            except AttributeError:
                pass

    def checkbox_set_all(self, value, CB_dict) -> None:
        for checkbox in CB_dict.keys():
            CB_dict[checkbox]['check'].set(value)


    def checkbox_set_state(self, CB_state, CB_dict) -> None:
        for checkbox in CB_dict.keys():
            CB_dict[checkbox]['state'] = CB_state
            CB_dict[checkbox]['obj'].configure(state=CB_state)


    def checkbox_get_values(self, CB_dict) -> None:
        self.selectedTaskTypes = []

        for checkbox in CB_dict.keys():
            # print(f"{CB_dict[checkbox]['name']}: \t {CB_dict[checkbox]['check'].get()} \t {CB_dict[checkbox]['state']}")
            if CB_dict[checkbox]['check'].get() is True:
                self.selectedTaskTypes.append(CB_dict[checkbox]['name'])

        # print(self.selectedTaskTypes)


    def get_current_credential_selected(self, selection) -> (dict[str, str]):

        if self.availableCredentials == None:
            messagebox.showwarning("Aviso!", "Nenhuma credencial selecionada. Verifique se existe uma pasta junto do script "\
                "chamada 'resources', e dentro dela existe uma pasta de 'credentials' com alguma credencial dentro.")
            return

        for key in self.availableCredentials:
            for item in self.availableCredentials[key]:
                if self.availableCredentials[key]['display_name'] == selection:
                    selectedItem: dict[str, str] = self.availableCredentials[key]
                    return selectedItem


    def get_current_project_selected(self, selection) -> (dict[str, str]):
        for key in self.projectsDict:
            for item in self.projectsDict[key]:
                if self.projectsDict[key]['name'] == selection:
                    selectedItem: dict[str, str] = self.projectsDict[key]
                    return selectedItem

    def on_content_changed(self, selection) -> None:
        self.selectedContent: str = selection
        self.taskTypes: (set[str]) = set()
        print(self.selectedContent)

        try:
            shotQuery = self.session.query(
                f'select name, descendants.type.name from Shot where project.full_name is "{self.selectedProjectName}" '
                f'and parent.name is {self.selectedContent}'
            ).all()
            if shotQuery:
                shots: list[str] = [x['name'] for x in shotQuery]
                taskTypes: set[str] = set()
                for item in shotQuery:
                    for child in item['descendants']:
                        try:
                            taskTypes.add(child['type']['name'])
                        except TypeError:
                            messagebox.showwarning("Atenção", f"Atenção! o Shot {item['name']} não possui tasks. O script vai pular esse shot.")
                print(f'Foram encontrados {len(taskTypes)} tipos de tarefa.')

                self.taskTypes: (set[str] ) = taskTypes
                self.shots: list[str] = shots
                self.shots.sort()

            else:
                self.taskTypes = None
                messagebox.showwarning("Atenção", f"Atenção! Este {self.contentType} não possui shots ou está fora do padrão necessário. Os shots precisam estar dentro dos {self.contentType}s no ftrack, sem nenhuma pasta intermediária.")

        except ServerError:
            messagebox.showwarning(
                "Atenção", "O episódio ou a sequência selecionada não possui nenhum shot, ou possui um shot sem nenhuma task dentro.\n"
                "Atualmente este programa consegue baixar apenas os uploads feitos diretamente nos shots.\n\n"
                "Se você não esperava encontrar este aviso neste momento, entre em contato com a coordenação ou o setor de pipeline para ver se é possível fazer algo sobre isso")


        self.populate_task_types_cb()
        self.validate_next_button()


    def list_available_credentials(self) -> (dict[str, dict[str, str]]):
        credentialsDict: dict[str, dict[str, str]] = {}

        if os.path.exists('./resources/credentials/'):
            credentialsPath: str = os.path.join(os.path.abspath('.'), 'resources/credentials/')
            credentialsPath: str = credentialsPath.replace('\\', '/')
            credentialsList: list[str] = [x for x in os.listdir(credentialsPath) if x.startswith('credentials-')]

            self.cretendialPath = credentialsPath

            for credential in credentialsList:
                credentialsDict[credential] = {
                    'file_name': credential,
                    'file_path': credentialsPath + credential,
                    'display_name': str(credential).replace('_', ' ').removeprefix('credentials-').removesuffix('.json'),
                    }

        if credentialsDict:
            return credentialsDict

        else:
            print('ERRO: Não foi encontrada a pasta de credenciais')


    def on_credential_changed(self, selection) -> None:

        self.projectsList.set_menu('--- carregando projetos ---', [])
        self.projectsList.update()


        selectedCredential: (dict[str, str]) = self.get_current_credential_selected(selection)

        if selectedCredential == None:
            messagebox.showwarning("Aviso!", "Nenhuma credencial selecionada.")
            return

        print("Credencial selecionada: " + selectedCredential['display_name'])

        with open(self.cretendialPath + selectedCredential['file_name'], 'r') as f:
            data = json.load(f)

        self.session = Session(
            server_url ="https://hype.ftrackapp.com",
            api_key = data["key"],
            api_user = data["user"]
        )

        self.serverLocation: Location = self.session.query(
                'Location where name is "ftrack.server"').one()

        self.update_project_list()

        print(f'Foram encontrados {len(self.availableProjects)} projetos.')

        if len(self.availableProjects) == 0:
            messagebox.showwarning("Atenção","Nenhum projeto foi encontrado!")

        self.validate_next_button()



    def on_project_changed(self, selection) -> None:

        self.selectedProject: (dict[str, str]) = self.get_current_project_selected(selection)

        if self.selectedProject == None:
            messagebox.showwarning("Aviso", "Nenhum projeto selecionado!")
            return

        self.selectedProjectName: str = self.selectedProject['name']

        print(f'Projeto selecionado: {self.selectedProject["name"]}')

        self.projectType: str = str(self.selectedProject['type'])

        self.contentType: (str ) = self.get_content_type(self.projectType)
        if self.contentType == None:
            messagebox.showwarning("Aviso", "Nenhum tipo de conteúdo selecionado!")
            return
        # print(f'Project Type: {self.projectType},\t Content type: {self.contentType}')

        if self.contentType == 'Episode' or self.contentType == 'Sequence':
            contentQuery: list[QueryResult] = self.session.query(
                f'''select name from {self.contentType} \
                    where project.full_name is "{self.selectedProjectName}"'''
            ).all()

            if contentQuery:
                self.contentList.configure(state='normal')
                contentList: list[str] = list({item['name'] for item in contentQuery})
                contentList.sort()
                self.availableContents = contentList

                print(f'Foram encontrados {len(self.availableContents)} {self.contentType}s.')

                self.contentList.set_menu(*self.availableContents)
                self.contentListLabel.configure(text=f'{self.contentType}:')

            else:
                messagebox.showwarning("Atenção", f"Nenhum(a) {self.contentType} foi encontrado!\nSe o projeto for longa, verifique se ele possui sequências.\nSe for série, precisa ter episódios.")
                self.contentList.configure(state='disabled')
                self.contentList.set_menu(f'Projeto é {self.projectType.capitalize()} mas\nnão tem {self.contentType}s')

        elif self.contentType == 'Shot':
            self.contentList.configure(state='disabled')
            self.contentList.set_menu('Shots (todos os shots)')

        else:
            self.contentList.configure(state='disabled')
            self.contentList.set_menu(f'Projeto precisa ser Curta, Longa\nou Série, mas é {self.projectType.capitalize()}')

        self.validate_next_button()



    def get_content_type(self, projectType: str) -> (str):
        return 'Episode'
        '''match projectType:
            case 'series':
                return 'Episode'
            case 'feature':
                return 'Sequence'
            case 'short':
                return 'Shot'
            case _:
                return None'''



    def get_project_type(self, code: str) -> str:
        if code.startswith('sr'):
            return 'series'
        if code.startswith('fm'):
            return 'feature'
        if code.startswith('sm'):
            return 'short'
        if code.startswith('gm'):
            return 'game'
        if code.startswith('ot'):
            return 'other'

        return f'unknown -> {code}'


    def update_project_list(self) -> None:

        projects: list[QueryResult] = self.session.query(
            'select full_name, name, id, custom_attributes from Project where status is "Active" '
            ).all()

        availableProjectsDict: dict[str, dict[str,str] ] = {}
        availableProjectNamesList: list[str] = []

        for result in projects:
            project: dict[str, str] = {
                'name': result['full_name'],
                'code': result['name'],
                'initials': result['custom_attributes']['initials'],
                'id': result['id'],
                'type': self.get_project_type(result['name']),
            }
            availableProjectsDict[project['name']] = project
            availableProjectNamesList.append(project['name'])

        self.availableProjects: list[str] = sorted(availableProjectNamesList)
        self.projectsDict: dict[str, dict[str, str]] = availableProjectsDict

        self.projectsList.set_menu('Selecione um projeto', *self.availableProjects)



    def prepare_to_download(self) -> None:

        self.currentShot: str = ''
        self.currentTaskType: str = ''

        if self.selectedProject == None:
            messagebox.showwarning("Aviso!", "Nenhum projeto selecionado.")
            return

        if self.downloadType_var.get() == 'only_most_recent':
            for shot in self.shots:
                self.currentShot = shot

                assetQuery: (QueryResult) = self.session.query(
                        f'''select version, components, asset.name, asset.id from AssetVersion\
                        where task.parent.name is "{self.currentShot}"\
                        and project_id is "{self.selectedProject['id']}"\
                        order by date descending'''
                        ).first()

                if not assetQuery:
                    print(f'O shot {self.currentShot} não possui uploads ainda.')
                    continue

                self.download_asset(assetQuery)

            print('Todos os arquivos foram baixados')


        elif self.downloadType_var.get() == 'type_dependent':
            for shot in self.shots:
                for taskType in self.selectedTaskTypes:
                    self.currentShot = shot
                    self.currentTaskType = taskType

                    assetQuery: (QueryResult ) = self.session.query(
                        f'''select version, components, asset.name, asset.id from AssetVersion\
                        where task.type.name is "{self.currentTaskType}"\
                        and task.parent.name is "{self.currentShot}"\
                        and project_id is "{self.selectedProject['id']}"\
                        order by date descending'''
                        ).first()

                    if not assetQuery:
                        print(f'O shot {self.currentShot} não possui tarefas do tipo {self.currentTaskType}')
                        continue

                    self.download_asset(assetQuery)
                    # print(assetQuery['asset']['name'])

            print('Todos os arquivos foram baixados')

        else:
            raise Exception('ERRO: algum erro com o checklist de tipo de download :(')



    def download_asset(self, assetToDownload) -> None:

        self.currentUplodadName: str = assetToDownload['asset']['name']
        self.currentUploadVersion: str = assetToDownload['version']

        print(f"Baixando o vídeo {self.currentUplodadName}...")

        for component in assetToDownload['components']:
            if any((component['file_type'] == '.mov',
                    component['file_type'] == '.mp4',
                    component['file_type'] == '.avi'
                    )) and 'ftrackreview' not in component['name']:
                link: str = self.serverLocation.get_url(component)

                self.currentFileExtension: str = component['file_type']

                downloadContent = requests.get(link)

                fileFolder: str = self.get_folder_name()
                fileName: (str) = self.get_file_name()

                if fileName == None:
                    messagebox.showwarning("Aviso", "Nenhum arquivo selecionado.")
                    return

                if not os.path.exists(fileFolder):
                    os.makedirs(fileFolder)

                with open(os.path.join(fileFolder, fileName), 'wb') as file:
                    file.write(downloadContent.content)
                    print(f'Vídeo baixado em:  {os.path.abspath(os.path.join(fileFolder, fileName))}')


    def get_file_name(self) -> (str):

        if self.is_replaceUploadName.get() == False:
            name: str = self.currentUplodadName + self.currentFileExtension
            return name

        if self.selectedProject == None:
            messagebox.showwarning("Aviso", "Nenhum projeto selecionado.")
            return

        projectInitial: str = self.selectedProject['initials']
        content: str = self.selectedContent

        if projectInitial.lower() in content.lower():
            projectInitial: str = ''
        else:
            projectInitial: str = self.selectedProject['initials']

        shot: str = self.currentShot

        if content.lower() in shot.lower():
            content: str = ''
        else:
            content: str = "_" + self.selectedContent

        if self.is_removeVersionFromName.get() is True:
            version: str = ''
        else:
            version: str = '_v' + str(self.currentUploadVersion).zfill(2)

        if self.currentTaskType:
            task: str = '_' + self.currentTaskType.lower()
        else:
            task: str = ''

        extension: str = self.currentFileExtension

        return projectInitial + content + shot + task + version + extension


    def get_folder_name(self) -> str:
        basePath: str = self.base_folder
        content: str = self.selectedContent
        shot: str = self.currentShot

        if self.is_groupByShot.get() is False:
            shot: str = ''

        return os.path.join(basePath, content, shot)


    def select_folder(self) -> None:
        rootPath: str = filedialog.askdirectory()
        if rootPath:
            self.selectedFolderLabel.configure(text=f'Pasta selecionada:\n{rootPath}', justify='center')
            self.base_folder: str = rootPath
        self.validate_next_button()


    def validate_next_button(self) -> None:
        try:
            if self.selectedProject == None:
                messagebox.showwarning("Aviso", "Nenhum projeto selecionado.")
                return

            if not bool(self.base_folder) \
            or not bool(self.taskTypes) \
            or not bool(self.selectedProjectName) \
            or not bool(self.availableContents) \
            or self.selectedProject['type'] == 'short' \
            or self.selectedProject['type'] == 'game':
                self.next_configButton.configure(state='disabled')

            else:
                self.next_configButton.configure(state='enabled')

        except AttributeError:
            self.next_configButton.configure(state='disabled')


    def go_to(self, *panels) -> None:
        for window in self.windows:
            window.pack_forget()
            window.grid_forget()
        for panel in panels:
            panel.pack(expand=True, fill='y')


    def show(self) -> None:
        self.window.mainloop()



x = window()

x.validate_next_button()
x.on_credential_changed(x.credentialsName[0])
x.update_project_list()
x.show()
