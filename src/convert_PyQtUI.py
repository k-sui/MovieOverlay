# -*- coding: utf-8 -*-
from PyQt4 import uic
 
import codecs

fin = codecs.open('movieOverlayUI.ui', 'r', 'utf-8')
fout = codecs.open('movieOverlayUI.py', 'w', 'utf-8')
uic.compileUi(fin,fout,execute=False)
fin.close()
fout.close()