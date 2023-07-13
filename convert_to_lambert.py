import maya.cmds as cmds

newMaterial = 'lambert'
# todos materias onde nao encontra o tipo
oldMaterial = 'unknown' #'aiStandardSurface'

#seleciona todos materias
allOldMaterial = cmds.ls (type=oldMaterial)


for mat in allOldMaterial:
    print ("Old Material: "+ mat)
    
    #cria o shading node para as novas conexoes
    SgNodes = cmds.listConnections (mat, destination=True, plugs=True, source=False, type='shadingEngine')
   
    if SgNodes:
        #cria o novo material
        newMat = cmds.shadingNode (newMaterial, asShader=True)
        print ("New Material:"+ newMat)
        
        #conecta o novo material no shading node
        shadEnginConec = '.outColor'  
        for s in SgNodes:
            
            cmds.connectAttr (newMat + shadEnginConec ,s , f=True)
            print ("New Shading Nodes: "+ s)
        
        #diffuse
        DiffuseAttrib = '.dc' #'.baseColor'
        
        if cmds.listConnections (mat + DiffuseAttrib, d=True, p=True):
            connect = cmds.listConnections (mat + DiffuseAttrib, d=True, p=True)
            cmds.connectAttr (connect[0], newMat + '.color',f=True)
            
        else:
            print ("Connections Not Found")
        #    baseColorR = cmds.getAttr (mat + '.baseColorR')
        #    baseColorG = cmds.getAttr (mat + '.baseColorG')
        #    baseColorB = cmds.getAttr (mat + '.baseColorB')       
        #    cmds.setAttr (nm + '.color', baseColorR,baseColorG,baseColorB)
        
        #deleta os materiais antigos
        cmds.delete (mat)
        #seta o nome do novo material igual ao antigo
        cmds.rename (newMat, mat)
        
    else:
        print ("Vray Nodes Not Found")

#cmds.listConnections ('_blendColors2', c=True )