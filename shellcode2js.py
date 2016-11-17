#!/usr/bin/env python

# 
# Converter from a C style shellcode or binary file containing the shellcode to escaped Javascript shellcode
#
# http://eternal-todo.com
# Jose Miguel Esparza
#

import sys,os

usage = "Usage: "  + sys.argv[0] + ''' shellcode|file

Arguments:

    shellcode: C style shellcode.
    file: binary file containing the shellcode.
'''
jsshellcode = ""
tmp = ""
cont = 0

if len(sys.argv) != 2:
   sys.exit(usage)

if os.path.exists(sys.argv[1]):
   shellcode = open(sys.argv[1],'r').read()
else:
   shellcode = sys.argv[1]
   for i in range(2,len(shellcode),4):
      chars = shellcode[i]+shellcode[i+1]
      tmp += chr(int(chars,16))
   shellcode = tmp

for i in range(0,len(shellcode)-1,2):
   if i%16 == 0:
      if cont == 0:
         jsshellcode += '"'
         cont += 1
      else:
         jsshellcode += '"+\n"'
   jsshellcode += "%%u%.2x%.2x" % (ord(shellcode[i+1]),ord(shellcode[i]))
print jsshellcode+'"'
