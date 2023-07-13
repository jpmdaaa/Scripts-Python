#!/usr/bin/env python
# :coding: latin-1

# Este script acessa todos os arquivos .ma que estão em uma pasta e suas respectivas subpastas, e remove
# o aviso de estudante que aparece para contas não-estudantis quando alguém utilizou uma versão estudantil
# do Maya para abrir o arquivo. Para usar o script, apenas copie ele para a pasta a partir de onde você
# quer executar esta varredura, e depois disso é só executar o script.

# IMPORTANTE: esse script precisa baixar TODOS os arquivos de TODAS as subpastas em que você colocar ele
# caso não sejam arquivos locais. Por isso ele pode demorar um pouco pra executar caso você esteja colocando
# ele em uma pasta da nuvem, como o Z por VPN, Google Drive ou Dropbox.

import os
import re
import logging

# Garante que o script esteja trabalhando na pasta onde o script se localiza
path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

# Define as configurações que serão usadas para gerar o arquivo de log
logging.basicConfig(
	filename='maya_student_tag_remover_log.txt',
	level=logging.INFO,
	format='%(asctime)s - %(message)s',
	datefmt='%Y-%m-%d %H:%M'
	)

# Forma prática de garantir que o que aparece no prompt de comando também está gerando um arquivo de log
def printMessage(text):
	logging.info(text)
	print(text)
	return

# Listas de arquivos usada para listar arquivos que foram alterados, e arquivos com erro:
filesWithStudentTag = []
filesWithError = []

# Lista todos os arquivos em TODAS as pastas a partir de onde o script está localizado
for root, dirs, files in os.walk(path):
	mayaFiles = [x for x in files if x.endswith('.ma')]
	for file in mayaFiles:
		filePath = os.path.join(root, file)

		printMessage(f'Analisando o arquivo {filePath}')

		try:
			content = open(filePath, 'r')
			oldData = content.read()
			content.close()

		except Exception as errorMessage:
			printMessage(f'O arquivo {filePath} encontrou um erro e não pode ser lido. Mais informações abaixo:')
			logging.exception('ExceptionMessage')
			filesWithError.append((filePath, errorMessage))

		# Com expressão regular, remove a linha que fala de licença de estudante
		regexObject = re.subn('fileInfo "license" "student";\n', '', oldData)

		# re.subn() tem dois ítens: o primeiro é o resultado da substituição gerada pela expressão regular
		newData = regexObject[0]
		# o segundo item é quantas correspondências foram encontradas
		numberOfSubstitutions = regexObject[1]

		if numberOfSubstitutions == 0:
			printMessage(f'Nenhuma tag foi encontrada neste arquivo.\n')

		# Caso o arquivo tenha a linha de estudante que precisa ser removida, a gente sobreescreve o conteúdo
		# do arquivo original pelo conteúdo com as ocorrências substituídas
		elif numberOfSubstitutions >= 1:
			content = open(filePath, 'w')
			content.write(newData)
			filesWithStudentTag.append(filePath)
			printMessage(f'Este arquivo possuia tag de estudante, que foi removida com sucesso.\n')

		content.close()

printMessage(f'Todos os arquivos foram verificados com sucesso.\n')


if filesWithStudentTag:
	studentTagFile = open('list_of_files_with_student_tag.txt', 'w', encoding='latin-1')
	studentTagFile.write('Estes são os arquivos que tinham tag de estudante:\n')

	for file in filesWithStudentTag:
		studentTagFile.write(f'{file}\n')

	studentTagFile.write('\nLembrando que a tag de estudante desses arquivos já foi removida automaticamente pelo script.')
	studentTagFile.close()

	printMessage(f'Foi gerado um arquivo de texto com os arquivos que haviam tag de estudante.\n')


if filesWithError:
	errorFile = open('list_of_files_with_errors.txt', 'w', encoding='latin-1')
	errorFile.write('Estes são os arquivos que não puderam ser lidos, junto de seus respectivos erros:\n\n')

	for file in filesWithError:
		for component in file:
			errorFile.write(f'{component}\n')
		errorFile.write('\n\n')

	errorFile.close()

	printMessage(f'Foi gerado um arquivo de texto com os arquivos que não puderam ser escaneados.\n')


input('Aperte <ENTER> para encerrar este script.\n')