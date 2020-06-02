import argparse
import sys
import hashlib
from subprocess import *
import subprocess
import time


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--compare_file', dest='compare_file', action='append', help="provides names to compare with json  file(s)",required=True)
parser.add_argument('-hf', '--hash_file', dest='hash_file', action='append', help="provides hash file, only .txt allowed",required=True)
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

out_names_ext=['json','txt']

compare_files = args.compare_file
hash_files = args.hash_file

for file in compare_files:
	if file.split('.')[-1] in out_names_ext:
		pass
	else:
		print '>> only .json or .txt are allowed'
		print '>> exiting... :('
		sys.exit(0)
    

for file in hash_files:
	if file.split('.')[-1] == 'txt':
		pass
	else:
		print '>> only .txt are allowed as hash file'
		print '>> exiting... :('
		sys.exit(0)


def ssdeep(ssdeep_file,hash_txt):
	cm2=['ssdeep','-a','-s','-b','-m',hash_txt,ssdeep_file ]
	proc2=subprocess.Popen(cm2,stdin=PIPE,stdout=PIPE,stderr = PIPE)
	data=''
	while proc2.poll() is None:
		data += proc2.stdout.read()
	return data


def _init_ssdeep(sdf,hf):
	#brute force results, ssdeep keeps returning >> ssdeep: No matching files loaded
	while 1:
		cont = ssdeep(sdf,hf)
		if cont!='ssdeep: No matching files loaded' or cont=="":
			if cont.strip('\n').strip('\r')!="":
				return cont
		else:
			print cont


print '\n\t\tSSdeep Successfully Executed\n\n'

if len(hash_files)==len(compare_files):
	for x,z in zip(hash_files,compare_files):
		print _init_ssdeep(z,x)

if len(hash_files)!=len(compare_files):
	for i in compare_files:
		print _init_ssdeep(i,hash_files[0])
		
print '\n\t\tProcessing Results'
print '\n\t\tPattern Matching Executed Successfully'