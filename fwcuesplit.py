#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cue splitter by Vojtěch Salajka
import sys, subprocess, re
if len(sys.argv) != 3 and len(sys.argv) != 4:
	print("usage example: fwcuesplit.py filename.wav filename.cue [prefix]")
	sys.exit()
prefix = ""
if len(sys.argv) == 4:
	prefix = sys.argv[3]
wavFilename = sys.argv[1]
if not wavFilename.endswith(".wav"):
	print("wav file needed")
	sys.exit()
cueFilename = sys.argv[2]
note = "Please note that this script depends on cuebreakpoints (found in cuetools package) and shnsplit (found in shntool package)."
try:
	p1 = subprocess.Popen(["cuebreakpoints", cueFilename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except OSError:
	print("Dependency error: cuebreakpoints not found. Please make sure it is installed properly.")
	print(note)
	sys.exit()
(cuebreakpointsStdout, cuebreakpointsStderr) = p1.communicate()
if p1.returncode != 0: # error getting breakpoints
	print(cuebreakpointsStderr)
	sys.exit()
try:
	p2 = subprocess.Popen(["shnsplit", "-a", "trk", "-O", "always", "-o", "flac", wavFilename], stdin=subprocess.PIPE)
except OSError:
	print("Dependency error: shnsplit not found. Please make sure it is installed properly.")
	print(note)
	sys.exit()
p2.communicate(cuebreakpointsStdout)
cueFile = open(cueFilename, "r")
cueLines = cueFile.readlines(False)
cueFile.close()
trackBlock = False
trackNumStr = "00"
for line in cueLines:
	#print line
	m = re.match(".*TRACK (?P<trackN>[0-9]+) AUDIO", line)
	if m:
		trackNumStr = m.group("trackN")
		trackBlock = True
	elif trackBlock:
		m2 = re.match(".*TITLE \"(?P<trackTitle>.*)\"", line)
		if m2:
			trackTitle = m2.group("trackTitle")
			trackFilenameOld = "trk"+trackNumStr+".flac"
			trackFilename = prefix+trackNumStr+" - "+trackTitle+".flac"
			p3 = subprocess.Popen(["mv", trackFilenameOld, trackFilename])		
md5sumFilename = "md5sum"+prefix+".txt"
print("Generating "+md5sumFilename+".")
md5sumTxt = open(md5sumFilename, "w")
p4 = subprocess.Popen(["md5sum", "-b", wavFilename], stdout=md5sumTxt)
md5sumTxt.close()
print("Finished.")
