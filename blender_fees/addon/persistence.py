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
import sys                #System Libraries
import os
from json import dumps, load
from bpy.props import IntProperty, CollectionProperty #, StringProperty 
from bpy.types import Panel, UIList #Some UI Blender Libs

from . import ressources
from . import files

#...................................
#         load_config              #
#                                  #
#   load the config of the store   #
#               dir                #
#...................................
def load_config():
    print('try to load config from file')
    ressources.command.append('Trying to load the store config')
    homedir = os.path.expanduser('~')
    path = homedir + '/' +'config_opener'

    #If the file exist then read it
    try:
        with open(path,'r+') as file:
            result = load(file)
        file.close()

        print ('result:'+str(type(result)))
        print (result.keys())
        print (result)
        t  = []
        for i in range(len(result['store'])):
            t.append(tuple(result['store'][i]))

        ressources.Items = t
        ressources.command.append('Success')

        return True    
    #Else wrote it
    except:
        ressources.command.append('Config not found create it')
        #write new default conf
        with open(path, "w+") as file:
            file.write(dumps({'store':ressources.Items}, file, indent=1))
        file.close() 

        return False

#...................................
#         write_config             #
#                                  #
#   write the config of the        #
#           Store                  #
#...................................
def write_config():
    #Vars
    homedir = os.path.expanduser('~')
    path = homedir + '/' +'config_opener'

    print('saving config for next startup')
    ressources.command.append('Trying to save the store config')

    with open(path, "w+") as file:
        file.write(dumps({'store':ressources.Items}, file, indent=1))
    file.close()

#...................................
#         load_asset               #
#                                  #
#   load assets from directory     #
#...................................
def load_asset():
    print('Load asset from files')

    #list subdir from libs dir
    root = bpy.context.scene.drives + ressources.path['Lib']+'/'
    print('root:'+root)

    if os.path.isdir(root):
        dir_to_go = files.listdirs(root)
        print(dir_to_go)
        asset = []

        for folder in dir_to_go:
            a = files.listdirs(folder)
            print(a)
            for x in range(len(a)):
                if sys.platform != 'win32':   
                    if a[x].split('/')[len(a[x].split('/'))-1] not in asset:
                        asset.append(a[x].split('/')[len(a[x].split('/'))-1])
                else:
                    if a[x].split('\\')[len(a[x].split('\\'))-1] not in asset:
                        asset.append(a[x].split('\\')[len(a[x].split('\\'))-1])
        print("ASSET:")
        print(asset)

    else:
        asset.append('none')


    return asset

#...................................
#         load_sequences           #
#                                  #
#   load sequences from directory  #
#...................................
def load_seq():
    print('Load seq from files')

    #list subdir from libs dir
    if sys.platform != 'win32':  
        root = bpy.context.scene.drives + ressources.path['Film']+'/'
    else:
        root = bpy.context.scene.drives + ressources.path['Film']+'\\'
    print('root:'+root)

    if os.path.isdir(root):
        seq = []

        a = files.listdirs(root)
        print(a)
        for x in range(len(a)):
            if sys.platform != 'win32':   
                if a[x].split('/')[len(a[x].split('/'))-1] not in seq:
                    seq.append(a[x].split('/')[len(a[x].split('/'))-1])
            else:
                if a[x].split('\\')[len(a[x].split('\\'))-1] not in seq:
                    seq.append(a[x].split('\\')[len(a[x].split('\\'))-1])
        print("SEQUENCE:")
        print(seq)

    else:
        seq.append('none')


    return seq

#...................................
#         load_shots               #
#                                  #
#   load shots  from directory     #
#...................................
def load_shots():
    print('Load shot from files')

    #list subdir from libs dir
    if sys.platform != 'win32':  
        root = bpy.context.scene.drives + ressources.path['Film']+'/'+bpy.context.scene.seq+'/'
    else:
        root = bpy.context.scene.drives + ressources.path['Film']+'\\'+bpy.context.scene.seq+'\\'
    print('root:'+root)

    shot = []
    if os.path.isdir(root):
        

        a = files.listdirs(root)
        print(a)
        for x in range(len(a)):
            if sys.platform != 'win32':   
                if a[x].split('/')[len(a[x].split('/'))-1] not in shot:
                    shot.append(a[x].split('/')[len(a[x].split('/'))-1])
            else:
                if a[x].split('\\')[len(a[x].split('\\'))-1] not in shot:
                    shot.append(a[x].split('\\')[len(a[x].split('\\'))-1])
        print("shot:")
        print(shot)

    else:
        shot.append('none')


    return shot
