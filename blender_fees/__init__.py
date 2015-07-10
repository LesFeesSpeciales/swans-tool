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

bl_info = {
    "name": "Les Fees Speciales",
    "author":"Les Fees Speciales",
    "version":(0,0),
    "blender":(2,75,0),
    "location": "View3D ",
    "description":"File management tool for production",
    "warning":"unstable",
    "wiki_url":"http://les-fees-speciales.coop/wiki/",
    "category":""
}

import bpy
from bpy.props import *
import sys
sys.path.append('/home/armabon/u/lib/python3x')
import naming.Herakles as naming
from opener import *
from bpy.props import IntProperty, CollectionProperty #, StringProperty 
from bpy.types import Panel, UIList


"""_______________________HELP SECTION________________________________

PROP OPTION:
    prop(data, property, text="", text_ctxt="", translate=True, icon='NONE', expand=False, slider=False, toggle=False, icon_only=False, event=False, full_event=False, emboss=True, index=-1, icon_value=0)

LAYOUT INFO:
    http://www.blender.org/api/blender_python_api_2_69_3/bpy.types.UILayout.html#bpy.types.UILayout
test:
___________________________________________________________________"""

# return name of selected object
def get_activeSceneObject():
    return bpy.context.scene.objects.active.name


# ui list item actions
class Uilist_actions(bpy.types.Operator):
    bl_idname = "custom.list_action"
    bl_label = "List Action"

    action = bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", ""),
        )
    )

    def invoke(self, context, event):

        scn = context.scene
        idx = scn.custom_index

        try:
            item = scn.custom[idx]
        except IndexError:
            pass

        else:
            if self.action == 'DOWN' and idx < len(scn.custom) - 1:
                item_next = scn.custom[idx+1].name
                scn.custom_index += 1
                info = 'Item %d selected' % (scn.custom_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'UP' and idx >= 1:
                item_prev = scn.custom[idx-1].name
                scn.custom_index -= 1
                info = 'Item %d selected' % (scn.custom_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'REMOVE':
                info = 'Item %s removed from list' % (scn.custom[scn.custom_index].name)
                scn.custom_index -= 1
                self.report({'INFO'}, info)
                scn.custom.remove(idx)

        if self.action == 'ADD':
            item = scn.custom.add()
            item.id = len(scn.custom)
            
            item.name = get_activeSceneObject() # assign name of selected object
            scn.custom_index = (len(scn.custom)-1)
            info = '%s added to list' % (item.name)
            self.report({'INFO'}, info)

        return {"FINISHED"}

# -------------------------------------------------------------------
# draw
# -------------------------------------------------------------------

# custom list
class UL_items(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(0.6)
        split.prop(item, "name", text="", emboss=False, translate=False, icon='FILE')
        split.label("Version: %d" % (index))

    def invoke(self, context, event):
        pass   

# print button
class Uilist_printAllItems(bpy.types.Operator):
    bl_idname = "custom.print_list"
    bl_label = "Print List"
    bl_description = "Print all items to the console"

    def execute(self, context):
        scn = context.scene
        for i in scn.custom:
            print (i.name, i.id)
        return{'FINISHED'}

# select button
class Uilist_printAllItems(bpy.types.Operator):
    bl_idname = "custom.select_item"
    bl_label = "Select List Item"
    bl_description = "Select Item in scene"

    def execute(self, context):
        scn = context.scene
        bpy.ops.object.select_all(action='DESELECT')
        obj = bpy.data.objects[scn.custom[scn.custom_index].name]
        obj.select = True

        return{'FINISHED'}


# Create custom property group
class CustomProp(bpy.types.PropertyGroup):
    '''name = StringProperty() '''
    id = IntProperty()


command=['test','test2','test2','test2']
folders =[]

'''<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

                VAR INIT

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''
def initSceneProperties(scn):
     bpy.types.Scene.FPath = StringProperty(
        name="",
        description="searching root",
        maxlen= 1024,
        subtype='DIR_PATH',
        default= "")
     bpy.types.Scene.drives = EnumProperty(
        name="Store",
        description="Store directory",
        items=(('toto', "toto", ""),
               ('toto2', "toto2", ""),
               ('', "", "")),
        default='',
        update=update_value(bpy.context,bpy.context,'drive'))
     bpy.types.Scene.roots = EnumProperty(
        name="Root",
        description="root",
        items=(('LIB', "LIB", ""),
               ('MOVIE', "MOVIE", ""),
               ('', "", "")),
        default='')
     bpy.types.Scene.type = EnumProperty(
        name="type",
        description="/lib/type",
        items=(('none', "none", ""),
               ('CHAR', "CHAR", ""),
               ('PROP', "PROP", ""),
               ('SET', "SET", ""),
               ('LOOKDEV', "LOOKDEV", "")),
        default='none')  
     bpy.types.Scene.famille = EnumProperty(
        name="famille",
        description="/lib/type/famille",
        items=(('none', "none", ""),
               ('f1', "f1", ""),
               ('f2', "f2", ""),
               ('f3', "f3", ""),
               ('f4', "f4", ""),
               ('none', "none", "")),
        default='none') 
     bpy.types.Scene.asset = EnumProperty(
        name="asset",
        description="/lib/type/famille/asset",
        items=(('none', "none", ""),
               ('a1', "a1", ""),
               ('a2', "a2", ""),
               ('a3', "a3", ""),
               ('a4', "a4", ""),
               ('NEW', "NEW", "")),
        default='none') 
     bpy.types.Scene.dpt = EnumProperty(
        name="dpt",
        description="/lib/type/famille/asset/dpt or /movie/seq/shot/dpt",
        items=(('none', "none", ""),
               ('dpt1', "dpt1", ""),
               ('dpt2', "dpt2", ""),
               ('dpt3', "dpt3", ""),
               ('dpt4', "dpt4", "")),
        default='none') 
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
     bpy.types.Scene.command = StringProperty(
        name="",
        description="command",
        maxlen= 500,
        default= '      -initialisation')
     bpy.types.Scene.hidec = BoolProperty(
        name = "hidec", 
        default=False,
        description = "hide console")
     bpy.types.Scene.hidecreator = BoolProperty(
        name = "hidec", 
        default=False,
        description = "hide console")
     bpy.types.Scene.seq = EnumProperty(
        name="type",
        description="/movie/seq",
        items=(('none', "none", ""),
               ('S_001', "S_001", ""),
               ('S_002', "S_002", ""),
               ('S_003', "S_003", ""),
               ('NEW', "NEW", "")),
        default='none')
     bpy.types.Scene.mode = EnumProperty(
        name="mode",
        description="file tool mode",
        items=(('OPEN', "Open Mode", "Opening file mode",'FILE_FOLDER',1),
               ('CREATE', "Create Mode", "Create file mode",'FILE',2),
               ('CHECK', "Check Mode", "Checking file mode",'FILE_SCRIPT',3)),
        default='OPEN')
     bpy.types.Scene.shot = EnumProperty(
        name="type",
        description="/movie/seq/shot",
        items=(('none', "none", ""),
               ('P_001', "P_001", ""),
               ('P_002', "P_002", ""),
               ('P_003', "P_003", ""),
               ('NEW', "NEW", "")),
        default='none')  
     '''-----------------------------------------
     
                    OPENER VARS
     
     -----------------------------------------'''
     bpy.types.Scene.hideopener = BoolProperty(
        name = "hideopener", 
        default=False,
        description = "hide console")
           
def update_value(self,context,type):
    print('update drive')
    #if type =='drive':
       #command.append(context.scene.drives)
         
    return None

'''<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

                FILE CREATE OPERATOR

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>''' 
class createF(bpy.types.Operator):
    bl_idname = "scene.createf"
    bl_label = "createf"
    
    def execute(self, context):
        print("Hello")
        
        return {"FINISHED"}

'''<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

                HELP OPERATOR

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''     
class Help(bpy.types.Operator):
    bl_idname = "scene.help"
    bl_label = "help"
    
    def execute(self, context):
        bpy.ops.wm.url_open(url="http://les-fees-speciales.coop/wiki/")
        return {"FINISHED"}
'''<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

                hide opener

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

                hide operator

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''         
class hideo(bpy.types.Operator):
    bl_idname = "scene.hideo"
    bl_label = "hideo"
    
    def execute(self, context):
        if context.scene.hideopener:
            context.scene.hideopener = False
        else:
            context.scene.hideopener = True
            
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
        #draw_opener(self,bpy.context,command)
        
        row = box.row(align=True) 
        if scn.hidecreator:
            
            #row.alignment='LEFT'
            
            row.operator("scene.hide",text="",emboss=False,icon='TRIA_RIGHT')    
            #row.prop(context.scene,"mode",text='',expand =True,emboss=True,icon_only=True)
            
            row.label(text='FILE TOOLS')
            #row.label(text=context.scene.mode+' MODE')
            #row.alignment='RIGHT'
            row.separator()
            row.operator("scene.help",text="",emboss=False,icon='HELP')
                
        elif not scn.hidecreator:
            #row.alignment='EXPAND'
            row.operator("scene.hide",text="",emboss=False,icon='TRIA_DOWN') 
            #row.prop(context.scene,"mode",text='',expand =True,emboss=True,icon_only=True)
            row.label(text='FILE TOOLS')
            #row.alignment='RIGHT'
            
            row.operator("scene.help",text="",emboss=False,icon='HELP')
            row = box.row()
            
            if scn.mode != 'CHECK':
                
                row.scale_y=1.5
                row = box.row()
              
                split = row.split()

                col = split.column()
                sub = col.column(align=True)
                #col = layout.column()
                #subrow = row.row(align=True)
                sub.label(text="New store dir:") 
    
                sub.prop(context.scene, "FPath",text='',icon_only=True)
               
                col = split.column()
                sub = col.column(align=True)
                sub.label(text="Bookmarks:")
                sub.prop(context.scene,"drives",text="",icon='BOOKMARKS')
                
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
                    
                    
                    if(scn.type=='none'):
                        row.label(text=" TYPE",icon='QUESTION')
                    else:
                        row.label(text=" TYPE",icon='FILE_TICK')
                    row = box.row(align=True)     
                    
                    #type setting-------------------------------------    
                    row.prop(scn,"type",expand=True,icon_value=4)
                    row = box.row()
                    
                    
                    #familly setting----------------------------------
                    
                    #row = box.row()    
                    split = row.split(align=True)
                    
                    col = split.column()  
                    
                    if(scn.famille=='none'):
                        col.label(text=" FAMILLE",icon='QUESTION')
                    else:
                        col.label(text="FAMILLE",icon='FILE_TICK')
                    #col.row(align=True)
                    sub = col.column(align=True)
                    sub.prop(scn, "famille",expand=False,text='')
                    #row = box.row()
                    
                    if scn.famille == 'NEW':
                        sub.prop(scn, "newF")
                        
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
                #col.row(align=True)
                sub = col.column(align=True)
                sub.prop(scn, "dpt",expand=False,text='')
         
                  
                row = box.row()
                #row = box.row()
                #box= box.row()
                
                
                rows = 3
                row.template_list("UL_items", "", scn, "custom", scn, "custom_index", rows=rows)
                #row = box.row()
                row = box.row()
                row.alignment='CENTER'
                row.scale_y=1.5
                row.operator("scene.createf",text="NEW",emboss=True,icon='FILE') 
                row.operator("scene.createf",text="OPEN",emboss=True,icon='NEWFOLDER')
                row.operator("scene.createf",text="SAVE AS",emboss=True,icon='PASTEDOWN') 
                             
                row.enabled =  False
                row = box.row()

                #row = layout.row()
                box=row.box()
                    
                #row = layout.row()
                row = box.row()
                
                if scn.hidec:
                    row.label(text='output',icon='CONSOLE')
                    row.operator("scene.xp",text="",emboss=False,icon='ZOOMIN') 
                   
                    
                    #row.label(text=">> "+command[len(command)-1])
                    
                elif not scn.hidec:
                    row.label(text='output',icon='CONSOLE')
                    row.operator("scene.xp",text="",emboss=False,icon='ZOOMOUT') 
                                
                    box2=box.row()
                    
                    #box2= box.box()
                    for i in range(len(command)):    
                       
                        box2.label(text=">> "+command[i])
                        box2.scale_y=0.3
                        box2=box.row()
                    
#        '''==================================================================
#        
#                            OPENER BETA CLOSE
#        
#        =================================================================='''
#        
#        layout = self.layout   
#        scn = context.scene    
#        row = layout.row()
#        box = layout.box()
#         
#        row = box.row(align=True) 
#        if scn.hideopener:
#            row.operator("scene.hideo",text="",emboss=False,icon='TRIA_RIGHT') 
#            row.label(text="OPEN")
#            #row.alignment='RIGHT'
#            
#            row.operator("scene.help",text="",emboss=False,icon='HELP')
#                
#        elif not scn.hideopener:
#            #row.alignment='EXPAND'
#            row.operator("scene.hideo",text="",emboss=False,icon='TRIA_DOWN') 
#            row.label(text="OPEN")
#            #row.alignment='RIGHT'
#            
#            row.operator("scene.help",text="",emboss=False,icon='HELP')
#            row = box.row()
#            row.scale_y=1.5
#            row = box.row()
#            row.prop(context.scene,"drives",text="",icon='DISK_DRIVE')
#            #col = layout.column()
#            row = box.row()
#            row.prop(context.scene, "roots", expand=True)
#
#
#            #row = layout.row()
#
#                
#            #row = layout.row()
#                    
#            row = box.row()
#            box2 = row.box()
#            box2.label(text=" Repertoires",icon='FILE_FOLDER')
#            
#            row = box.row()
#            
#
#            
#            row.scale_y=1.5
#            row.alignment='CENTER'
#            row.operator("scene.createf",text="OPEN",emboss=True,icon='NEWFOLDER')           
#            row.enabled =  False
#            row = box.row()

"""=============================================
        
            GENERAL FUNC
        
============================================="""
class file:
    def __init__(self):
       self.name = None
       self.type = None 
       self.hide = False                       
             
def isfolder(name):
    if name.find('.') == -1:
        return True
    else:
        return False
               
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

      
def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.custom = CollectionProperty(type=CustomProp)
    bpy.types.Scene.custom_index = IntProperty()
    #bpy.utils.register_class(opening_panel)
    bpy.utils.register_class(hideo)
    bpy.utils.register_class(hide)
    bpy.utils.register_class(XP)
    bpy.utils.register_class(Help)
    bpy.utils.register_class(createF)
    bpy.utils.register_class(naming_panel)
    
def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.custom
    del bpy.types.Scene.custom_index
    #bpy.utils.register_class(opening_panel)
    bpy.utils.register_class(hideo)
    bpy.utils.register_class(hide)
    bpy.utils.register_class(XP)
    bpy.utils.register_class(Help)
    bpy.utils.register_class(createF)
    bpy.utils.unregister_class(naming_panel)
    
if __name__ == "__main__":
    initSceneProperties(bpy.context.scene)  
    register()
