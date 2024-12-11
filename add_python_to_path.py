# Esse script serve para adicionar o Python sendo usado atualmente ao PATH do sistema.
# Isso é crucial para os scripts funcionarem, já que sem o Python adicionado ao PATH,
# nossos scripts não conseguem instalar as bibliotecas da web via PIP, etc.

# AVISO: esse script só funciona em windows por enquanto.

import os
import sys
import platform
import subprocess


def is_running_on_windows() -> bool:
    OS_NAME = platform.platform(terse=True)

    if 'windows' in OS_NAME.lower():
        return True

    return False


def get_python_folder() -> str:
    folder = os.path.dirname(sys.executable)
    print(folder)

    return folder


def is_python_on_path(pythonFolder) -> bool:

    pathsList = os.environ['PATH'].split(';')

    if pythonFolder in pathsList or (pythonFolder + os.path.sep) in pathsList:
        return True

    return False


def add_python_to_path(pythonFolder):

    # muda a pasta atual pra pasta onde o script se localiza
    os.chdir(os.path.dirname(__file__))
    os.chdir('./resources')

    try:
        # Executa o programa `pathed` para adicionar o caminho ao `PATH`
        subprocess.run(f'pathed -a "{pythonFolder}"')
        subprocess.run(f'''pathed -a "{pythonFolder + os.path.sep + 'Scripts'}"''')

        # Exibe uma mensagem de sucesso
        print("O Python foi adicionado com sucesso ao PATH do computador.")
        print("IMPORTANTE: Você precisa reiniciar o terminal, VS Code etc para essa alteração surtir efeito.")
        print("Na dúvida, reinicie o computador.")

    except Exception as error:
        # Exibe a mensagem de erro caso ocorra qualquer problema
        print(f'ERRO: não foi possível adicionar o Python ao PATH.')
        print("Este foi o erro recebido:")
        print(error)

    finally:
        input("Aperte <ENTER> para continuar.")




if __name__ == "__main__":

    if not is_running_on_windows():
        print("ERRO CRÍTICO: por enquanto esse script só funciona em Windows.",
            "\nOutras plataformas serão suportadas em breve.")
        input("Aperte <ENTER> para sair.")

    else:
        pythonVersion = get_python_folder()

        if is_python_on_path(pythonVersion):
            print("O Python atual já está no PATH do seu sistema. Você não precisa fazer nada.")

        else:
            print("Essa versão de Python precisa ser adicionada ao PATH. Tentando fazer isso...")
            add_python_to_path(pythonVersion)

