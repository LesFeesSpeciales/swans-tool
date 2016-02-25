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

import os.path
from bpy.props import IntProperty, CollectionProperty #, StringProperty 
from bpy.props import *   #Blender properties lib

'''-----------------------------------------------

             FILES FUNC 

----------------------------------------------'''
#...................................
#         getVersion               #
#                                  #
#   Get the actual version         #
#...................................
def getVersion(path_to_file):
    files = path_to_file.split("-")
    version=''
        
    print(dir)
    t = files[len(files)-1].split('.')
    
    print("t:"+str(t))
    
    if len(t)>1:               
        version = t[0].split('v')[1]
    print('version during getting it:'+version)
    
    if version != '':
        version = int(version)
        print(str(version))
    else:
        version ='none'
    print('Get Version'+ str(version)) #Debug things
        
    return version

#...................................
#         increaseVersion          #
#                                  #
#   Get the actual version         #
#...................................
def increaseVersion(path_to_file):     
    files = path_to_file.split("-")
    dir = ''
    
    for j in range(len(files)-1):
        dir = dir+files[j]+'-'
        
    print(dir)
    t = files[len(files)-1].split('.')
    
    print("t:"+str(t))
                   
    version = t[0].split('v')[1]
    print(version)
    version = int(version)
    print(version)
    version = version + 1
    print('version:'+str(version))
    if version > 9:
        file = dir + 'v'+ str(version)
    else:
        file = dir +'v0' +str(version)
    print(file)
    p = file+".blend" #Adding extention
    
    return p

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

#...................................
#         update_list_file         #
# ..................................
def Update_ListFile(dir):
    bpy.context.scene.custom.clear() #Clearing scene 
    
    dir = bpy.context.scene.newF.split('/')
    directory = ''
    #making dir
    for i in range(len(dir)-1):
        directory = directory + dir[i]+'/'
    #Checking dir existence
    if os.path.isdir(directory):
        list = listFiles(directory,".blend")
        print(directory)
        print(list)
        
        for i in range(len(list)):
            bpy.context.scene.custom.add() #Adding new empty file to the ui list
            bpy.context.scene.custom[i].name = list[i] #Fill it with info : name

        ressources.command.append("Files successfull listed")
    else:
        bpy.context.scene.custom.clear()
        ressources.command.append("Folder empty")

#...................................
#         getPath                  #
# get the path of the file dir     #
# ..................................
def getPath(dir):
    d = dir.split('/')
    directory = ''
    for i in range(len(d)-1):
        directory = directory +d[i]+ '/'

    print('get dir:'+directory)

    return directory

#...................................
#         listdirs                 #
#                                  #
#   List the forlders or a dir     #
#...................................
def listdirs(dir):
    return [os.path.join(os.path.join(dir, x)) for x in os.listdir(dir) 
        if os.path.isdir(os.path.join(dir, x))]
