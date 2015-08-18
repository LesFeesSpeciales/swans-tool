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

from . import ressources
from . import files
from . import persistence


from bpy.props import *
from bpy.props import IntProperty, CollectionProperty #, StringProperty 
from bpy.types import Panel, UIList #Some UI Blender Libs
import addon_utils #utils to find addons path
import sys

for x in range(len(addon_utils.paths())):
    appending = sys.path.append(addon_utils.paths()[x]+'/addon/python3x') #Appending naming libs
    print(appending)
import naming.Herakles as naming   #Import naming 

'''-----------------------------------------------

         INTERFACE NAMING/SCRIPT FUNCTIONS 

----------------------------------------------'''

#...................................
#         Create_naming            #
#                                  #
#   Create the basic naming        #
#       object and use it          #
#...................................
def create_naming(self,context,op, path,command):
    #Generate naming Object
    n = naming.StoreFolder.from_name(path['Store'])
    #Allowing dico
    c =n(**path)
    print(c.path()) 
    command.append(c.path())
    #bpy.context.scene.wild  = c.is_wild()        
    if op == 'CREATE':
        print("Create missing folders with naming...")
        c.create()
        print("done.")
        c.config()
    c.config()
    print("Naming path ----------------------->"+c.path())
    print('newwF:'+bpy.context.scene.newF)
    #print("the way is wild : "+is_wild)
    return str(c.path())

#...................................
#         update_naming            #
#                                  #
#   update the basic naming        #
#       object and use it          #
#...................................
def update_naming(self, context):
    print('Update naming')
    temp = ressources.path.copy()
    
    ressources.path.clear()
    n=''
    dest=""
    new = False
    
    #GET Store and project field from the file explorer
    if sys.platform == 'win32':
        dest = bpy.context.scene.drives.split('\\')
    else:
        dest = bpy.context.scene.drives.split('/')
            
    for i in range(len(dest)-2):
        n = n + dest[i]+'/'
    if sys.platform != 'win32':   
        ressources.path['Store']='/'+n
    else:
        ressources.path['Store']=n
    ressources.path['Project']=dest[len(dest)-2]
    
    #DEBUG things
    print("project:"+dest[len(dest)-2] )
    print("store : "+n)

    if bpy.context.scene.roots == 'LIB':
        ressources.path['Lib'] = 'LIB'
        ressources.path['Family']=bpy.context.scene.famille
        if bpy.context.scene.asset == 'other':
            tempAsset = (str(bpy.context.scene.newA),str(bpy.context.scene.newA),'')
            if tempAsset not in ressources.Items_asset:
                ressources.path['Asset']=bpy.context.scene.newA
                ressources.Items_asset.append((str(bpy.context.scene.newA),str(bpy.context.scene.newA),''))
                UpdateEnum('',ressources.Items_asset,'asset','','')
                bpy.context.scene.asset = bpy.context.scene.newA
                #bpy.context.scene.newA ="none"
            else:
                bpy.context.scene.newA = ""
          
        else:
            ressources.path['Asset']=bpy.context.scene.asset
        ressources.path['Dept']=bpy.context.scene.dpt
    elif bpy.context.scene.roots =='MOVIE':
        ressources.path['Film'] = 'FILM'
        ressources.path['Sequence'] = bpy.context.scene.seq
        ressources.path['Shot'] = bpy.context.scene.shot
        ressources.path['Dept'] = bpy.context.scene.dpt
    
    if 'Version' in temp:
        ressources.path['Version']=temp['Version']
    
    #Setup version and extention
    v = files.getVersion(bpy.data.filepath)
    if (v == 'none') or (ressources.path != temp):
        ressources.path['Version'] = 'v00'
    else:
        if v < 10:
            ressources.path['Version'] = 'v0'+str(v)
        else:
            ressources.path['Version'] = 'v'+str(v)

    change = False
    #Upgrade asset
    if (bpy.context.scene.famille != 'none') and (bpy.context.scene.roots != 'MOVIE') and (bpy.context.scene.drives != 'none'):
        temps = persistence.load_asset()
        for i in range(len(temps)):
            y = (str(temps[i]),str(temps[i]),'')
            if y not in ressources.Items_asset:
                ressources.Items_asset.append((str(temps[i]),str(temps[i]),''))
        UpdateEnum('',ressources.Items_asset,'asset','','')
    #Upgrade sequence
    elif (bpy.context.scene.roots == 'MOVIE') and (bpy.context.scene.drives != 'none') and (temp['Dept'] == ressources.path['Dept']) and ('Shot' in temp) and ('Sequence' in temp):
        temps = persistence.load_seq()
        for i in range(len(temps)):
            y = (str(temps[i]),str(temps[i]),'')
            if y not in ressources.Items_seq:
                ressources.Items_seq.append((str(temps[i]),str(temps[i]),''))
                change = True
        if change:
            UpdateEnum('',ressources.Items_seq,'seq','','none')
            bpy.context.scene.shot = ressources.Items_shot[0][0] 
        elif temp['Shot'] == bpy.context.scene.shot:
            temps = persistence.load_shots()
            ressources.Items_shot.clear()
            ressources.Items_shot.append(('none','none',''))
            for i in range(len(temps)):
                y = (str(temps[i]),str(temps[i]),'')
                if y not in ressources.Items_shot:
                    ressources.Items_shot.append((str(temps[i]),str(temps[i]),''))
            UpdateEnum('',ressources.Items_shot,'shot','','none') 
    
    change=False

    ressources.path['Extension'] = 'blend' 
    print('newwF:'+bpy.context.scene.newF)
    
    try:
        bpy.context.scene.newF = create_naming(self,context,'',ressources.path,ressources.command)   
        files.Update_ListFile(bpy.context.scene.newF)
    except:
        print('naming no setup, clearing list')
        bpy.context.scene.custom.clear() #Clearing scene 
        ressources.command.append("! missing field !")
    
    return None

#...................................
#         Update enum              #
#                                  #
#   Update th eenum propertie      #
#...................................
def UpdateEnum(Enums,Items,Name,Description,Defaults):
    print("update file list")
    print('updating:'+Name)   
    print('name:'+Name+' Description:'+Description)
    print('Items:'+str(tuple(Items)))
    if Name == 'Store': 
        bpy.types.Scene.drives= EnumProperty(
            name=Name,
            description=Description,
            items=tuple(Items),
            default=Defaults,
            update=update_naming)  
    elif Name == 'asset':
        bpy.types.Scene.asset= EnumProperty(
            name=Name,
            description=Description,
            items=tuple(Items),
            default='none',
            update=update_naming)
    elif Name == 'seq':
        bpy.types.Scene.seq= EnumProperty(
            name=Name,
            description=Description,
            items=tuple(Items),
            default=Defaults,
            update=update_naming)
    elif Name == 'shot':
        bpy.types.Scene.shot = EnumProperty(
            name=Name,
            description=Description,
            items=tuple(Items),
            default=Defaults,
            update=update_naming)

        