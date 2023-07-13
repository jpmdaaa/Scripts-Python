import maya.cmds as cm


class AlembicGen():
    
    def __init__(self, *args):
        #cria a janela
        self.window= 'AlembicWindow'
        self.title= 'AlembicGenerator'
        self.size=(100,100)
       
       #testa se a janela ja existe
        if cm.window(self.window, exists= True):
            cm.deleteUI(self.window,window=True)
        
        #cria a janela e uma coluna para porder desenhar as coisas nela
        self.window = cm.window(self.window, title= self.title, sizeable=True, widthHeight=self.size)
        cm.rowColumnLayout(numberOfColumns=1,columnAlign=(1,'right'),columnAttach=(2,'both',0), adjustableColumn=True)      
        self.nameObjField = cm.textFieldGrp(l= 'Name Obj / Number Shot: ', editable=True)    
        self.createMinFrame = cm.textFieldGrp(l= 'First Frame: ', editable=True)  
        self.createMaxFrame = cm.textFieldGrp(l= 'Last Frame: ', editable=True)    
        self.HideControlBtn = cm.button(label='Hide Controls', command= self.hideAll)
        self.ShowControlBtn = cm.button(label='Show Controls', command= self.showAll)
        self.creatAlembicLayBtn = cm.button(label='Create Alembic', command= self.creatAlembicLay)
        self.SelecProjetcMenu = cm.optionMenu(w = 250, label = "Project:")
        cm.menuItem(label = "VMB")
        cm.menuItem(label = "Other")
          
        cm.showWindow()
            
    def creatAlembicLay(self, *args):
        
        getFirstFrame= cm.textFieldGrp(self.createMinFrame, q=True, text=True)
        getLastFrame= cm.textFieldGrp(self.createMaxFrame, q=True, text=True)
        currentValueProject= cm.optionMenu(self.SelecProjetcMenu, query=True, value=True)
        nameObj=cm.textFieldGrp(self.nameObjField,q=True, text=True)
        print (currentValueProject)
        cameraNames= cm.ls(cameras=True)
        cameraShape= cameraNames[0]
        print (cameraShape)
        cm.camera(cameraShape , e=True, dgm=False, dst=False, dsa=False, dr=False, dfg=False, ovr=1.0)
        directory = cm.fileDialog2(cap = "Choose the new path",fm = 3)[0] + '/'
       
        
        if currentValueProject == "VMB":
            if cm.objExists("CAM_SH" + nameObj + "_grp" ):
               cm.AbcExport( j = "-frameRange " +  getFirstFrame + " " + getLastFrame+ " -ro -stripNamespaces -uvWrite -worldSpace -writeVisibility -dataFormat ogawa -root |CAM_SH" + nameObj + "_grp" + " -file " + directory + "/camera.abc")
               cm.AbcExport( j = "-frameRange " +  getFirstFrame + " " + getLastFrame+ " -ro -stripNamespaces -uvWrite -worldSpace -writeVisibility -dataFormat hdf5 -root |CAM_SH" + nameObj + "_grp" + " -file " + directory + "/camera_hdf5.abc")

            if cm.objExists('domo'):
                cm.AbcExport( j = "-frameRange " + getFirstFrame + " " + getLastFrame+ " -ro -stripNamespaces -uvWrite -worldSpace -writeVisibility -dataFormat ogawa -root |domo -file " + directory + "/domo.abc")
            
            if cm.objExists('SCENE_grp'):
                cm.AbcExport( j = "-frameRange " + getFirstFrame + " " + getLastFrame+ " -ro -stripNamespaces -uvWrite -worldSpace -writeVisibility -dataFormat ogawa -root |SCENE_grp -file " + directory + "/scene.abc")
             
        
                print ('Alembic gerado em: '+directory)
            
        if currentValueProject == "Other":
            if cm.objExists(nameObj):
                if nameObj[0:3]== "CAM":
                     cm.AbcExport( j = "-frameRange " +  getFirstFrame + " " + getLastFrame+ " -ro -stripNamespaces -uvWrite -worldSpace -writeVisibility -dataFormat ogawa -root |" + nameObj + " -file " + directory + "/"+ nameObj+ ".abc")
                     cm.AbcExport( j = "-frameRange " +  getFirstFrame + " " + getLastFrame+ " -ro -stripNamespaces -uvWrite -worldSpace -writeVisibility -dataFormat hdf5 -root |" + nameObj + " -file " + directory + "/"+ nameObj+"_hdf5" + ".abc")
                else:
                    cm.AbcExport( j = "-frameRange " +  getFirstFrame + " " + getLastFrame+ " -ro -stripNamespaces -uvWrite -worldSpace -writeVisibility -dataFormat ogawa -root |" + nameObj + " -file " + directory + "/"+ nameObj+ ".abc")
                    
                print ('Alembic gerado em: ' + directory)
                    
      

    def hideAll(self, *args):
        rigg_folders = [x for x in cm.ls(type = "transform",l = True) if len(x) >= 3 and ("rig" == x[-3:].lower() or "moveall_ctrl_grp" in x.lower())] + cm.ls(type = "parentConstraint")
        for re in rigg_folders:
            try:
                cm.setAttr(re + ".visibility",0)
            except:
                continue

    def showAll(self, *args):
        rigg_folders = [x for x in cm.ls(type = "transform",l = True) if len(x) >= 3 and ("rig" == x[-3:].lower() or "moveall_ctrl_grp" in x.lower())] + cm.ls(type = "parentConstraint")
        for re in rigg_folders:
            try:
                cm.setAttr(re + ".visibility",1)
            except:
                continue

program= AlembicGen()