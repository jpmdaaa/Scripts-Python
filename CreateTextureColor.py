import maya.cmds as cm
from resources import pylightxl as xl

class CreateLambColor():
    def __init__(self, *args):
        self.create_shader()  
       
    def create_shader(self, node_type="lambert"):
        #carrega a planilha 
        db = xl.readxl(fn='sample.xlsx')
        #passa por cada linha da planilha
        for row in db.ws(ws='Sheet').rows:
            #verifica se o objeto existe      
            if cm.objExists(row[1]):
                #verifica se o material ja existe
                if cm.objExists(row[1]+"_lambert"):
                     print("o lambert com este nome ja existe")
                #se o material ainda nao foi criado     
                else:     
                    #cria o material, o shading group, e conecta os dois
                    material = cm.shadingNode(node_type, name=row[1]+"_lambert", asShader=True)
                    sg = cm.sets(name="%sSG" % row[1]+"_lambert", empty=True, renderable=True, noSurfaceShader=True)
                    cm.connectAttr("%s.outColor" % material, "%s.surfaceShader" % sg)
                    #define a cor (carrega a cor da planilha)
                    cm.setAttr(material+'.color', float(row[2]), float(row[3]), float(row[4]))
                    #seleciona o material 
                    conectionsMat = cm.listConnections(material, d=True, et=True, t='shadingEngine')
                    #aplica o material no obj
                    cm.sets(row[1], e=True, forceElement= conectionsMat[0])
            
            #se o objeto nao existe    
            else:
                print("o objeto:"+ row[1]+ " nao existe")
      
        return material, sg
       
                 
CreateLambColor() 