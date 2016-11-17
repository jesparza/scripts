#!/usr/bin/env python

# 
# Little script to obtain a printable (C style) shellcode from the escaped Javascript code.
# It also writes to shellcode.out the resulted bytes.
#
# http://eternal-todo.com
# Jose Miguel Esparza
#


import sys

usage = "Usage: "+sys.argv[0]+''' js_shellcode

Arguments:

    js_shellcode: escaped Javascript shellcode.
'''
shellcode = ""
printableShellcode = ""
hexchar = ""
cont = 0

if len(sys.argv) != 2:
   sys.exit(usage)

jsshellcode = sys.argv[1]

for i in range(2,len(jsshellcode)-1,6):
   shellcode += chr(int(jsshellcode[i+2]+jsshellcode[i+3],16))+chr(int(jsshellcode[i]+jsshellcode[i+1],16))
   if cont == 0:
      printableShellcode += '"' 
   elif cont%8 == 0:
      printableShellcode += '"+\n"'
   printableShellcode += "\\x"+jsshellcode[i+2]+jsshellcode[i+3]+"\\x"+jsshellcode[i]+jsshellcode[i+1]
   cont += 1
open("shellcode.out","wb").write(shellcode)
print printableShellcode+'"'
