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

import sys                #System Libraries
import os
from json import dumps, load

from . import ressources

def load_config():
    print('try to load config from file')
    ressources.command.append('Trying to load the store config')
    homedir = os.path.expanduser('~')
    path = homedir + '/' +'config_opener'
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
    
    except:
        ressources.command.append('Config not found create it')
        #write new default conf
        with open(path, "w+") as file:
            file.write(dumps({'store':ressources.Items}, file, indent=1))
        file.close() 

        return False

def write_config():
    #Vars
    homedir = os.path.expanduser('~')
    path = homedir + '/' +'config_opener'

    print('saving config for next startup')
    ressources.command.append('Trying to save the store config')

    with open(path, "w+") as file:
        file.write(dumps({'store':ressources.Items}, file, indent=1))
    file.close()

