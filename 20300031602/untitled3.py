# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 19:31:22 2022

@author: LENOVO
"""

from PyQt5 import uic

with open('derstakipUI.py', 'w', encoding="utf-8") as fout:
   uic.compileUi('untitled.ui', fout)