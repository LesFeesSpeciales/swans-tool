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
from json import dumps, load

def load_config(dir):
    print('try to load config from file')
    n = [1, 2, 3]
    s = ["a", "b" , "c"]
    x = 0
    y = 0

    with open(dir, "r") as file:
        print(file.readlines())
    with open("text", "w") as file:
        dumps({'numbers':n, 'strings':s, 'x':x, 'y':y}, file, indent=4)
    file.close()

    with open("text") as file:
        result = load(file)
    file.close()
    print (type(result))
    print (result.keys())
    print (result)

def write_config():
    print('saving config for next startup')

