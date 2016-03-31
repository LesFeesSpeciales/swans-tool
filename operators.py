# Copyright Les Fees Speciales 2015
# 
# voeu@les-fees-speciales.coop
# 
# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software.  You can  use, 
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info". 
# 
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability. 
# 
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or 
# data to be ensured and,  more generally, to use and operate it in the 
# same conditions as regards security. 
# 
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import bpy
from bpy.props import *
import os.path            #Files functions of os lib
import sys  
import addon_utils #utils to find addons path
import shutil #Used to copy files 

from . import files
from . import gui
from . import interface
from . import ressources
from . import persistence

for x in range(len(addon_utils.paths())):
    appending = sys.path.append(addon_utils.paths()[x]+'/addon/python3x') #Appending naming libs
    print(appending)


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
            #Checking if file is already existing
            if not os.path.isfile(bpy.context.scene.newF):
                print("create directories")
                interface.create_naming(bpy.context,bpy.context,'CREATE',ressources.path,ressources.command)
                p = bpy.context.scene.newF
                print("saving file to :"+str(p))  
                for x in range(0,len(addon_utils.paths())):
                    print(addon_utils.paths()[x]+'/addon/base.blend')
                    if os.path.isfile(addon_utils.paths()[x]+'/addon/base.blend'):
                        shutil.copyfile(addon_utils.paths()[x]+'/addon/base.blend',p) 
                        print("new file copied")

                        ressources.command.append("new file copied")
                        break
                    else:
                        print("copy error")
                        ressources.command.append("Copy error")
                bpy.ops.wm.open_mainfile(filepath = p)
            else:
                ressources.command.append("File already EXIST !")
        #OPENING FILES----------->            
        elif self.action == "OPEN":
            print("opening file")
            file_name =  bpy.context.scene.custom[bpy.context.scene.custom_index].name
            if len(file_name) > 3: #checking if a file is selected
                p = files.getPath(bpy.context.scene.newF)+file_name
                #Checking file existence
                if os.path.isfile(p):
                    ressources.command.append("opening file :"+str(p))
                    bpy.ops.wm.open_mainfile(filepath = p)
                    #Refresh ans asset LIST UI List before breaking
                    files.Update_ListFile(bpy.context.scene.newF)
                    interface.UpdateEnum('',ressources.Items_asset,'asset','','')
                else:
                    ressources.command.append("unknown directory :"+str(p))
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

                AddAsset

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>''' 
class add_asset(bpy.types.Operator):
    bl_idname = "scene.add_asset"
    bl_label = "add_asset"
    
    add = bpy.props.StringProperty() # defining the property

    def execute(self, context):
        #ASSET--------------------------------------------------
        if self.add == 'asset':
            interface.update_naming(self,context)
        #SQUENCE------------------------------------------------
        elif self.add == 'seq':
            ##increase the seq
            ressources.command.append("add a sequence")
            max = 0
            num_seq = ""
            n_num_seq = 0

            #Find the next seq number
            for i in range(len(ressources.Items_seq)):
                if ressources.Items_seq[i][0]!='none':
                    for z in range(1,len(ressources.Items_seq[i][0])):
                        num_seq = num_seq + ressources.Items_seq[i][0][z]
                    n_num_seq = int(num_seq)
                    if n_num_seq>=max:
                        max = n_num_seq
                    num_seq = ""
                
            max = max + 1
 
            bpy.context.scene.seqn = max

            if bpy.context.scene.sequence:
                bpy.context.scene.sequence = False
            else:
                bpy.context.scene.sequence = True
            print('update sequence')
        #SHOT------------------------------------------------------------
        elif self.add == 'shot':
            ##increase the seq
            ressources.command.append("add a shot")
            max = 0
            num_shot = ""
            n_num_shot = 0

            for i in range(len(ressources.Items_shot)):
                if ressources.Items_shot[i][0]!='none':
                    for z in range(1,len(ressources.Items_shot[i][0])):
                        num_shot = num_shot + ressources.Items_shot[i][0][z]
                    n_num_shot = int(num_shot)
                    if n_num_shot>=max:
                        max = n_num_shot
                    num_shot = ""
                
            max = max + 1
            bpy.context.scene.shotn = max

            if bpy.context.scene.shoth:
                bpy.context.scene.shoth = False
            else:
                bpy.context.scene.shoth = True
            print('update shot')
        elif self.add == 'check_sequence':
            temp = bpy.context.scene.seqn
            temp = str(temp)

            while len(temp) < 3:
                temp = '0'+temp
                    
            temp = 'S'+temp
            tp = (str(temp),str(temp),'')
            if tp not in ressources.Items_seq:
                ressources.Items_seq.append(tp)
                interface.UpdateEnum('',ressources.Items_seq,'seq',temp,temp)
                bpy.context.scene.seq = temp
                bpy.context.scene.shot = 'none'
                bpy.context.scene.sequence = False
            else:
                ressources.command.append("Sequence already exist")
        elif self.add == 'check_shot':
            temp = bpy.context.scene.shotn
            temp = str(temp)

            while len(temp) < 3:
                temp = '0'+temp
                    
            temp = 'P'+temp
            tp = (str(temp),str(temp),'')
            if tp not in ressources.Items_shot:
                ressources.Items_shot.append(tp)
                interface.UpdateEnum('',ressources.Items_shot,'shot',temp,temp)
                bpy.context.scene.shot = temp
                bpy.context.scene.shoth = False
            else:
                ressources.command.append("Shot already exist")
        return {"FINISHED"}

'''<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

                OPEN DIR OPERATOR

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>''' 
class OBJECT_OT_custompath(bpy.types.Operator):
    bl_idname = "object.custom_path"
    bl_label = "open"
    __doc__ = ""   
    
    filename_ext = ""
    filter_glob = StringProperty(default="", options={'HIDDEN'},subtype='DIR_PATH')    
        
    #this can be look into the one of the export or import python file.
    #need to set a path so so we can get the file name and path
    filepath = StringProperty(name="File Path", description="Filepath importing store dir", maxlen= 1024, default= "")
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
        
        #Save the config of drives
        persistence.write_config()
        
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
    bpy.utils.register_class(add_asset)
    bpy.utils.register_class(OBJECT_OT_custompath)

def unregister():
    bpy.utils.unregister_class(DialogOperator)
    bpy.utils.unregister_class(file_op)
    bpy.utils.unregister_class(add_asset)
    bpy.utils.unregister_class(OBJECT_OT_custompath)
