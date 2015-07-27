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
      