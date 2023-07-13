from maya import cmds as cm

class SelectMirrorRig():
    
    def __init__(self, *args):
        #cria a janela
        self.window= 'Mirror Rig'
        self.title= 'ERRO'
        self.size=(200,60)
       
       #testa se a janela ja existe
        if cm.window(self.window, exists= True):
            cm.deleteUI(self.window,window=True)
        
        #cria a janela e uma coluna para porder desenhar as coisas nela
        self.window = cm.window(self.window, title= self.title, sizeable=False, widthHeight=self.size)
        cm.rowColumnLayout(numberOfColumns=1,columnOffset=[(2,'right',2)], adjustableColumn=True)
       
       #pega o objeto selecionado
        selected = cm.ls(sl=True,long=True) or []
        print(selected)
       
       #se nao selecionou nenhum objeto abre uma janela de erro
        if selected==[]:
            cm.text(label='Select Object!!!')
            cm.button(label='Close Window',command="cmds.deleteUI('%s')" % self.window)
            cm.showWindow()
        
        for eachSel in selected:
           print(eachSel)
           
           try: 
               #caso o objeto terminar com r_ (lado direito), ele altera o 'r' pelo 'l' e seleciona o lado esquerdo
               eachSel.index("r_")
              
               try:
                   select= cm.select(eachSel.replace("r_", "l_",1))
               
               except:
                #caso o objeto do outro lado nao exista
                   cm.text(label='Object not found')
                   cm.button(label='Close Window',command="cmds.deleteUI('%s')" % self.window)
                   cm.showWindow()
               
           
           except: 
               try:
                #caso o objeto terminar com l_ (lado esquerdo), ele altera o 'l' pelo 'r' e seleciona o lado direito
                   select= cm.select(eachSel.replace("l_", "r_",1))
               
               except:
                 #caso o objeto do outro lado nao exista
                   cm.text(label='Object not found')
                   cm.button(label='Close Window',command="cmds.deleteUI('%s')" % self.window)
                   cm.showWindow()
           
     
            

program= SelectMirrorRig()