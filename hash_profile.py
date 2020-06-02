#>python hasher.py -ch SCADA_to_substation_attack2.pcap -ch SCADA_to_substation_attack3.pcapng -ch SCADA_to_substation_normal.pcapng -o asdff.txt



import subprocess
from subprocess import *
import argparse
import sys

#ssdeep * > res.txt
#ssdeep -s -m res.txt *
#ssdeep -a -s -b -m jjjjj.txt mega104-17-12-18.pcapng

parser = argparse.ArgumentParser()
parser.add_argument('-ch', '--create_hash', dest='create_hasher', action='append', help="Provides names to hash",required=True)
parser.add_argument('-o', '--output_file', dest='outfile', action='append', help="Provides names to store the hash",required=True)
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

filestoshash=args.create_hasher
storehash=args.outfile


def ssdeep(ssdeep_file):
	cm1=['ssdeep',"-a",'-s','-b',ssdeep_file]
	proc=subprocess.Popen(cm1,stdin=PIPE,stdout=PIPE,stderr = PIPE)
	data=''
	while proc.poll() is None:
		data += proc.stdout.read()
	return data

if len(filestoshash)==len(storehash):
	for i,j in zip(filestoshash,storehash):
		outdata=ssdeep(filestoshash)
		fp=open(storehash,'w')
		fp.write(outdata)
		fp.close()


elif len(filestoshash)!=len(storehash):
	fp=open(storehash[0],'w')
	for i in filestoshash:
		outdata=ssdeep(i)
		fp.write(outdata)
	fp.close()

