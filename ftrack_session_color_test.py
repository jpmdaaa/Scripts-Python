import os
import json
import requests
import tkinter as tk
from tkinter import ttk

try:
    from ftrack_api import Session
except ImportError:
    print("Foi detectado que a API do ftrack não está instalada em seu sistema. Tentando instalar:")
    os.system("pip install ftrack-python-api")
    from ftrack_api import Session


credentialPath = os.path.abspath(r'F:/Users/joão/Documents/TRABALHO/Scripts/Ftrack/credentials/credentials-admin.json')
# ex: D:/Drives/Onedrive/Trabalho/Hype/Scripts/ftrack/Video Downloader/resources/credentials/credentials-admin.json

with open(credentialPath, 'r') as f:
    data = json.load(f)


def create_button(label, color, window):
    x = tk.Button(window, text=label)
    x.pack()
    x.configure(bg=color)
    r, g, b = [
        int(''.join(color[1:3]), 16),
        int(''.join(color[3:5]), 16),
        int(''.join(color[5:7]), 16),
        ]
    count = (r*0.3 + g*0.114 + b*0.114)
    print(count)
    if count > 120:
        x.configure(fg='#000000')
    else:
        x.configure(fg='#ffffff')


session = Session(
            server_url ="https://hype.ftrackapp.com",
            api_key = data["key"],
            api_user = data["user"]
        )

taskTypes = ['Layout', 'Animation', 'Animatic']
shotName = 'VMB102_SH0030'
projectCode = 'sr010_vamos_brincar'

projectId = session.query(
    f'select id from Project where name is "{projectCode}"'
).first()

window = tk.Tk()

for taskType in taskTypes:

    statusColor = session.query(
        f'''select color, name from Status\
        where tasks.name is {taskType}\
        and tasks.parent.name is {shotName}'''
        ).all()

    for status in statusColor:
        print(f"{status['name']} -> {status['color']}")
        create_button(label=status['name'], color=status['color'], window=window)


window.mainloop()