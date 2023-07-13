# -*- coding: utf-8 -*-

import os
import maya.cmds as cmds
import json
import glob

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


# Custom Modules
import sys
customModulePath = os.path.join(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(customModulePath)
from resources import pylightxl



def onMayaDroppedPythonFile(obj):
    from maya import mel
    """Ao arrastar o script pro Maya, ele cria um icone na shelf de layout"""

    # Garante que o script esteja trabalhando na pasta onde o script se localiza
    _scriptPath = os.path.dirname(os.path.realpath(__file__))
    os.chdir(_scriptPath)
    _scriptFileName = os.path.splitext(os.path.split(__file__)[1])[0]

    # get top shelf
    gShelfTopLevel = mel.eval("$tmpVar=$gShelfTopLevel")

    # get top shelf names
    shelves = cmds.tabLayout(gShelfTopLevel, query=1, ca=1)

    # create shelf if does not exist
    shelfName = 'Hype_layout'
    if shelfName not in shelves:
        cmds.shelfLayout(shelfName, parent=gShelfTopLevel)


    # add button
    cmds.shelfButton(
        label='SqGen',
        annotation='Sequence Gen',
        parent=shelfName,
        image= _scriptPath + '/resources/icons/sequence_gen_icon.png',
        command='import sys \nsys.path.append(r"{0}")\ntry:\n\treload({1})\nexcept NameError:\n\timport {1}'.format(_scriptPath, _scriptFileName),
        docTag='SqGen',
        )

    cmds.inViewMessage(
        amg='Botao criado com sucesso na shelf <hl>{0}</hl>.'.format(shelfName),
        pos='midCenter', fade=True )



# Code
def unique(list1):
    # insert the list to the set
    list_set = set(list1)
    # convert the set to the list
    unique_list = (list(list_set))
    return unique_list
    # for x in unique_list:
    #     print(x,)

class SequenceGen:
    def __init__(self):
        self.window = QWidget()
        self.window.resize(850, 500)
        self.window.setWindowTitle('Sequence Generator v02 - Release Candidate 01')
        self.window.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.vLayout = QVBoxLayout()
        self.vLayout.setAlignment(Qt.AlignTop)


        self.sheetPathString = ""
        self.referencePathString = ""
        self.audioPathString = ""
        self.sequencePathString = ""
        self.projectTypeString = ""
        self.projectStructureString = ""
        self.projectInitialsString = ""

        self.loadWindowPrefs()

        self.hLayoutHeader1 = QHBoxLayout()
        self.hLayoutHeader1.setAlignment(Qt.AlignLeft)

        self.hLayoutHeader2 = QHBoxLayout()
        self.hLayoutHeader2.setAlignment(Qt.AlignLeft)

        self.hLayoutHeader3 = QHBoxLayout()
        self.hLayoutHeader3.setAlignment(Qt.AlignLeft)

        self.hLayoutHeader4 = QHBoxLayout()
        self.hLayoutHeader4.setAlignment(Qt.AlignLeft)


        # Planilha Path TextField
        self.planilhaPathLabel = QLabel("Excel path:")
        self.planilhaPathLabel.setFixedWidth(150)
        self.planilhaPathLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.sheetPathTextField = QLineEdit()
        self.sheetPathTextField.setText(self.sheetPathString)
        self.planilhaPathBrowseButton = QPushButton("Browse")
        self.planilhaPathBrowseButton.clicked.connect(lambda: self.select_file(textField=self.sheetPathTextField, hint='Escolha a planilha a ser usada'))
        self.sheetPathTextField.textChanged.connect(self.on_path_changed)
        self.sheetPathTextField.textChanged.connect(self.saveWindowPrefs)


        # References Path TextField
        self.referencePathLabel = QLabel("Refs/proxies path:")
        self.referencePathLabel.setFixedWidth(150)
        self.referencePathLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.referencePathTextField = QLineEdit()
        self.referencePathTextField.setText(self.referencePathString)
        self.referencePathBrowseButton = QPushButton("Browse")
        self.referencePathBrowseButton.clicked.connect(lambda: self.select_folder(textField=self.referencePathTextField, hint='Selecione a pasta de references ou de proxies'))
        self.referencePathTextField.textChanged.connect(self.on_path_changed)
        self.referencePathTextField.textChanged.connect(self.saveWindowPrefs)


        # Audio Path TextField
        self.audioPathLabel = QLabel("Audio path:")
        self.audioPathLabel.setFixedWidth(150)
        self.audioPathLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.audioPathTextField = QLineEdit()
        self.audioPathTextField.setText(self.audioPathString)
        self.audioPathBrowseButton = QPushButton("Browse")
        self.audioPathBrowseButton.clicked.connect(lambda: self.select_folder(textField=self.audioPathTextField, hint='Selecione a pasta de audio'))
        self.audioPathTextField.textChanged.connect(self.on_path_changed)
        self.audioPathTextField.textChanged.connect(self.saveWindowPrefs)


        # Sequences/Episodes Path TextField
        self.sequencePathLabel = QLabel("Sequences/episodes path:")
        self.sequencePathLabel.setFixedWidth(150)
        self.sequencePathLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.sequencePathTextField = QLineEdit()
        self.sequencePathTextField.setText(self.sequencePathString)
        self.sequencePathBrowseButton = QPushButton("Browse")
        self.sequencePathBrowseButton.clicked.connect(lambda: self.select_folder(textField=self.sequencePathTextField, hint='Selecione a pasta de sequencias ou de episodios'))
        self.sequencePathTextField.textChanged.connect(self.on_path_changed)
        self.sequencePathTextField.textChanged.connect(self.saveWindowPrefs)


        # Header
        self.hLayoutHeader1.addWidget(self.planilhaPathLabel)
        self.hLayoutHeader1.addWidget(self.sheetPathTextField)
        self.hLayoutHeader1.addWidget(self.planilhaPathBrowseButton)

        self.hLayoutHeader2.addWidget(self.referencePathLabel)
        self.hLayoutHeader2.addWidget(self.referencePathTextField)
        self.hLayoutHeader2.addWidget(self.referencePathBrowseButton)

        self.hLayoutHeader3.addWidget(self.audioPathLabel)
        self.hLayoutHeader3.addWidget(self.audioPathTextField)
        self.hLayoutHeader3.addWidget(self.audioPathBrowseButton)

        self.hLayoutHeader4.addWidget(self.sequencePathLabel)
        self.hLayoutHeader4.addWidget(self.sequencePathTextField)
        self.hLayoutHeader4.addWidget(self.sequencePathBrowseButton)



        self.bottomLineLayout = QHBoxLayout()
        # self.bottomLineLayout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.projectTypeLabel = QLabel("Type:")
        self.projectTypeLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.projectTypeList = QComboBox()
        self.projectTypeList.addItems(['Series', 'Feature Movie', 'Short Movie'])
        self.projectTypeList.currentTextChanged.connect(self.on_type_text_changed)
        self.projectTypeList.currentTextChanged.connect(self.refreshShotList)
        self.projectTypeList.currentTextChanged.connect(self.saveWindowPrefs)
        self.projectTypeList.setCurrentText(self.projectTypeString)
        self.projectTypeList.setFixedWidth(120)


        self.projectInitialsLabel = QLabel("Project initials:")
        self.projectInitialsLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.projectInitialsTextField = QLineEdit()
        self.projectInitialsTextField.setFixedWidth(60)
        self.projectInitialsTextField.setText(self.projectInitialsString)
        self.projectInitialsTextField.textChanged.connect(self.on_initials_text_changed)
        self.projectInitialsTextField.textChanged.connect(self.saveWindowPrefs)


        self.episodeLabel = QLabel("Episode number:")
        self.episodeLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.episodeTextField = QLineEdit()
        self.episodeTextField.setFixedWidth(50)
        self.episodeTextField.setText("101")



        self.checkboxImportReferences = QCheckBox("Import Refs")
        self.checkboxImportReferences.setChecked(True)
        self.checkboxImportReferences.stateChanged.connect(lambda state: self.setReferencePathVisibility(state))
        self.setReferencePathVisibility(True)

        self.checkboxImportAudio = QCheckBox("Import Audio")
        self.checkboxImportAudio.setChecked(True)
        self.checkboxImportAudio.stateChanged.connect(lambda state: self.setAudioPathVisibility(state))
        self.setAudioPathVisibility(True)

        self.checkboxLockCameraProperties = QCheckBox("Lock camera properties")
        self.checkboxLockCameraProperties.setChecked(True)


        self.projectStructureLabel = QLabel("Structure:")
        self.projectStructureList = QComboBox()
        self.projectStructureList.addItems(['By file type (VMB)', 'By shots (TAF)'])
        self.projectStructureList.currentTextChanged.connect(self.on_structure_text_changed)
        self.projectStructureList.currentTextChanged.connect(self.saveWindowPrefs)
        self.projectStructureList.setCurrentText(self.projectStructureString)
        self.setSequencePathVisibility(True)


        self.bottomLineLayout.addWidget(self.projectInitialsLabel)
        self.bottomLineLayout.addWidget(self.projectInitialsTextField)
        self.bottomLineLayout.addSpacing(20)

        self.bottomLineLayout.addWidget(self.episodeLabel)
        self.bottomLineLayout.addWidget(self.episodeTextField)
        self.bottomLineLayout.addSpacing(20)

        self.startLabel = QLabel("From shot:")
        self.startLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        # self.bottomLineLayout.setFixedWidth(40)
        self.startText = QLineEdit()
        self.startText.setFixedWidth(70)
        self.startText.setText("10")
        self.bottomLineLayout.addWidget(self.startLabel, 0)
        self.bottomLineLayout.addWidget(self.startText, 0)
        self.bottomLineLayout.addSpacing(10)

        self.endLabel = QLabel("To shot:")
        self.endLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        # self.bottomLineLayout.setFixedWidth(40)
        self.endText = QLineEdit()
        self.endText.setFixedWidth(70)
        self.endText.setText("50")
        self.bottomLineLayout.addWidget(self.endLabel, 0)
        self.bottomLineLayout.addWidget(self.endText, 0)


        # Definicao de atualizar a lista dos shots cada vez que algum texto importante se altera
        QObject.connect(self.projectInitialsTextField, SIGNAL("textEdited(const QString&)"), self.refreshShotList)
        QObject.connect(self.episodeTextField, SIGNAL("textEdited(const QString&)"), self.refreshShotList)
        QObject.connect(self.startText, SIGNAL("textEdited(const QString&)"), self.refreshShotList)
        QObject.connect(self.endText, SIGNAL("textEdited(const QString&)"), self.refreshShotList)


        self.hBtnLayout = QHBoxLayout()
        self.execBtn = QPushButton("Create")
        self.execBtn.clicked.connect(self.createShots)
        self.cancelBtn = QPushButton("Cancel")
        self.cancelBtn.clicked.connect(self.window.close)
        self.hBtnLayout.addWidget(self.execBtn)
        self.hBtnLayout.addWidget(self.cancelBtn)


        # TODO: revisitar o sistema de presets
        # self.cameraLabel = QLabel(" Camera preset: ")
        # self.filterBoxCameras = QComboBox()
        # for item in ["defaultCam"]:
        #     self.filterBoxCameras.addItem(item)

        self.topLineLayout = QHBoxLayout()
        self.topLineLayout.addWidget(self.checkboxImportReferences, 1)
        self.topLineLayout.addWidget(self.checkboxImportAudio, 1)
        self.topLineLayout.addWidget(self.checkboxLockCameraProperties, 2)
        self.topLineLayout.addWidget(self.projectStructureLabel, 0)
        self.topLineLayout.addWidget(self.projectStructureList, 0)
        self.topLineLayout.addWidget(self.projectTypeLabel, 0)
        self.topLineLayout.addWidget(self.projectTypeList, 2)
        # self.topLineLayout.addWidget(self.cameraLabel, 0)
        # self.topLineLayout.addWidget(self.filterBoxCameras, 0)

        self.widget = QWidget()
        self.sub_layout = QVBoxLayout()
        self.sub_layout.setAlignment(Qt.AlignTop)

        self.widget.setLayout(self.sub_layout)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.allLayout = QHBoxLayout()
        self.allChk = QCheckBox("All")
        self.allChk.setChecked(True)
        self.allLayout.addWidget(self.allChk)
        self.sub_layout.addLayout(self.allLayout)
        self.allChk.stateChanged.connect(self.onAllCheckChange)

        self.vLayout.addLayout(self.topLineLayout)

        self.vLayout.addLayout(self.hLayoutHeader1)
        self.vLayout.addLayout(self.hLayoutHeader2)
        self.vLayout.addLayout(self.hLayoutHeader3)
        self.vLayout.addLayout(self.hLayoutHeader4)

        self.vLayout.addLayout(self.bottomLineLayout)
        self.vLayout.addWidget(self.scroll)
        self.vLayout.addLayout(self.hBtnLayout)
        self.window.setLayout(self.vLayout)

        self.listOfShots = {}

        if self.is_this_structure('By file type'):
            self.setSequencePathVisibility(False)


    def select_folder(self, textField, hint):
        dialog = QFileDialog()
        folderPath = dialog.getExistingDirectory(None, hint)
        if folderPath:
            textField.setText(folderPath)


    def select_file(self, textField, hint):
        dialog = QFileDialog()
        filePath = str(dialog.getOpenFileName(None, hint)[0])
        filePath = filePath.replace('\\', '/')
        if filePath:
            textField.setText(filePath)


    def on_initials_text_changed(self, text):
        self.projectInitialsString = text

    def on_path_changed(self, _ ):
        self.sheetPathString = self.sheetPathTextField.text()
        self.referencePathString = self.referencePathTextField.text()
        self.audioPathString = self.audioPathTextField.text()
        self.sequencePathString = self.sequencePathTextField.text()

    def on_structure_text_changed(self, text):
        self.projectStructureString = text
        if 'By shots' in text:
            self.setSequencePathVisibility(True)
            self.setAudioPathVisibility(False)

        if 'By file type' in text:
            self.setSequencePathVisibility(False)
            self.setAudioPathVisibility(True)


    def on_type_text_changed(self, text ):

        self.projectTypeString = text

        try:
            if self.is_series():
                self.sequencePathLabel.setText('Episodes path:')
                self.episodeLabel.setText('Episode number:')
                self.episodeLabel.show()
                self.episodeTextField.show()
                self.episodeLabel.setDisabled(False)
                self.episodeTextField.setDisabled(False)

            if self.is_feature_movie():
                self.sequencePathLabel.setText('Sequences path:')
                self.episodeLabel.setText('Sequence number:')
                self.episodeLabel.show()
                self.episodeTextField.show()
                self.episodeLabel.setDisabled(False)
                self.episodeTextField.setDisabled(False)

            if self.is_short_movie():
                self.sequencePathLabel.setText('Shots path:')
                self.episodeLabel.setDisabled(True)
                self.episodeTextField.setDisabled(True)

        except AttributeError:
            print('Algum atributo ainda nao foi definido')



    def is_this_structure(self, structure):
        if structure.lower() in self.projectStructureString.lower():
            return True
        return False


    def is_series(self):
        if self.projectTypeList.currentText() == 'Series':
            return True
        return False

    def is_feature_movie(self):
        if self.projectTypeList.currentText() == 'Feature Movie':
            return True
        return False

    def is_short_movie(self):
        if self.projectTypeList.currentText() == 'Short Movie':
            return True
        return False


    def setReferencePathVisibility(self, visible):
        if visible:
            self.referencePathLabel.show()
            self.referencePathTextField.show()
            self.referencePathBrowseButton.show()
        else:
            self.referencePathLabel.hide()
            self.referencePathTextField.hide()
            self.referencePathBrowseButton.hide()


    def setAudioPathVisibility(self, visible):
        if visible and self.is_this_structure('By file type'):
            print('Structure: ' + self.projectStructureString)
            self.audioPathLabel.show()
            self.audioPathTextField.show()
            self.audioPathBrowseButton.show()
        else:
            print('Structure: ' + self.projectStructureString)
            self.audioPathLabel.hide()
            self.audioPathTextField.hide()
            self.audioPathBrowseButton.hide()


    def setSequencePathVisibility(self, visible):
        if visible:
            self.sequencePathLabel.show()
            self.sequencePathTextField.show()
            self.sequencePathBrowseButton.show()
        else:
            self.sequencePathLabel.hide()
            self.sequencePathTextField.hide()
            self.sequencePathBrowseButton.hide()


    def saveWindowPrefs(self):
        print("Save Window Prefs")
        data = {}
        data['presets'] = []

        data['presets'].append({
            'planilhaPath': self.sheetPathTextField.text(),
            'referencePath': self.referencePathTextField.text(),
            'audioPath': self.audioPathTextField.text(),
            'sequencePath': self.sequencePathTextField.text(),
            'projectStructure': self.projectStructureString,
            'projectType': self.projectTypeString,
            'projectInitials': self.projectInitialsString
        })

        jsonFilePath = os.path.dirname(__file__) + os.path.sep + "resources/sequence_gen_prefs.json"

        with open(jsonFilePath, 'w') as outfile:
            json.dump(data, outfile, indent=2)


    def loadWindowPrefs(self):
        print("Load Window Prefs")

        jsonFilePath = os.path.dirname(__file__) + os.path.sep + "resources/sequence_gen_prefs.json"
        if not os.path.exists(jsonFilePath):
            data = {}
            data['presets'] = []

            # data['presets'].append({
            #     'planilhaPath': "Type excel path file...",
            #     'referencePath': "Type reference path file...",
            #     'audioPath': "Type audio path file..."
            # })

            with open(jsonFilePath, 'w') as outfile:
                json.dump(data, outfile)

        print(jsonFilePath)
        with open(jsonFilePath) as json_file:
            data = json.load(json_file)
            for p in data['presets']:
                self.sheetPathString = p['planilhaPath']
                self.referencePathString = p['referencePath']
                self.audioPathString = p['audioPath']
                self.sequencePathString = p['sequencePath']
                self.projectStructureString = p['projectStructure']
                self.projectTypeString = p['projectType']
                self.projectInitialsString = p['projectInitials']

        print("Dados Paths")
        print(self.sheetPathString)
        print(self.referencePathString)
        print(self.audioPathString)
        print(self.sequencePathString)
        print(self.projectStructureString)



    def onAllCheckChange(self):
        value = self.allChk.isChecked()
        for shot in self.listOfShots.keys():
            self.listOfShots[shot].setChecked(value)
        return


    def refreshShotList(self):
        try:
            self.cleanList()
        except AttributeError:
            return

        start_shot_number = filter(str.isdigit, str(self.startText.text()))
        end_shot_number = filter(str.isdigit, str(self.endText.text()))
        initials = self.projectInitialsTextField.text()
        prefix = ""

        if start_shot_number and end_shot_number and (int(end_shot_number) >= int(start_shot_number)):
            episode = self.episodeTextField.text().zfill(3)
            prefix = ""

            episode = episode.upper()

            for i in range(int(start_shot_number), int(end_shot_number) + 1, 10):
                shotName = self.createShotName(prefix + episode, str(i).zfill(4), initials=initials)
                if not shotName in self.listOfShots.keys():
                    self.sub_layout.addLayout(self.addShot(shotName))


    def cleanList(self):
        for widget in self.listOfShots.keys():
            self.listOfShots[widget].deleteLater()
        self.listOfShots = {}


    def addShot(self, shot_name):
        self.bottomLineLayout = QHBoxLayout()
        shot = QCheckBox(shot_name)
        shot.setChecked(True)
        self.listOfShots[shot_name] = shot
        self.bottomLineLayout.addWidget(shot)
        return self.bottomLineLayout

    def getEpisodeLogFromExcelSheets(self, episode):
        """Get the frame range information for the shots"""

        excelFile = pylightxl.readxl(str(self.sheetPathString))

        if excelFile:
            sheets = excelFile.ws_names
            frameSheetName = None

            for sheet in sheets:
                if "_ShotFrames" in sheet:
                    frameSheetName = sheet

            if frameSheetName == None:
                print('frameSheetName esta vazio')
                return None

            frameSheet = excelFile.ws(frameSheetName)

            # Print all values, iterating through rows and columns
            num_cols = frameSheet.maxcol

            episodeColNames = []
            for row_idx in range(1, frameSheet.maxrow):
                episodeColNames.append(frameSheet.index(row=row_idx, col=1))
            episodeColNames.remove("episode_name")

            episodeColNames = unique(episodeColNames)
            #episodeColNames = list(episodeColNames)
            print(episode)
            print(episodeColNames)

            for ep in episodeColNames:
                if episode in ep:
                    print(episode)
                    return episode

            return None



    def readMetadataFromExcelSheets(self):
        excelFile = pylightxl.readxl(str(self.sheetPathString))
        if excelFile:
            sheets = excelFile.ws_names
            frameSheetName = None

            for sheet in sheets:
                if "_ShotFrames" in sheet:
                    frameSheetName = sheet

            if frameSheetName == None:
                return None

            frameSheet = excelFile.ws(frameSheetName)

            shots = {}

            num_cols = frameSheet.maxcol
            for row_idx in range(2, frameSheet.maxrow + 1):
                shotNumber = str(int(frameSheet.index(row=row_idx, col=2))).zfill(4)
                startFrame = int(frameSheet.index(row=row_idx, col=3))
                endFrame = int(frameSheet.index(row=row_idx, col=4))
                shots[shotNumber] = [startFrame, endFrame]

            return shots


    def getShotAudio(self, episodeName, shotNumber, audioFolder):

        if self.is_this_structure('By file type'):
            if self.projectInitialsString not in episodeName:
                episodeName = self.projectInitialsString + episodeName

            episodeAudioFolder = os.path.join(audioFolder, episodeName)

            if not os.path.exists(episodeAudioFolder):
                print("ERROR: Essa sequencia ou episodio nao existe: " + str(episodeAudioFolder))
                print('audioFolder: ' + str(audioFolder))
                print('episodeName: ' + str(episodeName))
                return None

            audioFiles = os.listdir(episodeAudioFolder)
            for file in audioFiles:
                filePath =  os.path.abspath(os.path.join(episodeAudioFolder, file))
                filePath = filePath.replace('\\', '/')
                if (episodeName in file) and (shotNumber in file) and os.path.isfile(filePath):
                    return filePath

            return None

        if self.is_this_structure('By shots'):
            sequencesPath = self.sequencePathString
            # taskList = os.listdir(os.path.join(sequencesPath, episodeName, shotNumber))
            # layoutTask = [x for x in taskList if 'layout' in x.lower()][0]
            audioVersions = glob.glob(os.path.abspath(
                os.path.join(sequencesPath, 'seq' + episodeName, 'sh' + shotNumber, 'audio', '*')
                ))
            audioVersions.sort()
            print('audio versions:')
            print(audioVersions)
            filePath = audioVersions[-1] # pega a versao mais recente dos arquivos
            filePath = filePath.replace('\\', '/')
            return filePath


    def createShotName(self, episode, shot, initials):

        if self.is_series():
            shotName = initials + episode.zfill(3) + "_sh" + shot.zfill(4) + "_layout"

        if self.is_feature_movie():
            shotName = initials + '_seq' + episode.zfill(3) + "_sh" + shot.zfill(4) + "_layout"

        if self.is_short_movie():
            shotName = initials + "_sh" + shot.zfill(4) + "_layout"

        if shotName:
            return shotName

        else:
            print('ERROR: PROJECT TYPE NOT DEFINED')


    def createDefaultCamera(self, shotNumber):

        camLockCheckedStatus = self.checkboxLockCameraProperties.isChecked()

        camera = cmds.camera()
        cmds.setAttr(camera[0] + ".scaleX", 1, l=camLockCheckedStatus)
        cmds.setAttr(camera[0] + ".scaleY", 1, l=camLockCheckedStatus)
        cmds.setAttr(camera[0] + ".scaleZ", 1, l=camLockCheckedStatus)
        cmds.setAttr(camera[1] + ".displayResolution", 1)
        cmds.setAttr(camera[1] + ".displayGateMask", 1)
        cmds.setAttr(camera[1] + ".displaySafeAction", 1)
        cmds.setAttr(camera[1] + ".displaySafeTitle", 1)
        cmds.setAttr(camera[1] + ".overscan", 1, l=camLockCheckedStatus)

        # 35mm Academy
        cmds.setAttr(camera[1] + ".horizontalFilmAperture", 1.121)
        cmds.setAttr(camera[1] + ".verticalFilmAperture", 0.630)
        cmds.setAttr(camera[1] + ".focalLength", 50)
        cmds.setAttr(camera[1] + ".filmFit", 3)

        cmds.setAttr(camera[1] + ".nearClipPlane", l=camLockCheckedStatus)
        cmds.setAttr(camera[1] + ".cameraAperture", l=camLockCheckedStatus)
        cmds.setAttr(camera[1] + ".lensSqueezeRatio", l=camLockCheckedStatus)
        cmds.setAttr(camera[1] + ".cameraScale", l=camLockCheckedStatus)
        cmds.setAttr(camera[1] + ".filmFit", l=camLockCheckedStatus)

        camera = cmds.rename(camera[0], "CAM_SH" + shotNumber)
        cameraGroup = cmds.group(name = camera + "_grp", empty = True)
        cmds.parent(camera, cameraGroup, shape = True)
        return camera


    def createShot(self, shotNumber, start, end, audio, episode, initials):
        print("")
        print("formatNumber: " + str(shotNumber))
        print("start: " + str(start))
        print("end: " + str(end))
        print("audio: " + str(audio))
        print("episode: " + str(episode))

        camera = self.createDefaultCamera(shotNumber)
        if not camera:
            return

        shotName = self.createShotName(episode, shotNumber, initials=initials)
        if cmds.objExists(shotName):
            return

        cmds.sequenceManager(currentTime = start)
        if audio != None:
            shotName = cmds.shot(shotName, startTime = start, endTime = end, sequenceStartTime = start, sequenceEndTime = end, currentCamera = camera, track = 1, lock = True)
            cmds.sequenceManager(addSequencerAudio = audio)
        else:
            shotName = cmds.shot(shotName, startTime = start, endTime = end, sequenceStartTime = start, sequenceEndTime = end, currentCamera = camera, track = 1, lock = True)



    def searchAssetsFromExcelSheets(self, episode):

        excelFile = pylightxl.readxl(str(self.sheetPathString))
        if excelFile:
            sheets = excelFile.ws_names
            assetSheetName = None

            for sheet in sheets:
                if "_AssetRefs" in sheet:
                    assetSheetName = sheet

            if assetSheetName == None:
                return None

            assetSheet = excelFile.ws(assetSheetName)
            shotAssets = {}
            assetList = []

            num_cols = assetSheet.maxcol
            num_rows = assetSheet.maxrow

            for col_idx in range(1, assetSheet.maxcol + 1):
                shotNumber = str(int(assetSheet.index(row=1, col=col_idx))).zfill(4)
                shotNumber = shotNumber.decode("utf-8")
                if episode == shotNumber:
                    print("Shot Name: "  + shotNumber)
                    for row_idx in range(2, assetSheet.maxrow):
                        assetName = assetSheet.index(row=row_idx, col=col_idx)
                        if assetName != "":
                            assetList.append(assetName)
                    shotAssets[shotNumber] = assetList

            return assetList
        return None


    def loadAssetReferences(self, assetList):

        print("Asset List: " + str(assetList))

        referenceDirectory = self.referencePathString
        if not referenceDirectory.endswith(os.path.sep):
            referenceDirectory += os.path.sep
        print("Reference Path" + referenceDirectory)

        for assetName in assetList:
            folders = os.listdir(referenceDirectory)

            for folder in folders:
                assetPath = glob.glob(referenceDirectory + "*" + folder + os.path.sep + assetName + "*")
                if assetPath:
                    print(assetPath)
                    if len(assetName.split("_")) > 1:
                        fAsset = assetName.split("_")[1]
                    else:
                        fAsset = assetName

                    cmds.file(assetPath, namespace = fAsset, referenceNode = fAsset + "RN", reference = True)

        return


    def createShots(self):

        initials = self.projectInitialsTextField.text()
        episodeNumber = self.episodeTextField.text().zfill(3)
        print("Episode: " + episodeNumber)

        episode = self.getEpisodeLogFromExcelSheets(episodeNumber)
        if not episode:
            print("ERROR: Episode {1} not found!".format(episodeNumber))
            return

        shots = self.readMetadataFromExcelSheets()
        print("Shots: " + str(shots))


        if not shots:
            print("ERROR: shots not found in {1}".format(episode))
            return


        # Shot information
        for shot in sorted(shots, key = shots.__getitem__):
            fShot = filter(str.isdigit, str(shot)).zfill(4)
            shotName = self.createShotName(episode, fShot, initials=initials)

            if shotName in self.listOfShots.keys():
                frameStart = shots[shot][0]
                frameEnd = shots[shot][1]

                if self.listOfShots[shotName].isChecked():
                    audio = None
                    if self.checkboxImportAudio.isChecked():
                        audioFolder = os.path.abspath(self.audioPathTextField.text())
                        audio = self.getShotAudio(episode, fShot, audioFolder)

                    self.createShot(fShot, frameStart, frameEnd, audio, episode, initials=initials)


        # Import references to scene
        assetList = []
        for shot in sorted(shots, key = shots.__getitem__):
            fShot = filter(str.isdigit, str(shot)).zfill(4)
            shotName = self.createShotName(episode, fShot, initials)
            if shotName in self.listOfShots.keys():
                if self.checkboxImportReferences.isChecked():
                    assetList.extend(self.searchAssetsFromExcelSheets(fShot))

        print(assetList)
        assetList = unique(assetList)
        self.loadAssetReferences(assetList)

        sequences = cmds.sequenceManager(listSequencerAudio = True)
        if not sequences:
            print('Audio sequences not found')
            return

        cmds.lookThru('persp')
        cmds.select(ado=True)

        try:
            cmds.select('*domo*', d=True)
            cmds.select('*:Dome*', d=True)
        except ValueError:
            pass

        cmds.viewFit('persp')
        cmds.select(cl=True)

        self.window.close()


    def show(self):
        self.window.show()
        self.episodeTextField.setFocus()
        self.refreshShotList()


def run():
    program = SequenceGen()
    program.show()

    print("\nprojectType: " + str(program.projectTypeString))
    print("projectInitials: " + str(program.projectInitialsString))
    print("projectStructure: " + str(program.projectStructureString))
    print("audioPath: " + str(program.audioPathString))
    print("sheetPath: " + str(program.sheetPathString))
    print("sequencePath: " + str(program.sequencePathString))
    print("referencePath: " + str(program.referencePathString))


run()
