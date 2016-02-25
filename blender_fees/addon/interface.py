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

from . import ressources
from . import files
from . import persistence


from bpy.props import *
from bpy.props import IntProperty, CollectionProperty #, StringProperty 
from bpy.types import Panel, UIList #Some UI Blender Libs
import addon_utils #utils to find addons path
import sys, os

addon_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(addon_dir, 'python3x')) #Appending naming libs
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

        
