bl_info = {
    "name": "Les Fees Speciales",
    "author":"Les Fees Speciales",
    "version":(1,0),
    "location": "Tools ",
    "description":"File management tool for production",
    "wiki_url":"http://les-fees-speciales.coop/wiki/",
    "category":"User"
}

'''
Copyright (C) 2015 LES FEES SPECIALES

Created by LES FEES SPECIALES

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from pprint import pprint
import bpy
import os.path
from bpy.props import *
import sys
sys.path.append('/u/lib/python3x')
import naming.Herakles as naming
from bpy.props import IntProperty, CollectionProperty #, StringProperty 
from bpy.types import Panel, UIList
import shutil

"""_______________________HELP SECTION________________________________

PROP OPTION:
    prop(data, property, text="", text_ctxt="", translate=True, icon='NONE', expand=False, slider=False, toggle=False, icon_only=False, event=False, full_event=False, emboss=True, index=-1, icon_value=0)

LAYOUT INFO:
    http://www.blender.org/api/blender_python_api_2_69_3/bpy.types.UILayout.html#bpy.types.UILayout
test:
___________________________________________________________________"""


'''<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

                  VARS

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''
#-----GENERAL VARS-------
command=['initializing...done']
folders =[]
property = []#contain all props in a near futur.....
Items = []

#-----NAMING VARS-------
path={}
drives = (('Store',"Store directory",''),('/u/Project/',"/u/Project/",''),('test2_1',"test2_2",''),('',"",''))
is_wild = 'True'

#adding 
property.append(drives)

'''-----------------------------------------------

             FILES FUNC 

----------------------------------------------'''
#...................................
#         File                     #
#                                  #
#   Basic file class for           #
#       purpose                    #
#...................................
class file:
    def __init__(self):
       self.name = None
       self.type = None 
       self.hide = False                       
#...................................
#         checking func            #
#             to test              #
#          the type of file        #
#                                  #
#...................................             
def isfolder(name):
    if name.find('.') == -1:
        return True
    else:
        return False
#...................................
#         List directories         #
#...................................               
def listdir(root):
    buffer = os.listdir(root)
    for i in range(len(buffer)-1):
        tmp = file()
        if isfolder(buffer[i]):
            tmp.type = 'D'
        else:
            tmp.type = 'F' 
        tmp.hide = False  
        tmp.name= buffer[i]   
        folders.append(tmp)           
#...................................
#         List files               #
#...................................
def listFiles(dir, ext):
    fileList = []

    for file in os.listdir(dir):
        if file[-len(ext):] == ext:
            fileList.append(file)
            
    return fileList

'''-----------------------------------------------

             INTERFACE NAMING FUNC 

----------------------------------------------'''
#...................................
#         Create_naming            #
#                                  #
#   Create the basic naming        #
#       object and use it          #
#...................................
def create_naming(self,context,op):
    #Generate naming Object
    n = naming.StoreFolder.from_name(path['Store'])
    #Allowing dico
    c =n(**path)
    dir = c.path()
    print(c.path())
    command.append(c.path())
    bpy.context.scene.wild  = c.is_wild()        
    if op == 'CREATE':
        print("Create missing folders with naming...")
        c.create()
        print("done.")
        
    print("the way is wild : "+is_wild)
    return c.path()

def Update_ListFile(dir):
    bpy.context.scene.custom.clear()
    list = listFiles(bpy.types.Scene.newF,".blend")
    print(list)
    for i in range(len(list)):
        bpy.context.scene.custom.add()
        bpy.context.scene.custom[i].name = list[i]
#...................................
#         update_naming            #
#                                  #
#   update the basic naming        #
#       object and use it          #
#...................................
def update_naming(self, context):
    path.clear()
    #print(bpy.context.scene.drives.split('/'))
    path['Store']='/'+bpy.context.scene.drives.split('/')[1]
    path['Project']=bpy.context.scene.drives.split('/')[2]
    
    if bpy.context.scene.roots == 'LIB':
        path['Lib'] = 'LIB'
        path['Family']=bpy.context.scene.famille
        path['Asset']=bpy.context.scene.asset
        path['Dept']=bpy.context.scene.dpt
    elif bpy.context.scene.roots =='MOVIE':
        path['Film'] = 'FILM'
        path['Sequence'] = bpy.context.scene.seq
        path['Shot'] = bpy.context.scene.shot
        path['Dept'] = bpy.context.scene.dpt
    #pprint(path)
    
    bpy.types.Scene.newF = create_naming(self,context,'')
    Update_ListFile(bpy.types.Scene.newF)
    
    return None


       
def initSceneProperties():
     #PROJECT DIR----------------------------->
     bpy.types.Scene.drives = EnumProperty(name="none",description="none",items=(('')))
     s = len(property)
     
     Items.append(('none',"none",""))        
     for i in range(s):      
        for line in range(1,len(property[i]),3):
            Items.append((str(property[i][line][0]),str(property[i][line][1]),str(property[i][line][2])))         
            print(Items)
        UpdateEnum(bpy.types.Scene,tuple(Items),property[i][0][0],property[i][0][1],Items[0][0])    
         
     #ROOT----------------------------->
     bpy.types.Scene.roots = EnumProperty(
        name="Root",
        description="root",
        items=(('LIB', "LIB", ""),
               ('MOVIE', "MOVIE", ""),
               ('', "", "")),
        default='LIB',
        update = update_naming)  
        
     #FAMILY----------------------------------->
     bpy.types.Scene.famille = EnumProperty(
        name="famille",
        description="/lib/type/famille",
        items=(('none', "none", ""),
               ('Chars', "Chars", ""),
               ('Props', "Props", ""),
               ('Sets', "Sets", ""),
               ('Lookdev', "Lookdev", ""),
               ('none', "none", "")),
        default='none',
        update = update_naming)
     #ASSET------------------------------------>
     bpy.types.Scene.asset = EnumProperty(
        name="asset",
        description="/lib/type/famille/asset",
        items=(('none', "none", ""),
               ('a1', "a1", ""),
               ('a2', "a2", ""),
               ('a3', "a3", ""),
               ('a4', "a4", ""),
               ('NEW', "NEW", "")),
        default='none',
        update = update_naming)
        
     #DEPARTEMENT----------------------------->
     bpy.types.Scene.dpt = EnumProperty(
        name="dpt",
        description="/lib/type/famille/asset/dpt or /movie/seq/shot/dpt",
        items=(('none', "none", ""),
               ('Mod', "Mod", ""),
               ('Actor', "Actor", ""),
               ('Anim', "Anim", ""),
               ('Layout', "Layout", ""),
               ('Lighting', "Lighting", ""),
               ('Compo', "Compo", ""),
               ('Matte', "Mat", ""),
               ('Cam', "Cam", ""),
               ('Vfx', "Vfxr", ""),
               ('Shad', "Shad", "")),
        default='none',
        update = update_naming) 
      #SEQUENCE------------------------------->
     bpy.types.Scene.seq = EnumProperty(
        name="type",
        description="/movie/seq",
        items=(('none', "none", ""),
               ('S_001', "S_001", ""),
               ('S_002', "S_002", ""),
               ('S_003', "S_003", ""),
               ('NEW', "NEW", "")),
        default='none',
        update = update_naming)
     #SHOT------------------------------------>
     bpy.types.Scene.shot = EnumProperty(
        name="type",
        description="/movie/seq/shot",
        items=(('none', "none", ""),
               ('P_001', "P_001", ""),
               ('P_002', "P_002", ""),
               ('P_003', "P_003", ""),
               ('NEW', "NEW", "")),
        default='none',
        update = update_naming) 
     #Strings props---------------------------->
     bpy.types.Scene.newF = StringProperty(
        name="",
        subtype = 'FILE_NAME',
        description="new familly",
        maxlen= 50,
        default= "")
     bpy.types.Scene.newA = StringProperty(
        name="",
        subtype = 'FILE_NAME',
        description="new asset",
        maxlen= 50,
        default= "")
     bpy.types.Scene.newD = StringProperty(
        name="",
        subtype = 'FILE_NAME',
        description="new asset",
        maxlen= 50,
        default= "")
     #HIDING BOOLEANS------------------------->
     bpy.types.Scene.hidec = BoolProperty(
        name = "hidec", 
        default=False,
        description = "hide console")
     bpy.types.Scene.wild = BoolProperty(
        name = "is_wild", 
        default=True,
        description = "is the path valid")
     bpy.types.Scene.hidecreator = BoolProperty(
        name = "hidec", 
        default=False,
        description = "hide console")
    
           

'''<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

                     File List

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''
# return name of selected object
def get_activeSceneObject():
    return bpy.context.scene.objects.active.name

# custom list
class UL_items(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(0.6)
        split.prop(item, "name", text="", emboss=False, translate=False, icon='FILE')
        split.label("Version: %d" % (index))

    def invoke(self, context, event):
        pass   

# Create custom property group
class CustomProp(bpy.types.PropertyGroup):
    name = StringProperty() 
    id = IntProperty()
'''<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

                DIALOG OPERATOR

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>''' 
class DialogOperator(bpy.types.Operator):
    bl_idname = "object.dialog_operator"
    bl_label = "Pose already exist, overwrite or change the pose name"
    
    overwrite = BoolProperty(name="Overwrite")
    
    def execute(self, context):
        scn = context.scene
        if self.overwrite:
            print("overwrite")
            file_name = bpy.types.Scene.newF.split("/")
            p = bpy.types.Scene.newF+"/"+file_name[len(file_name)-1]+".blend"
            bpy.ops.wm.save_as_mainfile(filepath=p) 
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
'''<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

                OPEN DIR OPERATOR

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>''' 
class OBJECT_OT_custompath(bpy.types.Operator):
    bl_idname = "object.custom_path"
    bl_label = "open"
    __doc__ = ""
    
    
    filename_ext = ".txt"
    filter_glob = StringProperty(default="*.txt", options={'HIDDEN'})    
        
    
    #this can be look into the one of the export or import python file.
    #need to set a path so so we can get the file name and path
    filepath = StringProperty(name="File Path", description="Filepath used for importing txt files", maxlen= 1024, default= "")
    files = CollectionProperty(
        name="File Path",
        type=bpy.types.OperatorFileListElement,
        )    
    def execute(self, context):
        #set the string path fo the file here.
        #this is a variable created from the top to start it
        bpy.context.scene.newF = self.properties.filepath
        
        
        print("*************SELECTED FILES ***********")
        for file in self.files:
            print(file.name)
        
        print("FILEPATH %s"%self.properties.filepath)#display the file name and current path    
        Items.append((str(self.properties.filepath),str(self.properties.filepath),""))
        UpdateEnum(bpy.types.Scene,Items,str(self.properties.filepath),str(self.properties.filepath),str(self.properties.filepath))
        return {'FINISHED'}


    def draw(self, context):
        self.layout.operator('file.select_all_toggle')        
    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}


'''---------------------------------------------------

                General function to update
                      -EnumProperty-

---------------------------------------------------'''

def UpdateEnum(Enums,Itemss,Name,Description,Defaults):
    print("update file list")
    bpy.types.Scene.drives= EnumProperty(
        name=Name,
        description=Description,
        items=Itemss,
        default=Defaults)        
        
'''<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

                FILE OPERATOR

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>''' 
class file_op(bpy.types.Operator):
    bl_idname = "scene.file_op"
    bl_label = "file_op"
    
    action = bpy.props.StringProperty() # defining the property
    def execute(self, context):
        if self.action == "NEW":
            print("create directories")
            create_naming(bpy.context,bpy.context,'CREATE')
            file_name = bpy.types.Scene.newF.split("/")
            p = bpy.types.Scene.newF+"/"+file_name[len(file_name)-1]+".blend"
            if os.path.isfile(p):
                command.append("File already exist")
                bpy.ops.object.dialog_operator('INVOKE_DEFAULT') #calls the popup
            else:
                print("saving file to :"+str(p))  
                shutil.copyfile('/u/tools/blender_fee/base.blend',p)  
                    
        elif self.action == "OPEN":
            print("opening file")
            file_name =  bpy.context.scene.custom[bpy.context.scene.custom_index].name
            p = bpy.types.Scene.newF+"/"+file_name
            bpy.ops.wm.open_mainfile(filepath = p)
            
        elif self.action == "SAVE_AS":
            create_naming(bpy.context,bpy.context,'CREATE')
            file_name = bpy.types.Scene.newF.split("/")
            p = bpy.types.Scene.newF+"/"+file_name[len(file_name)-1]+".blend"
            if os.path.isfile(p):
                command.append("File already exist")
                bpy.ops.object.dialog_operator('INVOKE_DEFAULT') #calls the popup
            else:
                print("saving file to :"+str(p))  
                bpy.ops.wm.save_as_mainfile(filepath=p)    
        return {"FINISHED"}

'''<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

                HELP OPERATOR

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''     
class Help(bpy.types.Operator):
    bl_idname = "scene.help"
    bl_label = "help"
    
    def execute(self, context):
        bpy.ops.wm.url_open(url="http://les-fees-speciales.coop/wki/")
        return {"FINISHED"}
    
'''<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

                hide console

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''         
class XP(bpy.types.Operator):
    bl_idname = "scene.xp"
    bl_label = "xp"
    
    def execute(self, context):
        if context.scene.hidec:
            context.scene.hidec = False
        else:
            context.scene.hidec = True
            
        return {"FINISHED"}

'''<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

                hide operator

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''         
class hide(bpy.types.Operator):
    bl_idname = "scene.hide"
    bl_label = "hide"
    
    def execute(self, context):
        if context.scene.hidecreator:
            context.scene.hidecreator = False
        else:
            context.scene.hidecreator = True
            
        return {"FINISHED"}

'''<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

                GUI CREATION

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>''' 
class naming_panel(bpy.types.Panel):
    bl_label = "Files Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "les fees speciales"

    
    def draw(self, context):
        layout = self.layout
        scn = context.scene    
        row = layout.row()
        box = layout.box()
        #Example of external drawing function: draw_opener(self,bpy.context,command)
        
        row = box.row(align=True)
        
        #---> PANEL HIDE 
        if scn.hidecreator:            
            row.operator("scene.hide",text="",emboss=False,icon='TRIA_RIGHT')    
            
            row.label(text='FILE TOOLS')
            row.separator()
            row.operator("scene.help",text="",emboss=False,icon='HELP')
            
        #---> PANEL NOT HIDE        
        elif not scn.hidecreator:
            row.operator("scene.hide",text="",emboss=False,icon='TRIA_DOWN') 
            row.label(text='FILE TOOLS')   
            
            row.operator("scene.help",text="",emboss=False,icon='HELP')
            row = box.row()
                            
            row.scale_y=1.5
            row = box.row()
            
            split = row.split()

            col = split.column()
            
            sub = col.column(align=True)
            sub.label(text="Project dir:") 
            
            #addd=========================================================
            
            subrow = sub.row(align=True)
        
            subrow.prop(context.scene,"drives",text="")
            subrow.operator("object.custom_path",text="", icon='FILE_FOLDER')
            
            #=============================================================
            row = box.row()
                
            row.prop(context.scene, "roots", expand=True)

            ''' IF MOVIE'''
            if scn.roots == 'MOVIE':         
                row = box.row()
                box = row.box()
                row = box.row(align=True)
 
                
                #SEQ=============================================
                if(scn.seq=='none'):
                    row.label(text=" SEQUENCE",icon='QUESTION')
                else:
                    row.label(text=" SEQUENCE",icon='FILE_TICK')
                row = box.row(align=True)     
                
                #type setting------------------------------------- 
                split = row.split(align=True)
                
                col = split.column()   
                sub = col.column(align=True)
                sub.prop(scn, "seq",expand=False,text='')
                #row = box.row()
                
                if scn.seq == 'NEW':
                    sub.prop(scn, "newF")
                    
                row = box.row()
                
                #SHOT=============================================
                if(scn.shot=='none'):
                    row.label(text=" SHOT",icon='QUESTION')
                else:
                    row.label(text=" SHOT",icon='FILE_TICK')
                row = box.row(align=True)     
                
                #type setting------------------------------------- 
                split = row.split(align=True)
                
                col = split.column()   
                sub = col.column(align=True)
                sub.prop(scn, "shot",expand=False,text='')
                #row = box.row()
                
                if scn.shot == 'NEW':
                    sub.prop(scn, "newF")
                    
                row = box.row()
                  
               
     
            elif scn.roots == 'LIB':
                row = box.row()
                box = row.box()
                row = box.row()
                
                #family setting-------------------------------------    
                if(scn.famille=='none'):
                    row.label(text=" FAMILY",icon='QUESTION')
                else:
                    row.label(text=" FAMILY",icon='FILE_TICK')
                row = box.row(align=True)     
                
                
                row.prop(scn,"famille",expand=True,icon_value=4)
                row = box.row()
                
                
                #asset setting----------------------------------
                split = row.split(align=True)
                col = split.column()
                
                if(scn.asset=='none'):
                    col.label(text=" ASSET",icon='QUESTION')
                else:
                    col.label(text=" ASSET",icon='FILE_TICK')
                #col.row(align=True)
                sub = col.column(align=True)
                sub.prop(scn, "asset",expand=False,text='')
                if scn.asset == 'NEW':
                  sub.prop(scn, "newA")
                
                row = box.row()
                
            #dpt setting----------------------------------
            split = row.split(align=True)
            col = split.column()

            if(scn.dpt=='none'):
                col.label(text=" DPT",icon='QUESTION')
            else:
                col.label(text=" DPT",icon='FILE_TICK')
            
            sub = col.column(align=True)
            sub.prop(scn, "dpt",expand=False,text='')
     
            row = box.row()        
                   
            #File list---------------------------------------
            rows = 3
            row.template_list("UL_items", "", scn, "custom", scn, "custom_index", rows=rows)
            #row = box.row()
            row = box.row()
            
            #Operator OPEN/NEW/SAVE AS--------------------------
            row.alignment='CENTER'
            row.scale_y=1.5
            
            row.operator("scene.file_op",text="NEW",emboss=True,icon='FILE').action = "NEW" 
            row.operator("scene.file_op",text="SAVE AS",emboss=True,icon='PASTEDOWN').action = "SAVE_AS" 
            row.operator("scene.file_op",text="OPEN",emboss=True,icon='NEWFOLDER').action = "OPEN"
            
            
            if scn.wild:
                row.enabled =  False
            else:
                row.enabled =  True
                
            row = box.row()
            box=row.box()
                
            #console-------------------------------------------------------
            row = box.row()
            
            if scn.hidec:
                row.label(text='output',icon='CONSOLE')
                row.operator("scene.xp",text="",emboss=False,icon='ZOOMIN') 
               
                
            elif not scn.hidec:
                row.label(text='output',icon='CONSOLE')
                row.operator("scene.xp",text="",emboss=False,icon='ZOOMOUT') 
                            
                box2=box.row()
                
                #box2= box.box()
                for i in range(len(command)):    
                   
                    box2.label(text=">> "+command[i])
                    box2.scale_y=0.3
                    box2=box.row()
      
def register():
    initSceneProperties() 
    bpy.utils.register_module(__name__)
    bpy.types.Scene.custom = CollectionProperty(type=CustomProp)
    bpy.types.Scene.custom_index = IntProperty()

def unregister():   
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.custom
    del bpy.types.Scene.custom_index

if __name__ == "__main__":
    register()
