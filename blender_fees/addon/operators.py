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


import bpy
from bpy.props import *
import os.path            #Files functions of os lib
import sys  
from . import files
from . import gui
from . import interface
from . import ressources
from . import __init__


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

                hide console

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''         
class XP(bpy.types.Operator):
    bl_idname = "scene.xp"
    bl_label = "xp"
    
    def execute(self, context):
        if context.scene.hidec:
            context.scene.hid,commandec = False
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

                DIALOG OPERATOR

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>''' 
class DialogOperator(bpy.types.Operator):
    bl_idname = "object.dialog_operator"
    bl_label = "File already exist, overwrite or change version"
    
    increase_version = BoolProperty(name="Increase Version")
    overwrite = BoolProperty(name="Overwrite")

    def execute(self, context):
        scn = context.scene
        
        #If the user want to overwrite
        if self.overwrite:
            print("overwrite")
            p = bpy.context.scene.newF
            bpy.ops.wm.save_as_mainfile(filepath=p) 
            
        #IF user want to add version
        if self.increase_version:  
            print("Increase version")
            
            ######################
            path = files.increaseVersion(bpy.context.scene.newF)
            
            while os.path.isfile(path):
                print("FILE ALREADY EXIST ERASE IT")
                path = files.increaseVersion(path)
                
            bpy.ops.wm.save_as_mainfile(filepath=path) 
            print('save as:'+path)

        files.Update_ListFile(bpy.context.scene.newF)   
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

'''<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

                FILE OPERATOR

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>''' 
class file_op(bpy.types.Operator):
    bl_idname = "scene.file_op"
    bl_label = "file_op"
    
    action = bpy.props.StringProperty() # defining the property
    
    def execute(self, context):
        #CREATING NEW FILES------>
        if self.action == "NEW": 
            print("create directories")
            interface.create_naming(bpy.context,bpy.context,'CREATE',ressources.path,ressources.command)
            p = bpy.context.scene.newF
            print("saving file to :"+str(p))  
            for x in range(0,len(addon_utils.paths())):
                print(addon_utils.paths()[x]+'/addon/base.blend')
                if os.path.isfile(addon_utils.paths()[x]+'/addon/base.blend'):
                    shutil.copyfile(addon_utils.paths()[x]+'/addon/base.blend',p) 
                    print("new file copied")
                    break
                else:
                    print("copy error")
            bpy.ops.wm.open_mainfile(filepath = p)
                
        #OPENING FILES----------->            
        elif self.action == "OPEN":
            print("opening file")
            file_name =  bpy.context.scene.custom[bpy.context.scene.custom_index].name
            if len(file_name) > 3: #checking if a file is selected
                p = files.getPath(bpy.context.scene.newF)+file_name
                bpy.ops.wm.open_mainfile(filepath = p)
            else:
                print('no file selected')
            
        #SAVE8AS FILES----------->
        elif self.action == "SAVE_AS":
            file_name = bpy.context.scene.newF.split("/")
            p = bpy.context.scene.newF
            if os.path.isfile(p):
                ressources.command.append("File already exist")
                bpy.ops.object.dialog_operator('INVOKE_DEFAULT') #calls the popup
            else:
                ressources.command.append("saving file to :"+str(p))
                interface.create_naming(bpy.context,bpy.context,'CREATE',ressources.path,ressources.command)
                print("saving file to :"+str(p))  
                bpy.ops.wm.save_as_mainfile(filepath=p)    
                
            files.Update_ListFile(bpy.context.scene.newF)
            #__init__.update_naming(self,context)
        return {"FINISHED"}

'''<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

                OPEN DIR OPERATOR

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>''' 
class OBJECT_OT_custompath(bpy.types.Operator):
    bl_idname = "object.custom_path"
    bl_label = "open"
    __doc__ = ""   
    
    filename_ext = ""
    filter_glob = StringProperty(default="", options={'HIDDEN'})    
        
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
        #bpy.context.scene.newF = self.properties.filepath     
        
        print("*************SELECTED FILES ***********")
        for file in self.files:
            print(file.name)
        
        print("FILEPATH %s"%self.properties.filepath)#display the file name and current path    
        ressources.Items.append((str(self.properties.filepath),str(self.properties.filepath),""))
        interface.UpdateEnum(bpy.types.Scene,ressources.Items,'Store',str(self.properties.filepath),str(self.properties.filepath))
        return {'FINISHED'}

    def draw(self, coitemntext):
        self.layout.operator('file.select_all_toggle')        
    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

        

def register():
    bpy.utils.register_class(DialogOperator)
    bpy.utils.register_class(file_op)
    bpy.utils.register_class(OBJECT_OT_custompath)

def unregister():
    bpy.utils.unregister_class(DialogOperator)
    bpy.utils.unregister_class(file_op)
    bpy.utils.unregister_class(OBJECT_OT_custompath)