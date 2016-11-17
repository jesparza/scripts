#!/usr/bin/env python

# 
# Script to de/compress the streams of a PDF file
#
# http://eternal-todo.com
# Jose Miguel Esparza
#

import sys,zlib,os,re

usage = "Usage: "  + sys.argv[0] + ''' -c|-d target

Arguments:

    target: the string or file to be de/compressed.

Options:

    -c: compress
    -d: decompress
'''

def cleanStream(stream):
   output = stream
   for i in range(len(stream)):
      if stream[i] == '\r' or stream[i] == '\n':
         output = output[1:]
      else:
         break
   for i in range(len(stream)-1,0,-1):
      if stream[i] == '\r' or stream[i] == '\n':
         output = output[:-1]
      else:
         break
   return output


if len(sys.argv) != 3 or (sys.argv[1] != '-c' and sys.argv[1] != '-d'):
   sys.exit(usage)

action = sys.argv[1]
target = sys.argv[2]
targets = []
if os.path.exists(target):
   content = open(target,'r').read()
   if action == '-d':
      targets = re.findall('/Filter\s*?/FlateDecode.*?stream(.*?)endstream',content,re.DOTALL)
      if targets == []:
         targets.append(content)
   else:
      targets.append(content)
else:
   targets.append(target)
for string in targets:
   string = cleanStream(string)
   try:
      if action == '-c':
         print zlib.compress(string)
      else:
         print zlib.decompress(string)
   except:
      print "Zlib error: "+str(sys.exc_info()[1])
