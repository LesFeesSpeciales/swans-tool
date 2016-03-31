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
from bpy.props import IntProperty, CollectionProperty #, StringProperty 
from bpy.types import Panel, UIList #Some UI Blender Libs

import os.path            #Files functions of os lib
import sys  

from . import files
from . import interface
from . import ressources


'''<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

                     File UIList
            Stock the file list into the UI
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''

# return name of selected object
def get_activeSceneObject():
    return bpy.context.scene.objects.active.name

# custom list to display files into Tools
class UL_items(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(0.6)
        split.prop(item, "name", text="", emboss=False, translate=False, icon='FILE')
       

    def invoke(self, context, event):
        pass   

# Create custom property group
class CustomProp(bpy.types.PropertyGroup):
    name = StringProperty() 
    id = IntProperty()


'''<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<item

                GUI CREATION

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>''' 
def enable(x):
    if bpy.context.scene.drives == 'none':
        x.enabled = False
    else:
        x.enabled=True

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
        #Example of external drawing function: draw_opener(self,bpy.context,ressources.command)
        
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

            enable(row)

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
                subrow = sub.row(align=True)

                enable(subrow)

                subrow.prop(scn, "seq",expand=False,text='')
                
                

                if scn.sequence:
                    subrow.operator("scene.add_asset",text="", icon='MOVE_UP_VEC').add = 'seq'
                    subrow = sub.row(align=True)
                    if scn.shoth or scn.drives=='none':
                        subrow.enabled = False
                    else : 
                        subrow.enabled = True
                    subrow.prop(scn, "seqn")
                    subrow.operator("scene.add_asset",text="", icon='PLUS').add = 'check_sequence'
                else:
                    if scn.shoth or scn.drives=='none':
                        subrow.enabled = False
                    else : 
                        subrow.enabled = True
                    subrow.operator("scene.add_asset",text="", icon='MOVE_DOWN_VEC').add = 'seq'
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
                subrow = sub.row(align=True)
                enable(subrow)
                subrow.prop(scn, "shot",expand=False,text='')
                if scn.shoth:
                    subrow.operator("scene.add_asset",text="", icon='MOVE_UP_VEC').add = 'shot'
                    subrow = sub.row(align=True)
                    if scn.sequence or scn.drives=='none':
                        subrow.enabled = False
                    else : 
                        subrow.enabled = True
                    subrow.prop(scn, "shotn")
                    subrow.operator("scene.add_asset",text="", icon='PLUS').add = 'check_shot'
                else:
                    if scn.sequence or scn.drives=='none' :
                        subrow.enabled = False
                    else : 
                        subrow.enabled = True
                    subrow.operator("scene.add_asset",text="", icon='MOVE_DOWN_VEC').add = 'shot'
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
                
                enable(row)
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
                enable(sub)
                sub.prop(scn, "asset",expand=False,text='')
                if scn.asset == 'other':
                  subrow = sub.row(align=True)
                  subrow.prop(scn, "newA")
                  subrow.operator("scene.add_asset",text="", icon='PLUS').add = 'asset'
                
                row = box.row()
                
            #dpt setting----------------------------------
            split = row.split(align=True)
            col = split.column()
           
            if(scn.dpt=='none'):
                col.label(text=" DPT",icon='QUESTION')
            else:
                col.label(text=" DPT",icon='FILE_TICK')
            
            sub = col.column(align=True)
            enable(sub)
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
            enable(row)
            row.operator("scene.file_op",text="NEW",emboss=True,icon='FILE').action = "NEW" 
            row.operator("scene.file_op",text="SAVE AS",emboss=True,icon='PASTEDOWN').action = "SAVE_AS" 
            row.operator("scene.file_op",text="OPEN",emboss=True,icon='COPYDOWN').action = "OPEN"
            
            
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
                for i in range(len(ressources.command)-1,-1,-1):    
                    box2.label(text=">> "+ressources.command[i])
                    box2.scale_y=0.3
                    box2=box.row()
  
def register():

    bpy.types.Scene.custom = CollectionProperty(type=CustomProp)
    bpy.types.Scene.custom_index = IntProperty()

def unregister():
    del bpy.types.Scene.custom
    del bpy.types.Scene.custom_index    
