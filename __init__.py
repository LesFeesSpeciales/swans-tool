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


bl_info = {
    "name": "Les Fees Speciales",
    "author":"Les Fees Speciales",
    "version":(1,0),
    "location": "Tools ",
    "description":"File management tool for production",
    "wiki_url":"http://les-fees-speciales.coop/wiki/",
    "category":"Production"
}


import imp

try:
    imp.reload(ressources)
    imp.reload(gui)
    imp.reload(interface)
    imp.reload(files)
    imp.reload(operators)
    imp.reload(persistence)

except:
    from . import ressources 
    from . import gui
    from . import interface
    from . import files
    from . import operators
    from . import persistence

from pprint import pprint #Lib to print dictionnaries
import addon_utils        #utils to find addons path
import bpy                #Blender Libpython3
import os.path            #Files functions of os lib
from bpy.props import *   #Blender properties lib
import sys                #System Libraries
import json


addon_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(addon_dir, 'python3x')) #Appending naming libs
import naming.Herakles as naming   #Import naming 

from bpy.props import IntProperty, CollectionProperty #, StringProperty 
from bpy.types import Panel, UIList #Some UI Blender Libs
import shutil #Used to copy files 


"""_______________________HELP SECTION________________________________

PROP OPTION:
    prop(data, properties, text="", text_ctxt="", translate=True, icon='NONE', expand=False, slider=False, toggle=False, icon_only=False, event=False, full_event=False, emboss=True, index=-1, icon_value=0)

LAYOUT INFO:
    http://www.blender.org/api/blender_python_api_2_69_3/bpy.types.UILayout.html#bpy.types.UILayout
test:
___________________________________________________________________"""

properties = []#contain all props in a near futur.....

#-----NAMING VARS-------
drives = (('Store',"Store directory",''),('/u/Project/',"/u/Project/",''),('test2_1',"test2_2",''),('',"",''))
asset = (('asset',"/lib/type/famille/asset",''),('criquet', "criquet", ""),('plantes', "plantes", ""),('arbres', "arbres", ""),('other', "other", ""))
seq = (('seq',"sequence",''),('S001',"S001",''),('S002',"S002",''))
shot = (('shot',"shot",''),('P001',"P001",''),('P002',"P002",''))

is_wild = 'True'

#adding 
properties.append(drives)
properties.append(asset)
properties.append(seq)
properties.append(shot)
      
#...................................
#         initSceneProperties      #
#                                  #
#   Init the scene properties      #
#...................................
def initSceneProperties():
     #PROJECT DIR----------------------------->
     bpy.types.Scene.drives = EnumProperty(name="none",description="none",items=(('')),update=interface.update_naming)
     bpy.types.Scene.asset = EnumProperty(name="none",description="none",items=(('')))
     bpy.types.Scene.seq = EnumProperty(name="none", description="none", items=(('')), update = interface.update_naming)
     bpy.types.Scene.shot = EnumProperty(name="none", description="none", items=(('')), update = interface.update_naming) 
     bpy.types.Scene.subtypes = EnumProperty(name="subtype", description="subtype", items=((''))) 
    
     s = len(properties)
     
     ressources.Items.append(('none',"none",""))
     ressources.Items_asset.append(('none',"none",""))
     ressources.Items_seq.append(('none',"none",""))
     ressources.Items_shot.append(('none',"none",""))
   

     for i in range(s):
        #Setup store dir
        if properties[i][0][0] == 'Store': 
            if not persistence.load_config():      
                for line in range(1,len(properties[i])):
                    ressources.Items.append((str(properties[i][line][0]),str(properties[i][line][1]),str(properties[i][line][2])))         
            interface.UpdateEnum(bpy.types.Scene,ressources.Items,properties[i][0][0],properties[i][0][1],ressources.Items[0][0])    
        
        #Setup assets
        elif properties[i][0][0] == 'asset':
            for line in range(1,len(properties[i])):
                ressources.Items_asset.append((str(properties[i][line][0]),str(properties[i][line][1]),str(properties[i][line][2])))         
                print(ressources.Items_asset)
            interface.UpdateEnum(bpy.types.Scene,ressources.Items_asset,properties[i][0][0],properties[i][0][1],ressources.Items_asset[0][0])
        
        #Setup sequences
        elif properties[i][0][0] == 'seq':
            for line in range(1,len(properties[i])):
                ressources.Items_seq.append((str(properties[i][line][0]),str(properties[i][line][1]),str(properties[i][line][2])))         
                print(ressources.Items_seq)
            interface.UpdateEnum(bpy.types.Scene,ressources.Items_seq,properties[i][0][0],properties[i][0][1],ressources.Items_seq[0][0])

         #Setup shots
        elif properties[i][0][0] == 'shot':
            for line in range(1,len(properties[i])):
                ressources.Items_shot.append((str(properties[i][line][0]),str(properties[i][line][1]),str(properties[i][line][2])))         
                print(ressources.Items_shot)
            interface.UpdateEnum(bpy.types.Scene.shot,ressources.Items_shot,properties[i][0][0],properties[i][0][1],ressources.Items_shot[0][0])
     
     #ROOT----------------------------->
     bpy.types.Scene.roots = EnumProperty(
        name="Root",
        description="root",
        items=(('LIB', "LIB", ""),
               ('MOVIE', "MOVIE", ""),
               ('', "", "")),
        default='LIB',
        update = interface.update_naming)  
        
     #FAMILY----------------------------------->
     bpy.types.Scene.famille = EnumProperty(
        name="famille",
        description="/lib/type/famille",
        items=(('Chars', "Chars", ""),
               ('Props', "Props", ""),
               ('Sets', "Sets", ""),
               ('Lookdev', "Lookdev", ""),
               ('none', "none", "")),
        default='none',
        update = interface.update_naming)
        
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
               ('Vfx', "Vfx", ""),
               ('Shad', "Shad", "")),
        default='none',
        update = interface.update_naming) 

     bpy.types.Scene.newF = StringProperty(
        name="",
        subtype = 'FILE_NAME',
        description="new familly",
        maxlen= 500,
        default= "")
     bpy.types.Scene.newA = StringProperty(
        name="",
        description="new asset",
        maxlen= 50,
        default= "")
     bpy.types.Scene.newS = StringProperty(
        name="",
        description="new sequence",
        maxlen= 50,
        default= "")
     #HIDING BOOLEANS------------------------->
     bpy.types.Scene.hidec = BoolProperty(
        name = "hidec", 
        default=False,
        description = "hide console")
     bpy.types.Scene.wild = BoolProperty(
        name = "is_wild", 
        default=False,
        description = "is the path valid")
     bpy.types.Scene.sequence = BoolProperty(
        name = "is_wild", 
        default=False,
        description = "is the path valid")
     bpy.types.Scene.shoth = BoolProperty(
        name = "is_wild", 
        default=False,
        description = "is the path valid")
     bpy.types.Scene.hidecreator = BoolProperty(
        name = "hidec", 
        default=False,
        description = "hide console")
     bpy.types.Scene.seqn = IntProperty(
        min=0,
        max=999,
        name = "Sequence", 
        default=0,
        description = "sequence number")
     bpy.types.Scene.shotn = IntProperty(
        min=0,
        max=999,
        name = "Shot", 
        default=0,
        description = "Shot number")
'''---------------------------------------------------

                Basic function 
                     

---------------------------------------------------'''

def register():
    initSceneProperties() 
    operators.register()
    bpy.utils.register_module(__name__)
    gui.register()
   
def unregister():   
    bpy.utils.unregister_module(__name__)
    gui.unregister()
    del bpy.types.Scene.roots
    del bpy.types.Scene.famille
    del bpy.types.Scene.asset
    del bpy.types.Scene.drives
    del bpy.types.Scene.dpt
    del bpy.types.Scene.seq
    del bpy.types.Scene.shot
    del bpy.types.Scene.newF
    del bpy.types.Scene.newA
    del bpy.types.Scene.newD
    del bpy.types.Scene.hidec
    del bpy.types.Scene.wild
    del bpy.types.Scene.hidecreator

if __name__ == "__main__":
    register()
