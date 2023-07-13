import maya.cmds as cmds


class ReflectionChange():
    
    def __init__(self, *args):
       self.allMaterial()
                
    def allMaterial(self,*args):
         #pega o objeto selecionado no outliner
          theNodes = cmds.ls(sl = True, dag = True, s = True)
          #pega o shading engine e o material do objeto
          shadeEng = cmds.listConnections(theNodes , type = "shadingEngine")
          materials = cmds.ls(cmds.listConnections(shadeEng ), materials = True)
          
         
          for i in materials:  
             try:
                #para cara material selecionado altera ou o gloos ou reflect ou smigloos (descomentar qual for usar)
                 selected = cmds.ls(i)
                 cmds.setAttr('%s.useRoughness' % i, 1)
                 
                 ##Gloss
                 cmds.setAttr('%s.reflectionColorAmount' % i,0.200)
                 cmds.setAttr('%s.reflectionGlossiness' % i,0.600)
  
                 
                 #NoReflect
                 #cmds.setAttr('%s.reflectionColorAmount' % i,0.050)
                 #cmds.setAttr('%s.reflectionGlossiness' % i,0.950)
                 
                 #SemiGloss
                 #cmds.setAttr('%s.reflectionColorAmount' % i,0.100)
                 #cmds.setAttr('%s.reflectionGlossiness' % i,0.650)
                   
                 
             except: 
                 print ("nao foi possível setar os atributos")
                 pass
         
         
        
program= ReflectionChange()