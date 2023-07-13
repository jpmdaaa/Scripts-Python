#IMPORTANTE O ARQUIVO MB ou MA, ESTAR COM O PADRAO : (EP / SHOT / ANIM OR LAYOUT / VERSION) EX:'VMB111_SH0450_anim_v01' 
#EDITADO POR JOAO MACEDO EM 10/05/23
#Update 04/04 - Camera Overscan desativado / Adicionado Total de frames ao video final  
#Update 11/04- funcoes renomeadas, script adaptado para funcionar em qualquer projeto 
#Update 10/05 - Infos passadas para cima / Checkbox para alterar smootnhes antes de gerar o playblast

import webbrowser
from maya import cmds, mel
import subprocess
import os
import re
import platform
import json

'''

UI
- Nome do Animador
- Camera
- blocking ou spline(refine)
- TimeLine
- Abrir explorer
- abrir ftrack

OK/Cancel

'''


# ---------------DEFS

def pB_get_file_info():
    filePath = cmds.file(query=True, sceneName=True)
    folder, name = os.path.split(filePath)
    return folder, name


def pB_get_scene_shot(fileName):
    ptn = re.compile(r'sh(\d{4,})', re.IGNORECASE)
    search = re.search(ptn, fileName)
    try:
        shot = search.group(1)
        return shot
    except Exception:
        return ''


def pB_open_file(path):

    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])



def pB_get_scene_sequence(fileName):
    ptn = re.compile(r'seq(\d{3,})', re.IGNORECASE)
    search = re.search(ptn, fileName)
    try:
        sequence = search.group(1)
        return sequence
    except Exception:
        return ''


def pB_HUD_currentFrame():
    minTime = cmds.playbackOptions(q=True, min=True)
    maxTime = cmds.playbackOptions(q=True, max=True)
    viewLay_cFrame = cmds.currentTime(q=True)
    displayTime = '%d ( %d / %d )' % (viewLay_cFrame, minTime, maxTime)
    return displayTime

def pB_HUD_TotalFrame():
    minTime = cmds.playbackOptions(q=True, min=True)
    maxTime = cmds.playbackOptions(q=True, max=True)
    displayTotalTime = (int(maxTime)-int(minTime))
    return displayTotalTime

def pB_playblast_recording(pB_rec_fileName, pB_rec_camera):
    blastResolutionWidthHeight = [1920,1080]
    # newWindows
    if cmds.window('pB_window', exists=True):
        cmds.deleteUI('pB_window')

    pB_mainWindow = cmds.window('pB_window',
                                    title='Playblast Window',
                                    sizeable=False,
                                    w=960,
                                    h=540,
                                    retain=True)

    cmds.paneLayout('pB_window_paneLayout')

    if not cmds.modelPanel('pB_window_modelPanel', ex=1):
        cmds.modelPanel('pB_window_modelPanel')
    else:
        cmds.modelPanel('pB_window_modelPanel', e=1, p='pB_window_paneLayout')

    cmds.showWindow(pB_mainWindow)

    cmds.modelEditor('pB_window_modelPanel',
                     e=1,
                     allObjects=0,
                     polymeshes=1,
                     grid=0,
                     hud=1,
                     imagePlane=1,
                     cam=pB_rec_camera,
                     displayAppearance="smoothShaded",
                     dtx=1,
                     m=0)

    # cmds.setFocus ('pB_window_modelPanel')

    # sound
    gPlayBackSlider = mel.eval('$tmpVar=$gPlayBackSlider')
    sceneSound = False
    if cmds.timeControl(gPlayBackSlider, q=True, sound=True):
        sceneSound = cmds.timeControl(gPlayBackSlider, q=True, sound=True)
    else:
        sceneSound = False
  
    cmds.playblast(filename=pB_rec_fileName,
                   format="qt",
                   editorPanelName='pB_window_modelPanel',
                   forceOverwrite=True,
                   showOrnaments=True,
                   offScreen=True,
                   fp=4,
                   percent=100,
                   viewer=True,
                   compression="H.264",
                   sound=sceneSound,
                   quality=100,
                   widthHeight=blastResolutionWidthHeight)
    
  
    cmds.deleteUI('pB_window')
    cmds.ls('SCENE_grp')
    cmds.displaySmoothness( du=0, dv=0, pw=4, ps=1,po=1)
    
def pB_playblast_action(pB_act_fullFileNamePath, pB_act_camera, pB_act_HUD_userName,
                            pB_act_HUD_shotName):
    ##---------------------- cameraFix
   
    # [CamAttribut  s, defaultValue, User_defaultValue]
    camAttrMatrix = [['.displayFilmGate', False, False],
                         ['.displayResolution', True, False],
                         ['.displayGateMask', True, False],
                         ['.displayGateMaskOpacity', 1, 1],
                         ['.displayGateMaskColorR', 0, 0],
                         ['.displayGateMaskColorG', 0, 0],
                         ['.displayGateMaskColorB', 0, 0],
                         ['.displayFieldChart', False, False],
                         ['.displaySafeAction', True, False],
                         ['.displaySafeTitle', True, False],
                         ['.displayFilmPivot', False, False],
                         ['.displayFilmOrigin', False, False],
                         ['.overscan', 1.1, False],
                         ['.panZoomEnabled', False, False]]
    cam = cmds.ls(type='camera')
    cameraShape = cam[0]
    cmds.setAttr(cameraShape+'.overscan', lock=False)
    #print(cameraShape)
    #lista = cmds.listConnections(cam[0])
    #print(lista)
    #cmds.disconnectAttr(cam[0]+ '.overscan',lista[0])

    for i in range(len(camAttrMatrix)):
        camAttrMatrix[i][2] = cmds.getAttr(pB_act_camera + camAttrMatrix[i][0])
        cmds.setAttr(pB_act_camera + camAttrMatrix[i][0], camAttrMatrix[i][1])

    # display Preferences
    displayPrefs = [['Font Size (sfs)', 100, cmds.displayPref(q=0, sfs=True)],
                        ['Font Option (FM)', 50, cmds.displayPref(q=1, fm=True)],
                        ['hardwareRenderingGlobals.ssaoEnable', True,
                         cmds.getAttr('hardwareRenderingGlobals.ssaoEnable')],
                        ['hardwareRenderingGlobals.multiSampleEnable', True,
                         cmds.getAttr('hardwareRenderingGlobals.multiSampleEnable')]]

    
    cmds.displayPref(fm=displayPrefs[1][1])
    cmds.displayPref(sfs=displayPrefs[0][1])
    cmds.setAttr(displayPrefs[2][0], displayPrefs[2][1])
    cmds.setAttr(displayPrefs[3][0], displayPrefs[3][1])
    cmds.displayPref(sfs=100, dfs=50) #font size


    # ---------------------- HUD
    ##query and hide previous huds
    prevHUD = {}
    for headsup in cmds.headsUpDisplay(listHeadsUpDisplays=True):
        vis = cmds.headsUpDisplay(headsup, q=True, vis=True)
        prevHUD[headsup] = vis
        cmds.headsUpDisplay(headsup, e=True, vis=False)

    # UserName
    pB_HUD_userName = pB_act_HUD_userName
    pB_UI_animProc = cmds.optionMenu('UI_processInput', query=True, value=True)  # blocking / refine / fix / layout
    if cmds.headsUpDisplay('HUD_userName', q=True, ex=True):
        cmds.headsUpDisplay('HUD_userName', rem=True)
    
    if pB_UI_animProc!="layout":
        cmds.headsUpDisplay('HUD_userName', s=0, b=cmds.headsUpDisplay(nextFreeBlock=0), bs='large',
                        lfs='large', label='Animator: ' + pB_HUD_userName, ao=True)
    else:
        cmds.headsUpDisplay('HUD_userName', s=0, b=cmds.headsUpDisplay(nextFreeBlock=0), bs='large',
                        lfs='large', label='Layouter: ' + pB_HUD_userName, ao=True)

    # shotName
    pB_HUD_shotName = pB_act_HUD_shotName
    if cmds.headsUpDisplay('HUD_shotName', q=True, ex=True):
        cmds.headsUpDisplay('HUD_shotName', rem=True)
    cmds.headsUpDisplay('HUD_shotName', s=1, b=cmds.headsUpDisplay(nextFreeBlock=1), bs='large',
                        lfs='large', label=pB_HUD_shotName, ao=True)

    # cFrame
    pB_HUD_currentFrame = 'Current Frame:'
    if cmds.headsUpDisplay('HUD_currentFrame', q=True, ex=True):
        cmds.headsUpDisplay('HUD_currentFrame', rem=True)
    cmds.headsUpDisplay('HUD_currentFrame', s=3, b=cmds.headsUpDisplay(nextFreeBlock=3), bs='large',
                        lfs='large', label=pB_HUD_currentFrame, command='pB_HUD_currentFrame()',
                        attachToRefresh=True, ao=True)

    # Total Frames
    pB_HUD_TotalFrames= 'Total Frames:'
    if cmds.headsUpDisplay('HUD_TotalFrames', q=True, ex=True):
        cmds.headsUpDisplay('HUD_TotalFrames', rem=True)
    cmds.headsUpDisplay('HUD_TotalFrames', s=4, b=cmds.headsUpDisplay(nextFreeBlock=4), bs='large',
                        lfs='large', label=pB_HUD_TotalFrames, command='pB_HUD_TotalFrame()', ao=True)

    if cmds.checkBox('Smoothness', v=True):
         cmds.ls('SCENE_grp')
         cmds.displaySmoothness( du=3, dv=3, pw=16, ps=4,po=3 )
         #print("alterou smoothness")
    else:
          cmds.ls('SCENE_grp')
          cmds.displaySmoothness( du=0, dv=0, pw=4, ps=1,po=1)
          #print("nao alterou smoothness")
          
    
    ##PlayblastRUN
    pB_playblast_recording(pB_act_fullFileNamePath, pB_act_camera)
   
    # Camera
    for i in range(len(camAttrMatrix)):
        cmds.setAttr(pB_act_camera + camAttrMatrix[i][0], camAttrMatrix[i][2])

    # HUDS
    for headsup in prevHUD:
        cmds.headsUpDisplay(headsup, e=True, vis=prevHUD[headsup])
    cmds.headsUpDisplay('HUD_userName', rem=True)
    cmds.headsUpDisplay('HUD_shotName', rem=True)
    cmds.headsUpDisplay('HUD_currentFrame', rem=True)
    cmds.headsUpDisplay('HUD_TotalFrames', rem=True)

    ## openLinks
    pB_open_file(os.path.dirname(pB_act_fullFileNamePath))
   
    #webbrowser.open(str("https://hype.ftrackapp.com/"))
   
    #print("retornou smoothness")

    # close UI
    if cmds.window('playblast_UI', exists=True):
        cmds.deleteUI('playblast_UI')


def pB_UI_runCMD(selectPath, pB_fileName, pB_UI_cameraName, pb_UI_userName):
    # CHECK IF EXISTS
    if not os.path.exists(selectPath + pB_fileName):
        pB_playblast_action(selectPath + pB_fileName, pB_UI_cameraName, pb_UI_userName,
                                pB_fileName)
    else:
        confirmAction = cmds.confirmDialog(title='Confirm',
                                           message=pB_fileName + ' already exists. Do you want to replace it?',
                                           button=['Yes', 'No'],
                                           defaultButton='Yes',
                                           cancelButton='No',
                                           dismissString='No')

        if confirmAction == 'Yes':
            pB_playblast_action(selectPath + pB_fileName, pB_UI_cameraName, pb_UI_userName,
                                    pB_fileName)


def pB_UI_gettingFileInfo():
    if cmds.file(query=True, sceneName=True, shn=True):
        fileName, fileExtension = cmds.file(query=True, sceneName=True, shn=True).split('.')

        fileParts = fileName.split('_')
        
        # seq / ep
        fileParts[0] = fileParts[0].replace('VMB', '')
        fileParts[0] = fileParts[0].replace('TEM', '')

        # shot
        fileParts[1] = fileParts[1].replace('SH', '')
       
        # version
        fileParts[3] = fileParts[3].replace('v', '')
    

        # camera
       
        fileParts.append('CAM_SH' + fileParts[1]+ '_grp')

        # timeStart
        fileParts.append(cmds.playbackOptions(q=True, min=True))
        # timeEnd
        fileParts.append(cmds.playbackOptions(q=True, max=True))

        return fileParts
    else:
        return False


##-----------------------------INTERFACE----------------------------------

def pB_UI():
    if cmds.window('playblast_UI', exists=True):
        cmds.deleteUI('playblast_UI')

    # vars
    fileData = pB_UI_gettingFileInfo()
    labelW = 80
    TotalFrames= (int(fileData[6])- int(fileData[5]))
   
    pB_UI_mainWindow = cmds.window('playblast_UI', title='  Playblast' , sizeable=False,
                                       retain=True)

    cmds.columnLayout(columnOffset=['both', 20])

    cmds.rowLayout(nc=1)
    cmds.text('Playblast Settings', align='center', font='boldLabelFont', width=200, height=40)
    cmds.setParent('..')

    cmds.rowLayout(nc=5)
    cmds.text('Camera', w=100, h=40, align='right', font='boldLabelFont')
    cmds.separator(w=10, m=False)
    cmds.textField('UI_cameraInput', tx="CAM_SH"+ fileData[1], w=110, h=30, font='fixedWidthFont')
    cmds.setParent('..')

    cmds.rowLayout(nc=5)
    cmds.text('Sequence/Episode', w=100, h=40, align='right', font='boldLabelFont')
    cmds.separator(w=10, m=False)
    cmds.textField('UI_sequenceInput', tx=fileData[0], w=110, h=30, font='fixedWidthFont')
    cmds.setParent('..')

    cmds.rowLayout(nc=5)
    cmds.text('Shot number', w=100, h=40, align='right', font='boldLabelFont')
    cmds.separator(w=10, m=False)
    cmds.textField('UI_shotInput', tx=fileData[1], w=110, h=30, font='fixedWidthFont')
    cmds.setParent('..')

    cmds.rowLayout(nc=5)
    cmds.text('Frame start', w=100, h=40, align='right', font='boldLabelFont')
    cmds.separator(w=10, m=False)
    cmds.textField('UI_startInput', tx=int(fileData[5]), w=110, h=30, font='fixedWidthFont')
    cmds.setParent('..')

    cmds.rowLayout(nc=5)
    cmds.text('Frame end', w=100, h=40, align='right', font='boldLabelFont')
    cmds.separator(w=10, m=False)
    cmds.textField('UI_endInput', tx=int(fileData[6]), w=110, h=30, font='fixedWidthFont')
    cmds.setParent('..')

    
    cmds.rowLayout(nc=5)
    cmds.text('Total Frames', w=100, h=40, align='right', font='boldLabelFont')
    cmds.separator(w=10, m=False)
    cmds.textField('UI_endInput', tx=int(TotalFrames), w=110, h=30, font='fixedWidthFont')
    cmds.setParent('..')

    cmds.rowLayout(nc=5)
    cmds.text('Process', w=100, h=40, align='right', font='boldLabelFont')
    cmds.separator(w=10, m=False)
    cmds.optionMenu('UI_processInput', w=110, h=30)
    

    cmds.menuItem(parent='UI_processInput', label='blocking')
    cmds.menuItem(parent='UI_processInput', label='spline')
    cmds.menuItem(parent='UI_processInput', label='fix')
    cmds.menuItem(parent='UI_processInput', label='layout')
    cmds.setParent('..')

    cmds.rowLayout(nc=5)
    cmds.text('User Name', w=100, h=40, align='right', font='boldLabelFont')
    cmds.separator(w=10, m=False)
    cmds.textField('UI_nameInput', tx='', w=110, h=30, font='fixedWidthFont')
    cmds.setParent('..')


    cmds.rowLayout(nc=5)
    cmds.text('Force smoothness', w=100, h=40, align='right', font='boldLabelFont')
    cmds.separator(w=10, m=False)
    chekBoxSmooth= cmds.checkBox('Smoothness', w=110, h=30,value=False)
    cmds.setParent('..')

    cmds.rowLayout(nc=5)
    cmds.separator(h=60, m=False)
    cmds.button('Play', command='pB_UI_b_play()', width=90, height=30)
    cmds.separator(w=20, m=False)
    cmds.button('Cancel', command='cmds.deleteUI(\'playblast_UI\')', height=30, w=90)
    cmds.setParent('..')

    cmds.showWindow(pB_UI_mainWindow)


def pB_UI_b_play():

    fileInfos = pB_UI_gettingFileInfo()

    pB_UI_cameraName = cmds.textField('UI_cameraInput', q=1, tx=1)
    pB_UI_animProc = cmds.optionMenu('UI_processInput', query=True, value=True)  # blocking / refine / fix / layout
    pb_UI_userName = cmds.textField('UI_nameInput', q=1, tx=1)
    pb_UI_sequence = cmds.textField('UI_sequenceInput', q=1, tx=1)
    pb_UI_shot = cmds.textField('UI_shotInput', q=1, tx=1)
    pb_fileVersion = fileInfos[3]
    pb_UI_timeLineStart = cmds.textField('UI_startInput', q=1, tx=1)
    pb_UI_timelineEnd = cmds.textField('UI_endInput', q=1, tx=1)
    pb_UI_explorer = True
    pb_UI_Ftrack = True

    # FIX ANIMATION PATH
    pB_animationFilePath = ''
    if pB_UI_animProc == 'blocking':
        pB_animationFilePath = '01_' + pB_UI_animProc
    elif pB_UI_animProc == 'spline':
        pB_animationFilePath = '02_' + pB_UI_animProc
    elif pB_UI_animProc == 'fix':
        pB_animationFilePath = '03_' + pB_UI_animProc
    elif pB_UI_animProc == 'layout':
        pB_animationFilePath = '04_' + pB_UI_animProc
    # Obter o caminho absoluto do diretório atual
    current_directory = os.path.abspath('.')

    # Obter o disco principal do caminho absoluto
    main_disk = current_directory.split(os.sep)[0]


    if os.path.exists(main_disk+ '/hype/playblast_gen/pathPlayBlast.json'):
        pathJson= open(main_disk+ '/hype/playblast_gen/pathPlayBlast.json')
        data= json.load(pathJson)
        print(data['Path'])
        selectPath=data['Path']
        print("Json encontrado")
        print("Path playblast: " + selectPath[0])

    else:
        selectPath= cmds.fileDialog2(fileMode=3)
         
        if selectPath:
            savePath = {'Path': selectPath}
            #pathJson= (str(selectPath) + '/path.json')
            #pathJson= pathJson.replace("[","").replace("]","").replace("u'","").replace('\\', '/').replace("'","")
            #pathJson= pathJson.encode('unicode_escape').decode()
            #print(pathJson)
            if os.path.exists(main_disk+ '/hype/playblast_gen/pathPlayBlast.json'):
                pass
            else:
                os.makedirs(main_disk+ '/hype/playblast_gen/')

            with open(main_disk+ '/hype/playblast_gen/pathPlayBlast.json', 'w') as file:
                json.dump(savePath, file)
                print("Json criado em: "+ main_disk+ '/hype/playblast_gen/pathPlayBlast.json')
                print("caminho salvo em: "+ selectPath[0])
            
        else:
            print("Selecione um caminho valido")
            return  
    
    
    # Path and File
   
   
    '''pB_filePath = cmds.workspace(q=True,
                                     rd=True) + 'sequences/seq' + pb_UI_sequence + '/sh' + pb_UI_shot + '/03_animation/' + pB_animationFilePath + '/movies/'''
    pB_fileName = pb_UI_sequence + '_SH' + pb_UI_shot + '_' + pB_UI_animProc + '_v' + pb_fileVersion + '.mov'
    selectPath[0]= selectPath[0]+ "/"
    
    if len(pb_UI_userName) > 2:
        pB_UI_runCMD(selectPath[0], pB_fileName, pB_UI_cameraName, pb_UI_userName)
    else:
        cmds.confirmDialog(title='Error',
                           message='You need to save shot with template (EP / SHOT / ANIM OR LAYOUT / VERSION))',
                           button=['Ok'],
                           defaultButton='Ok',
                           cancelButton='No',
                           dismissString='No')
  

def main():
    
    if pB_UI_gettingFileInfo(): 
        pB_UI()
    else:
        cmds.confirmDialog(title='Error',
                           message='You need to write a valid name.',
                           button=['Ok'],
                           defaultButton='Ok',
                           cancelButton='No',
                           dismissString='No')
              
        
     
if __name__ == '__main__':
  
    main()
