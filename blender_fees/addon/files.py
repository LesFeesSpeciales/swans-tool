
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
import os.path


'''-----------------------------------------------

             FILES FUNC 

----------------------------------------------'''
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

