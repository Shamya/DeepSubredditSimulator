from __future__ import division #makes / always do float division, and // do integer division
import os, subprocess, sys, re

START = chr(2)
END = chr(3)

def getTextFiles(dir):
  contents = os.listdir(dir)
  for content in contents:
    content = os.path.join(dir, content)
    if os.path.isdir(content):
      getTextFiles(content)
    elif os.path.isfile(content) and content[-4:] == ".txt":
      lines = None
      f.write(START)
      with open(content, "r") as textFile:
        lines = textFile.readlines()
      for line in lines:
        f.write(line.strip() + " ")
      f.write(END + " ")

f = open("data/oanc.txt", "w")
getTextFiles("data/oanc")
f.close()