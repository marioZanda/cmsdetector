#!/usr/bin/python

import sys, getopt
import requests
import validators
import subprocess
import os
import json


help =  '''
			
usage : python cmsdetector.py [option] [argument]

	options 		argument
	
	-i		<file path> for multiple urls
	
	-u 		<url> 
	
	-h / --help		display help menu
	
	
	examples : python cmsdetector.py -i urls.txt 
	
				python cmsdetector.py -u wordpress.com
	'''
def FileCheck(fn):
    try:
      open(fn, "r")
      return 1
    except IOError:
      print "Error: File does not appear to exist."
      return 0

def main(argv):
	result = ""
	inputfile = ''
	outputfile = ''
	opts, args = getopt.getopt(argv,"hi:u:",["help","ifile=","url="])
	if len(opts) == 0:
		print help
	for opt, arg in opts:
		if opt in ("-h","--help"):
			print help
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
			if FileCheck(inputfile):
				with open(inputfile,"r") as f:
					for line in f.read().splitlines():
						valid= (validators.domain(line) or validators.url(line))
						if valid==True:
							print("Checking "+line+" ... \n")
							subprocess.call(["python3", "CMSeeK/cmseek.py","--follow-redirect","-u",line],stdout=open(os.devnull,"w"),stderr=subprocess.STDOUT)
							line = line.replace('https://','').replace('http://', '').replace('/','')
							location = "CMSeeK/Result/"+line+"/cms.json"
							with open(location,"r") as f:
								data = json.load(f)
								if data['cms_name'] == "":
									result = result+line+" ----------> No CMS found\n"
								else:
									result = result+line+" ----------> "+data['cms_name']+"\n"
							
						else:
							print("Invalid url")
		elif opt in ("-u", "--url"):
			url = arg
			valid= (validators.domain(url) or validators.url(url))
			if valid==True:
				print("Checking "+url+" ... \n")
				subprocess.call(["python3", "CMSeeK/cmseek.py","--follow-redirect","-u",url],stdout=open(os.devnull,"w"),stderr=subprocess.STDOUT)
				url = url.replace('https://','').replace('http://', '').replace('/','')
				location = "CMSeeK/Result/"+url+"/cms.json"
				with open(location,"r") as f:
					data = json.load(f)
					if data['cms_name'] == "":
						result = result+url+" ----------> No CMS found\n"
					else:
						result = result+url+" ----------> "+data['cms_name']+"\n"
			else:
				print("Invalid url")
	print result
if __name__ == "__main__":
   main(sys.argv[1:])
