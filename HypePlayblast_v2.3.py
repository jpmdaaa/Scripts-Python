import maya.cmds as mc
import os.path as path
import maya.mel as mel
import os
import shutil


#Return a list with all cameras except maya's default ones(persp,front,etc...)
def get_all_dev_cameras():

    all_cameras = mc.listCameras()
    developer_cameras = []

    for c in all_cameras:

        if c == 'front':

            continue

        elif c == 'persp':

            continue

        elif c == 'side':

            continue

        elif c == 'top':

            continue

        else:
            developer_cameras.append(c)

    return developer_cameras

# get all shots from sequance manager
def getAllShots():
    return mc.sequenceManager(listShots=True)

# Get Camera used by a shot
def getShotsCamera(mshot):
    print mshot
    cam = mc.shot(mshot,q=True,currentCamera=True)
   
    print cam
    return cam

def ToogleHUDForPlayblast(shotFullName='',toogle=True):
    #HUDs to set 'HUDCameraName', 'HUDCurrentFrame', 'HUDFocalLength'
    #delete all HUDs sections and blocks that will be used
    for i in range(10):
        for j in range(100):
                mc.headsUpDisplay(rp=(i,j))

    print 'is visible: ' + str(mc.headsUpDisplay(q = True,lv = True))
    fileName = (path.split(mc.file( q=True, sn=True))[1]).split(".")[0]
    print fileName
    fileName = fileName.lower()
    list_of_components = fileName.split("_")
    split_flag = mc.checkBox('splitPlayblastInShots',q=True,value=True)

    print "this is" + str(list_of_components)
    #print list_of_components

    scene_info = ""

    if split_flag:

        if getAllShots() != None:
            print 'there is a shot'
            scene_info = shotFullName

        else:
            print 'not shot'
            for c in list_of_components:

                c_low = c.lower()
                print c_low

                if "ep" in c_low:

                    scene_info = scene_info + c + "_"

                elif "seq" in c_low:

                    scene_info = scene_info + c + "_"

                elif "shot" in c_low:

                    scene_info = scene_info + c + "_"

                elif ("s" in c_low) and (len(c_low) == 4):

                    scene_info = scene_info + c + "_"

                elif 'lay' in c_low:

                    scene_info = scene_info + c + "_"

                elif 'anim' in c_low:

                    scene_info = scene_info + c + "_"

                elif 'approved' in c_low:

                    scene_info = scene_info + c

                elif "-" in c_low:

                    if not split_flag:

                        scene_info = scene_info + c
    else:

        for c in list_of_components:

            c_low = c.lower()
            print c_low

            if "ep" in c_low:

                scene_info = scene_info + c + "_"

            elif "seq" in c_low:

                scene_info = scene_info + c + "_"

            elif "shot" in c_low:

                scene_info = scene_info + c + "_"

            elif ("s" in c_low) and (len(c_low) == 4):

                scene_info = scene_info + c + "_"

            elif 'lay' in c_low:

                scene_info = scene_info + c + "_"

            elif 'anim' in c_low:

                scene_info = scene_info + c + "_"

            elif 'approved' in c_low:

                scene_info = scene_info + c

            elif "-" in c_low:

                if not split_flag:

                    scene_info = scene_info + c
    print 'scene info:' + scene_info

    #print scene_info

    # Show Camera Names
    # delete HUD if exists
    if mc.headsUpDisplay( 'HUDCameraName_Custom', exists=True ) and toogle:
        mc.headsUpDisplay( 'HUDCameraName_Custom', remove=True )

    # Create HUD
    if toogle:
        mc.headsUpDisplay('HUDCameraName_Custom',s=7,b=0, ba='center',pre='cameraNames',labelFontSize= 'large',dataFontSize = 'large',visible=True, allowOverlap=True)
        #print mc.headsUpDisplay('HUDCameraName_Custom',q = True,pre=True)
    print 'hud visible: ' + str(mc.headsUpDisplay('HUDCameraName_Custom',q = True,lv = True))
    
    # delete HUD if exists
    if mc.headsUpDisplay( 'HUDCameraName_Custom', exists=True ) and not toogle:
        mc.headsUpDisplay( 'HUDCameraName_Custom', remove=True )

    # Show Curret Frame
    def currentFrame():
        minTime = mc.playbackOptions(q = True, min = True)
        maxTime = mc.playbackOptions(q = True, max = True)
        currentFrame = mc.currentTime(q = True)
        displayTime = '%d ( %d / %d )'% (currentFrame,minTime ,maxTime)
        return displayTime

    # Delete Current Frame HUD if has One
    if mc.headsUpDisplay( 'HUDCurrentFrame_Custom', exists=True ) and toogle:
        mc.headsUpDisplay( 'HUDCurrentFrame_Custom', remove=True )

    # Create a current frame callback to display the current frame
    if toogle:
        mc.headsUpDisplay( 'HUDCurrentFrame_Custom',
                section=9,
                block=0,#mc.headsUpDisplay( nextFreeBlock=0 ),
                blockSize='small',
                label='Current Frame:',
                labelFontSize = 'large',
                dataFontSize = 'large',
                command = currentFrame,
                attachToRefresh=True,
                allowOverlap=True,
                visible=True
        )

    # Delete Current Frame HUD if has One
    if mc.headsUpDisplay( 'HUDCurrentFrame_Custom', exists=True ) and not toogle:
        mc.headsUpDisplay( 'HUDCurrentFrame_Custom', remove=True )


    # Show Focal Length

    # delete focal length HUD
    if mc.headsUpDisplay( 'HUDFocalLength_Custom', exists=True ) and toogle:
        mc.headsUpDisplay( 'HUDFocalLength_Custom', remove=True )

    if toogle:
        mc.headsUpDisplay(
                            'HUDFocalLength_Custom',
                            section=9,
                            block=1,
                            blockSize="small",
                            labelFontSize="large",
                    		dataFontSize="large",
                    		label="Focal Length:",
                    		preset="focalLength",
                    		visible=True,
                    		allowOverlap=True
        )

    # delete focal length HUD
    if mc.headsUpDisplay( 'HUDFocalLength_Custom', exists=True ) and not toogle:
        mc.headsUpDisplay( 'HUDFocalLength_Custom', remove=True )

    # Show animator name HUD

    # delete animator name HUD
    if mc.headsUpDisplay( 'HUDAnimatorName_Custom', exists=True ) and toogle:
        mc.headsUpDisplay( 'HUDAnimatorName_Custom', remove=True )

    if toogle:
        mc.headsUpDisplay(
            'HUDAnimatorName_Custom',
            section=5,
            block=0,
            blockSize="small",
            labelFontSize="large",
            dataFontSize="large",
            label="Animator Name: " + mc.textField('animatorName',q=True,tx=True),
            visible=True,
            allowOverlap=True
        )

    # delete animator name HUD
    if mc.headsUpDisplay( 'HUDAnimatorName_Custom', exists=True ) and not toogle:
        mc.headsUpDisplay( 'HUDAnimatorName_Custom', remove=True )

    # delete animator name HUD
    if mc.headsUpDisplay( 'HUDSequenceName_Custom', exists=True ) and toogle:
        mc.headsUpDisplay( 'HUDSequenceName_Custom', remove=True )

    if toogle:
        mc.headsUpDisplay(
            'HUDSequenceName_Custom',
            section=2,
            block=2,
            blockSize="small",
            labelFontSize="large",
            dataFontSize="large",
            label="Scene info: " + scene_info,
            visible=True,
            allowOverlap=True
        )

    # delete animator name HUD
    if mc.headsUpDisplay( 'HUDSequenceName_Custom', exists=True ) and not toogle:
        mc.headsUpDisplay( 'HUDSequenceName_Custom', remove=True )

    # Show status HUD

    # delete animator name HUD
    if mc.headsUpDisplay( 'HUDStatus_Custom', exists=True ) and toogle:
        mc.headsUpDisplay( 'HUDStatus_Custom', remove=True )

    if toogle:
        mc.headsUpDisplay(
            'HUDStatus_Custom',
            section=5,
            block=1,
            blockSize="small",
            labelFontSize="large",
            dataFontSize="large",
            label="Status: " + mc.optionMenu('statusType',q=True,v=True),
            visible=True,
            allowOverlap=True
        )

    # delete animator name HUD
    if mc.headsUpDisplay( 'HUDStatus_Custom', exists=True ) and not toogle:
        mc.headsUpDisplay( 'HUDStatus_Custom', remove=True )

def doPlayBlastIWinUI():
    if mc.window('doPlayBlastWin',exists=True):
        mc.deleteUI('doPlayBlastWin')

    win = mc.window('doPlayBlastWin', t='Hype Playblast v2.2', s=False)
    win = cmds.window( win, edit=True, widthHeight=(268, 220) )
    mc.columnLayout('doPlayBlastMainLay')

    # new ROW
    # Set movie file name
    mc.rowColumnLayout( parent='doPlayBlastMainLay', numberOfColumns=3, columnWidth=[(1, 45),(2, 200), (3,20)] )

    fileName = (path.split(mc.file( q=True, sn=True))[1]).split(".")[0]

    mc.text(l="Name:")
    mc.textField('nameDoPlayTxtFld', tx=fileName)
    mc.popupMenu( 'fillPlayMenu', parent='nameDoPlayTxtFld' )

    mc.button(l="+", c="grabNameDoPlay()")

    # new row
    # Split playblast into shots
    mc.rowColumnLayout( parent='doPlayBlastMainLay', numberOfColumns=2, columnWidth=[(1,128),(2,255)] )
    mc.checkBox('splitPlayblastInShots', l="Split Playblast Shots:")
    mc.checkBox('setPlayblastDirectory', l="Set Playblast Dir:")

    # new ROW
    # animator name
    mc.rowColumnLayout( parent='doPlayBlastMainLay', numberOfColumns=2, columnWidth=[(1, 90),(2, 168)] )
    mc.text(l="Animator Name:")
    mc.textField('animatorName')

    # new ROW
    # animator name
    mc.rowColumnLayout( parent='doPlayBlastMainLay', numberOfColumns=2, columnWidth=[(1, 90),(2, 168)] )
    #mc.text(l="Status:")
    mc.optionMenu('statusType',w = 134 ,label = 'Status:')
    options = ['Blocking','Polish','WIP','FIX']
    for opt in options:
        mc.menuItem( label=opt )

    mc.scrollLayout('playblast_scroll_area', parent = 'doPlayBlastMainLay', horizontalScrollBarThickness = 16, verticalScrollBarThickness = 16,bgc = [0.4,0.4,0.4],width = 510,height = 100)
    mc.columnLayout('playblast_inner_layer',parent = 'playblast_scroll_area')
    mc.rowColumnLayout( parent = 'playblast_inner_layer', numberOfColumns = 2,columnWidth = [(1, 150),(2, 100)])
    listOfSounds = getSoundList()

    if listOfSounds:
        for sound in listOfSounds:

            mc.rowColumnLayout( parent = 'playblast_inner_layer', numberOfColumns = 1)
            if len(listOfSounds) == 1:
                mc.checkBox(str(sound)+ '_checkbox',label = str(sound), align = 'center',v = True)
            else:
                mc.checkBox(str(sound)+ '_checkbox',label = str(sound), align = 'center')

    # new ROW
    # Interactive buttons
    mc.rowColumnLayout( parent='doPlayBlastMainLay', numberOfColumns=2, columnWidth=[(1, 135),(2, 135)] )

    mc.button(l="Make", c="makeDoPlay()")
    mc.button('showDoPlayBlastBtn', l="Show", c="showDoPlay()")
    createSnowAnimPopUpDP( 'showDoPlayBlastBtn', 'Folder' )


    mc.showWindow(win)

    mc.scriptJob( e=["SceneOpened","grabNameDoPlay()"], parent='doPlayBlastWin')
    mc.scriptJob( ct=["writingFile","grabNameDoPlay()"], parent='doPlayBlastWin')

#---------------------------------------------------------------------------------------
def createSnowAnimPopUpDP( buttonName, animName ):
    pathFile = path.split(mc.file( q=True, sn=True))[0]
    mc.popupMenu( parent=buttonName )
    if animName == 'Folder':
        mc.menuItem( l="Open - "+animName, c="makeOpenFolderAnimSnowDP()")
    else:
        mc.menuItem( l="Open - "+animName, c="makeOpenAnimSnowDP('" +pathFile+ "' )")


def makeOpenFolderAnimSnowDP():
    pathFile = path.split(mc.file( q=True, sn=True))[0]
    folderPath =  os.path.dirname(pathFile)
    fileName = os.path.basename(pathFile)
    os.chdir( folderPath )
    os.startfile( fileName )


def makeOpenAnimSnowDP( path ):
    folderPath =  os.path.dirname(path)
    fileName = os.path.basename(path)
    os.chdir( folderPath )
    os.startfile( fileName )

#---------------------------------------------------------------------------------------------
def grabNameDoPlay():
    fileName = (path.split(mc.file( q=True, sn=True))[1]).split(".")[0]
    mc.textField('nameDoPlayTxtFld', e=True, tx=fileName)
    fillDoPlay()


#---------------------------------------------------------------------------------------------
# Try to find sound nodes from the camera sequencer or as a independent node.
# returns a list of sound names(string) if they exist,otherwise returns None-type.
def getSoundList():

    sequencerNodeName = mc.sequenceManager(q=True,node=True)

    if mc.sequenceManager(lsa=sequencerNodeName):
        return mc.sequenceManager(lsa=sequencerNodeName)
    elif mc.ls(typ = "audio"):
        return mc.ls(typ = "audio")
    else:
        return None
#---------------------------------------------------------------------------------------------
def makeDoPlay():
    pathFile = path.split(mc.file( q=True, sn=True))[0]
    fileName = mc.textField('nameDoPlayTxtFld', q=True, tx=True)
    Clist = getAllShots()
    if Clist != None:

        #For each shot,sets basic parameters
        for cl in Clist:

            cam = getShotsCamera(cl)
            print "i'm here"
            if cam == None:
                continue
            mc.camera(cam,e=True,dgm= False,dr=False,ovr=1.0)

        # split playblast into shots
        splitPlayblastInShots = mc.checkBox('splitPlayblastInShots', q=True, value=True)
        setPlayblastDir = mc.checkBox('setPlayblastDirectory', q=True, value=True)

        if(setPlayblastDir):
            path_dir = mc.fileDialog2(cap = "Choose path to save the movie",fm = 3)[0]+'/'
            print path_dir

        check=False
        print pathFile+"/"+fileName+".avi"
        try:
            os.remove(pathFile+"/"+fileName+".avi")
        except:
            check=True
            print ">> playblast is already deleted.."

        if check:
            mc.menuItem(  parent='fillPlayMenu', label=fileName, c="mc.textField('nameDoPlayTxtFld', e=True, tx='"+fileName+"')" )
    	#get sound name

        #Get the sound node from somewhere.
        soundName = None
        if getSoundList():

            for sound in getSoundList():

                if mc.checkBox(str(sound)+ '_checkbox',q = True,ex = True) and mc.checkBox(str(sound)+ '_checkbox',q = True,v = True):
                    print str(sound) + ' was selected!'
                    soundName = sound
                    break

        aPlayBackSliderPython = maya.mel.eval('$tmpVar=$gPlayBackSlider')
        range = mc.timeControl( aPlayBackSliderPython, q=True, range=True )
        range = range.replace("\"","")
        rangeArr = range.split(":")
        strFrm = int(rangeArr[0])+0
        endFrm = int(rangeArr[1])+0

        if endFrm-strFrm == 1:
            startFrame = mc.playbackOptions( q=True, min=True )
            endFrame = mc.playbackOptions( q=True, max=True )
        else:
            startFrame = strFrm
            endFrame = endFrm

        # set resolution of final blast
        blastResolutionWidthHeight = (1280,720)

        # Show HUD 'camera names', 'current frame', 'focal length'

        # Create playblast
        if splitPlayblastInShots:
            # if a playblast for each camera shot
            allShots = getAllShots()
            # for each camera shot create a playblast
            for s in allShots:
                if getShotsCamera(s) == None:
                    continue

                # Show HUD 'camera names', 'current frame', 'focal length'
                ToogleHUDForPlayblast(s,toogle=True)
                # with each start and end frame
                shotStartFrame = mc.getAttr(s+".sequenceStartFrame")
                shotEndFrame = mc.getAttr(s+".sequenceEndFrame")
                cameraName = getShotsCamera(s)
                #File name of the in case of split playblast into shots.

                mov_buffer = s.split("_")

                print mov_buffer
                mov_name = ""
                for mb in mov_buffer:

                    if "lay" in mb or "anim" in mb:

                        mov_name += "anim"

                    elif "seq" not in mb:

                        mov_name += mb + "_"

                fileShotName = mov_name + '.mov'
                # set camera to look throu
                mc.lookThru(cameraName)
                # if is a shot playblas
                if(setPlayblastDir):
                    makePlayblast(shotStartFrame,shotEndFrame,fileShotName,soundName,blastResolutionWidthHeight,pathFile = path_dir)
                else:
                    makePlayblast(shotStartFrame,shotEndFrame,fileShotName,soundName,blastResolutionWidthHeight)
                # Hide HUD 'camera names', 'current frame', 'focal length'
                ToogleHUDForPlayblast(toogle=False)
        else:
            #when all in one sequence
            ToogleHUDForPlayblast(toogle=True)
            if(setPlayblastDir):
                makePlayblast(startFrame,endFrame,fileName,soundName,blastResolutionWidthHeight,pathFile=path_dir)
            else:
                # if is a full playblast
                makePlayblast(startFrame,endFrame,fileName,soundName,blastResolutionWidthHeight)

            # Hide HUD 'camera names', 'current frame', 'focal length'
            ToogleHUDForPlayblast(toogle=False)
    else:

        print 'No shot in sequencer manager!'
        cameras = get_all_dev_cameras()

        # split playblast into shots
        splitPlayblastInShots = mc.checkBox('splitPlayblastInShots', q=True, value=True)
        setPlayblastDir = mc.checkBox('setPlayblastDirectory', q=True, value=True)

        if splitPlayblastInShots:

            print 'There are no shots in the sequence manager! Only one playblast will be made.'

        if(setPlayblastDir):
            path_dir = mc.fileDialog2(cap = "Choose path to save the movie",fm = 3)[0]+'/'
            print path_dir

        check=False

        print pathFile+"/"+fileName+".avi"

        try:
            os.remove(pathFile+"/"+fileName+".avi")
        except:
            check=True
            print '>> playblast is already deleted..'

        if check:
            mc.menuItem(  parent='fillPlayMenu', label=fileName, c="mc.textField('nameDoPlayTxtFld', e=True, tx='"+fileName+"')" )

    	#get sound name.
        if mc.ls(typ="audio"):
            soundName = mc.ls(typ="audio")[0]
            print 'Soundname from scene:' + soundName
        else:
            soundName = None
            print 'No Soundname'

        aPlayBackSliderPython = maya.mel.eval('$tmpVar=$gPlayBackSlider')
        range = mc.timeControl( aPlayBackSliderPython, q=True, range=True )
        range = range.replace("\"","")
        rangeArr = range.split(":")
        strFrm = int(rangeArr[0])+0
        endFrm = int(rangeArr[1])+0

        if endFrm-strFrm == 1:
            startFrame = mc.playbackOptions( q=True, min=True )
            endFrame = mc.playbackOptions( q=True, max=True )
        else:
            startFrame = strFrm
            endFrame = endFrm

        # set resolution of final blast
        blastResolutionWidthHeight = (1280,720)

        if cameras == None:

            print 'No cameras in this project besides the default ones.'

        else:

            for c in cameras:

                mc.camera(c,e=True,dgm= False,dr=False,lt=True,ovr=1.0)

                mov_buffer = fileName.split("_")

                print mov_buffer
                mov_name = ""
                for mb in mov_buffer:

                    mb_lower = mb.lower()

                    if "lay" in mb_lower or "anim" in mb_lower:

                        mov_name += "anim"

                    elif "approved" in mb_lower:

                        continue

                    elif "seq" not in mb_lower:

                        mov_name += mb + "_"

                fileShotName = mov_name + '.mov'
                print fileShotName
                mc.lookThru(c)
                #when all in one sequence
                ToogleHUDForPlayblast(toogle=True)
                # if is a shot playblas
                if(setPlayblastDir):
                    makePlayblast(startFrame,endFrame,fileShotName,soundName,blastResolutionWidthHeight,pathFile = path_dir)
                else:
                    makePlayblast(startFrame,endFrame,fileShotName,soundName,blastResolutionWidthHeight)
                # Hide HUD 'camera names', 'current frame', 'focal length'
                ToogleHUDForPlayblast(toogle=False)



def makePlayblast(startFrame,endFrame,fileName,soundName,wh,pathFile=mc.workspace(q=True,fn=True)+'/movies/animation/' ):
    # if is a full playblast
    #pathFile = path.split(mc.file( q=True, sn=True))[0]
    fileT =  pathFile+"/"+fileName
    project = mc.workspace(q=True,fn=True)+'/'
    print fileT
    if soundName != None:
        mc.playblast(  format="qt", startTime= startFrame, endTime= endFrame, filename=pathFile+fileName, sound=soundName, forceOverwrite=True, showOrnaments=True, offScreen=True,  fp=0, percent=100, compression="H.264", quality=100, widthHeight=wh)
    else:
        mc.playblast(  format="qt", startTime= startFrame, endTime= endFrame, filename=pathFile+fileName, forceOverwrite=True, showOrnaments=True, offScreen=True,  fp=4, percent=100, compression="H.264", quality=100, widthHeight=wh)
    #lockCameraAttributes(mc.modelEditor( mc.getPanel(wf=True), q=True, cam=True ))
    #shutil.move(fileT,project+'movies/'+fileName+'.mov')
#---------------------------------------------------------------------------------------------
def showDoPlay():
    pathFile = path.split(mc.file( q=True, sn=True))[0]
    fileName = mc.textField('nameDoPlayTxtFld', q=True, tx=True)
    try:
        os.chdir( pathFile+"/" )
        os.startfile( fileName+".mov" )
    except:
        mc.warning(">> PLAYBLAST   '"+fileName+"'   NOT FOUND!")


#---------------------------------------------------------------------------------------------
def fillDoPlay():
    pathFile = path.split(mc.file( q=True, sn=True))[0]
    print pathFile
    dialFile = sorted( os.listdir( pathFile ) )

    if mc.popupMenu( 'fillPlayMenu', q=True, exists=True ):
        mc.deleteUI('fillPlayMenu')

    mc.popupMenu( 'fillPlayMenu', parent='nameDoPlayTxtFld' )
    for i in xrange( len(dialFile) ):
        if ".avi" in dialFile[i]:
            mc.menuItem(  parent='fillPlayMenu', label=dialFile[i].split(".")[0], c="mc.textField('nameDoPlayTxtFld', e=True, tx='"+dialFile[i].split(".")[0]+"')" )

def unlockCameraAttributes(aCamera):

    if mc.objectType(aCamera) == 'transform':

        for attribute in mc.listAttr(aCamera):
            try:
                mc.setAttr(aCamera + '.' + attribute,l = False)
            except:
                continue
        shape = mc.listRelatives(aCamera,s = True)[0]
        
        
        print shape
        for attribute in mc.listAttr(shape):
            try:
                mc.setAttr(shape + '.' + attribute,l = False)
            except:
                continue
def lockCameraAttributes(aCamera):

    if mc.objectType(aCamera) == 'transform':

        for attribute in mc.listAttr(aCamera):
            try:
                mc.setAttr(aCamera + '.' + attribute,l = True)
            except:
                continue
        shape = mc.listRelatives(aCamera,s = True)[0]
        print 'this is: ' + shape
        for attribute in mc.listAttr(shape):
            try:
                mc.setAttr(shape + '.' + attribute,l = True)
            except:
                continue
      

# FILL
#currentCamera = mc.modelEditor( mc.getPanel(wf=True), q=True, cam=True )
##unlockCameraAttributes(currentCamera)
doPlayBlastIWinUI()
fillDoPlay()
#cmds.getPanel(wf=True)
#print cmds.modelEditor( cmds.getPanel(wf=True), q=True, cam=True )
#unlockCameraAttributes(mc.modelEditor( mc.getPanel(wf=True), q=True, cam=True ))
#lockCameraAttributes(mc.modelEditor( mc.getPanel(wf=True), q=True, cam=True ))

#mc.panZoom('camera', abs=True)
