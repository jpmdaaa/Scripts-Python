#os.environ["GIT_PYTHON_REFRESH"] = "quiet"
import os
from git import Repo
import shutil




class Main():
    def __init__(self):
        # Instantiate repo object
        #local do repositorio no PC
        self.repo_dir=("F:/Users/joão/Documents/TRABALHO/Scripts/Git/scripts")
        #URL do repositorio no git
        self.repo_url = "https://github.com/hype-admin/scripts"
        self.repo = Repo(self.repo_dir)

        #self.checkRepo()
        #self.pullGit()
        self.commit()
    
      
    def pullGit (self):
        #atualiza o projeto (pull)
        self.repo.git.pull()
        print("Repositório atualizado")

    def checkRepo(self):
        #checa se o repositorio ja foi clonado, se nao ele clona
        if not os.path.exists(self.repo_dir):
            Repo.clone_from(self.repo_url, self.repo_dir)

    def commit(self):

        #caminho do script aberto
        caminho_script = os.path.realpath(__file__)
        # Define o novo caminho do arquivo
        novo_caminho_script = self.repo_dir
        # Copia o arquivo para o novo local
        shutil.copy2(caminho_script, novo_caminho_script)
        # Commit changes
        self.repo.git.add([novo_caminho_script])
        #commit("Nome do comitt que vai para o git")
        self.repo.index.commit("Added AutoUpdateGit.py")
        print("Arquivo adicionado ao Repositório")
        #self.pushGit()

    def pushGit(self):
        # envia as mudanças para o repositório no git (push)
        self.repo.git.push("--set-upstream", "origin", "Joao-Branch")

    def mergeGit(self): 
        # Merge a branch into the current branch
        self.repo.git.merge("joao_branch")
        
    def deleteBranch(self):
        # Delete uma branch
        self.repo.git.branch("-D", "my_branch")

Main()