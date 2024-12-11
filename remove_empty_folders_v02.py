#!/usr/bin/env python

# Este script acessa todas as subpastas de uma pasta raiz, e envia para a lixeira todas as pastas
# que estao vazias. Para usa-lo, basta jogar o script na pasta desejada, e clicar em executar ele.

import os
import subprocess

# Importa uma biblioteca necessaria para fazer este script enviar pastas para a lixeira
try:
	from send2trash import send2trash
except ImportError:
	print('Foi detectado que você ainda não tem as bibliotecas de Python necessárias para este script funcionar.'
		'\nEste script baixará elas automaticamente para você agora.'
		'\n(Isso é necessário apenas uma vez para este script.)\n')
	subprocess.run(['pip', 'install', 'Send2Trash'])
	from send2trash import send2trash


# Garante que o script esteja trabalhando na pasta onde o script se localiza
path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

# Lista de pastas que foram removidas:
removedFolders = []

# Lista todos os arquivos em TODAS as pastas a partir de onde o script está localizado
def deleteEmptyFolders(root):

	deletedFolders = set()

	for currentFolder, subFolders, files in os.walk(root, topdown=False):
		subDirFolders = any( subdir for subdir in subFolders if os.path.join(currentFolder, subdir) not in deletedFolders)

		if not any(files) and not subDirFolders:
			print(f'A pasta "{currentFolder}" está vazia.')
			removedFolders.append(currentFolder)
			send2trash(currentFolder)
			deletedFolders.add(currentFolder)

	print(f'Todos os arquivos de "{path}" foram verificados com sucesso.\n')

	return deletedFolders

deleteEmptyFolders(path)

if removedFolders:
	revomedFoldersFile = open('list_of_deleted_folders.txt', 'w')
	revomedFoldersFile.write('Estas são as pastas que foram deletadas:\n')

	for file in removedFolders:
		revomedFoldersFile.write(f'{file}\n')

	revomedFoldersFile.close()

	print(f'Foi gerado um arquivo de texto com as pastas que foram removidas.\n')


input('Aperte <ENTER> para encerrar este script.\n')
