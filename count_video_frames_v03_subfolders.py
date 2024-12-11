#!/usr/bin/env python
# :coding: utf-8 BOM

# Este script conta quantos frames tem cada um dos vídeos que está na mesma pasta que ele.
# É recomendado ter o Python 3.7 ou superior instalado em sua máquina.
# Para usar o script, é só copiá-lo para a pasta onde estão os vídeos cujos frames você quer
# contar, e depois disso é só executá-lo e ser feliz :)

import os
import subprocess


try:
    from tqdm import tqdm
except ImportError:
    print("Foi detectado que o módulo 'tqdm' não está instalada em seu sistema. Tentando instalar:")
    os.system("python -m pip install tqdm")
    from tqdm import tqdm


# Garante que o script esteja trabalhando na pasta onde o script se localiza
path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

# Lista todos os vídeos da pasta nos formatos estabelecidos
listOfVideoExtensions = ('.mp4', '.MP4', '.mov', '.MOV')

# Gera um arquivo de texto onde serão colocadas as informações de frames
with open('_frame_count_.txt', 'w') as file:

    file.write('Video Name\tFrames\n')

    for root, folders, files in os.walk(path):

        videoFiles = [x for x in os.listdir(root) if x.endswith(listOfVideoExtensions)]

        print('\t')

        # Conta a quantidade de frames em cada vídeo na pasta.
        for video in  tqdm (videoFiles, colour="#00802b", desc='Contando os frames'):
            videoPath = os.path.abspath(f'{root}/{video}')

            cmds = [
                    'ffprobe',
                    '-v', 'error', 
                    '-count_frames',
                    '-select_streams', 'v:0', 
                    '-show_entries',
                    'stream=nb_read_frames', '-of',
                     'default=nokey=1:noprint_wrappers=1', 
                     videoPath 
                ]
            
            p = subprocess.Popen(cmds, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

            output, error = p.communicate()

            if error:
                print ('Erro encontrado')


            # Pega apenas o nome (sem a extensão) do arquivo para colocar no arquivo de texto
            videoName = os.path.splitext(video)[0]
            file.writelines(f'{videoName}\t{output.decode()}\n')


print('\nTodos os arquivos foram verificados com sucesso.')

print('Arquivo com informações de frames gerado com sucesso.')

input('Aperte <ENTER> para encerrar este script.\n')
