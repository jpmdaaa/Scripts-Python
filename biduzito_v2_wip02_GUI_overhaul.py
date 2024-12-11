import os
import json
import tkinter as tk
from tkinter import ttk, messagebox

try:
    from ftrack_api import Session
except ImportError:
    print("Foi detectado que a API do ftrack não está instalada em seu sistema. Tentando instalar:")
    os.system("python -m pip install ftrack-python-api")
    from ftrack_api import Session

from resources.typeHints import *
from typing import Literal

# Garante que o script esteja trabalhando na pasta onde o script se localiza
try:
    scriptPath: str = os.path.dirname(os.path.realpath(__file__))
    os.chdir(scriptPath)
except NameError:
    pass


class MainWindow():

    def __init__(self) -> None:

        # ---------- Setup inicial ----------
        self.window = tk.Tk()
        self.window.title('ftrack Tasks')
        self.window.geometry('600x500')

        # ---------- Parâmetros ----------
        self.selectedCredential_var = tk.StringVar()
        self.selectedProject_var = tk.StringVar()
        self.selectedUser_var = tk.StringVar()
        self.availableUsers_list: list[str] = []
        # ---------- Parâmetros ----------


        # ---------- separa o nome das credenciais disponíveis
        self.availableCredentials: (dict[str, dict[str, str]]) = self.list_available_credentials()
        self.credentialsName: list[str] = []
        self.availableProjects: list[str] = []

        if self.availableCredentials == None:
            messagebox.showwarning("Aviso!", "Nenhuma credencial disponível. Verifique se existe uma pasta junto do script "
                "chamada 'resources', e dentro dela existe uma pasta de 'credentials' com alguma credencial dentro.\n"
                "Qualquer dúvida, favor solicitar uma credencial ao setor de Produção ou de Pipeline")

        else:
            for cred in self.availableCredentials:
                x: str = self.availableCredentials[cred]['display_name']
                self.credentialsName.append(x)


        # ----------------------------------- Definição das principais áreas da interface -----------------------------------
        self.main_window = ttk.Frame(self.window)

        self.top_frame = ttk.Frame(self.main_window)
        self.main_frame = ttk.Frame(self.main_window)
        self.bottom_frame = ttk.Frame(self.main_window, style='test.TFrame')


        # ----------------------------------- Sessão superior -----------------------------------
        # ---------- Credencial selecionada
        self.credentials_label = ttk.Label(self.top_frame, text='Credencial')
        self.credentials_label.grid(row=0, column=0, sticky='s', padx=5)

        self.credentials_list = ttk.OptionMenu(self.top_frame, self.selectedCredential_var, self.credentialsName[0], *self.credentialsName, command=self.on_credential_changed, direction='below', style='credential.TMenubutton')
        self.credentials_list.grid(row=1, column=0, sticky='n', padx=5)


        # ---------- Projeto selecionado
        self.projectsList_label = ttk.Label(self.top_frame, text='Projeto')
        self.projectsList_label.grid(row=0, column=1, sticky='s')

        self.projects_list = ttk.OptionMenu(self.top_frame, self.selectedProject_var, 'Escolha um projeto', *self.availableProjects, command=self.on_project_changed, direction='below', style='credential.TMenubutton')
        self.projects_list.configure(width=20)
        self.projects_list.grid(row=1, column=1, sticky='n', padx=5, ipadx=10)


        # ---------- Usuário selecionado
        self.usersList_label = ttk.Label(self.top_frame, text='Usuário')
        self.usersList_label.grid(row=0, column=2, sticky='s')

        self.users_list = ttk.OptionMenu(self.top_frame, self.selectedUser_var, 'Escolha um user', *self.availableUsers_list, command=self.on_user_changed, direction='below', style='credential.TMenubutton')
        self.users_list.configure(width=15)
        self.users_list.grid(row=1, column=2, sticky='n', padx=5, ipadx=5)




        # ----------------------------------- Sessão principal -----------------------------------
        emptyUser_label = ttk.Label(self.main_frame, text='Por favor escolha um projeto e um nome de usuário.', wraplength=350)
        emptyUser_label.pack()


        self.tasks_tree = ttk.Treeview(self.main_frame, columns=('status', 'state', 'type', 'link'))
        self.tasks_tree.pack(expand=True, fill='both')

        self.top_frame.pack(anchor='e', padx=10, side='top')
        self.bottom_frame.pack(side='bottom')
        self.main_frame.pack(expand=True, fill='both', side='bottom')

        self.main_window.pack(fill='both', expand=True)

        # ttk.Separator(self.main_window, orient='horizontal').pack(fill='x', anchor='w', pady=5, before=self.bottom_frame)
        ttk.Separator(self.main_window, orient='horizontal').pack(fill='x', anchor='w', pady=5, after=self.top_frame)

        # Testes de estilo:
        style = ttk.Style()
        # style.configure('TLabel', background='#b5ffbb')
        style.configure('TMenubutton', background='#cad4df')
        style.configure('main.TMenubutton', width=30)



    def populate_treeview_with_tasks(self, tasksDict: dict):

        self.tasks_tree.delete(*self.tasks_tree.get_children())

        for task in tasksDict:
            self.tasks_tree.insert(
                parent='',
                index='end',
                text=tasksDict[task]['path'],
                values=(
                    tasksDict[task]['status'],
                    tasksDict[task]['state'],
                    tasksDict[task]['type'],
                    tasksDict[task]['url']
                    )
                )

        ...



    def get_selected_credential(self, selection) -> (dict[str, str]) | None:

        if self.availableCredentials == None:
            messagebox.showwarning("Aviso!", "Nenhuma credencial selecionada. Verifique se existe uma pasta junto do script "\
                "chamada 'resources', e dentro dela existe uma pasta de 'credentials' com alguma credencial dentro.")
            return

        for key in self.availableCredentials:
            for item in self.availableCredentials[key]:
                if self.availableCredentials[key]['display_name'] == selection:
                    selectedItem: dict[str, str] = self.availableCredentials[key]
                    return selectedItem



    def get_selected_project(self, selection) -> (dict[str, str]):
        for key in self.projectsDict:
            for item in self.projectsDict[key]:
                if self.projectsDict[key]['name'] == selection:
                    selectedItem: dict[str, str] = self.projectsDict[key]
                    return selectedItem



    def list_available_credentials(self) -> (dict[str, dict[str, str]]) | None:
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

        selectedCredential: (dict[str, str]) = self.get_selected_credential(selection)

        with open(self.cretendialPath + selectedCredential['file_name'], 'r') as f:
            data = json.load(f)

        self.session = Session(
            server_url ="https://hype.ftrackapp.com",
            api_key = data["key"],
            api_user = data["user"]
        )

        self.serverLocation: Location = self.session.query(
                'Location where name is "ftrack.server"').one()



    def on_project_changed(self, selection) -> None:

        self.selectedProject: (dict[str, str]) = self.get_selected_project(selection)

        self.selectedProjectName: str = self.selectedProject['name']

        print(f'Projeto selecionado: {self.selectedProject["name"]}')

        self.update_users_list()



    def on_user_changed(self, selection) -> None:

        user = self.get_info_from_user(selection)

        if user == None:
            print("AVISO: usuário não encontrado:", selection)
            return

        self.selectedUser_var.set(user['name'])

        userTasks = self.get_tasks_from_user(username=user['username'])

        self.populate_treeview_with_tasks(tasksDict=userTasks)

        print(f'Usuário selecionado: {user}')



    def get_info_from_user(self, user) -> dict[str, str]  | None:

        for person in self.usersDict:
            if self.usersDict[person]['name'] == user:
                return self.usersDict[person]



    def get_tasks_from_user(self, username) -> dict[str, dict[str, str]] | None:

        tasksDict= {}

        taskQuery = self.session.query(
            f"""select name, status, type, link, id
            from Task
            where assignments any (resource.username = "{username}")
            and project_id is "{self.selectedProject['id']}"
            """
        ).all()

        if len(taskQuery) == 0:
            print("\t(Este usuário não possui nenhuma task pendente neste projeto.)")

        else:
            for task in taskQuery:

                tasksDict[task] = {
                    'path' : ' / '.join(x['name'] for x in task['link'][1:]),
                    'url': (
                        r'https://hype.ftrackapp.com/#slideEntityId='
                        + task['id']
                        + r'&slideEntityType=task&entityId='
                        + self.selectedProject['id']
                        + r'&entityType=show&itemId=projects'
                        ),
                    'status': task['status']['name'],
                    'type': task['type']['name'],
                    'state': task['status']['state']['name']
                    }

            return tasksDict




    def update_project_list(self) -> None:

        projects: list[QueryResult] = self.session.query(
            'select full_name, name, id, custom_attributes, allocations '
            'from Project where status is "Active" '
            ).all()

        availableProjectsDict: dict[str, dict[str,str] ] = {}
        availableProjectNamesList: list[str] = []

        for result in projects:
            project: dict[str, str] = {
                'name': result['full_name'],
                'code': result['name'],
                'initials': result['custom_attributes']['initials'],
                'id': result['id'],
                'allocations': result['allocations']
            }
            availableProjectsDict[project['name']] = project
            availableProjectNamesList.append(project['name'])

        self.availableProjects: list[str] = sorted(availableProjectNamesList)
        self.projectsDict: dict[str, dict[str, str]] = availableProjectsDict
        self.projects_list.set_menu('Selecione um projeto', *self.availableProjects)



    def update_users_list(self)-> None:

        users: list[QueryResult] = self.session.query(
            f"""select assignments, first_name, last_name, username
                from User
                where assignments any (context.project_id =  "{self.selectedProject['id']}")
                """).all()

        usersDict = {}
        namesList = []

        for user in users:
            usersDict[user] = {
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'name': ' '.join((user['first_name'], user['last_name'])),
                'username': user['username'],
            }

            namesList.append(usersDict[user]['name'])


        self.availableUsers_list: list[str] = sorted(namesList)
        self.users_list.set_menu('Selecionar um nome, ', *self.availableUsers_list)

        self.usersDict: dict[str, dict[str, str]] = usersDict



    def show(self) -> None:
        self.window.mainloop()



if __name__ == '__main__':

    x = MainWindow()
    x.on_credential_changed(x.credentialsName[0])
    x.update_project_list()
    x.show()
