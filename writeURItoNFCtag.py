#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# Author: Jose Miguel Esparza (jesparza AT eternal-todo DOT com)
# Date: 2012-07-01
# Description: Simple script to write any URI to an NFC tag. Using the 0x00 URI type we can write any type of
#              URI in the tag, without thinking about it. Based on the helloworld.py (nfcpy) script.
#              You can take a look at:
#                   - The different URIs defined by the specification: http://www.maintag.fr/fichiers/pdf-fr/nfcforum-ts-rtd-uri-1-0.pdf
#                   - Other special URIs related to installed mobile applications: http://sixrevisions.com/web-development/qr-codes-uri-schemes/
# Requirements: nfcpy
# 
#
# -----------------------------------------------------------------------------
# Copyright 2011 Stephen Tiedemann <stephen.tiedemann@googlemail.com>
#
# Licensed under the EUPL, Version 1.1 or - as soon they 
# will be approved by the European Commission - subsequent
# versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the
# Licence.
# You may obtain a copy of the Licence at:
#
# http://www.osor.eu/eupl
#
# Unless required by applicable law or agreed to in
# writing, software distributed under the Licence is
# distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# See the Licence for the specific language governing
# permissions and limitations under the Licence.
# -----------------------------------------------------------------------------

import os
import sys
import time

sys.path.insert(1, os.path.split(sys.path[0])[0])

import nfc
import nfc.ndef
import nfc.ndef.Uri

if len(sys.argv) != 2:
    sys.exit('Usage: '+sys.argv[0]+' uri')
myURI = sys.argv[1]

clf = nfc.ContactlessFrontend()

print "Please, touch a tag to send your URI to the world..."
while True:
    tag = clf.poll()
    if tag and tag.ndef:
        break
    time.sleep(1)

uri = nfc.ndef.Uri.UriRecord(myURI)
uri._data = '\x00'+myURI
message = nfc.ndef.Message(uri)
tag.ndef.message = message.tostring()

print "Thanks, you can remove the tag..."

