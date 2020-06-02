#python create_profile.py -cp SCADA_to_substation_normal.pcapng -o norm.json -cp SCADA_to_substation_attack1.pcapng -o attk.json


import argparse
import sys
import subprocess
from subprocess import *
import json


all_data=[]

parser = argparse.ArgumentParser()
parser.add_argument('-cp', '--create_profile', dest='create_profile', action='append', help="provides names to create file(s) from >>  .pcap or .pcapng Files",required=True)
parser.add_argument('-o', '--output_file', dest='output_file', action='append', help="provides names for output json file(s) >> .json File",required=True)
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])


read_file_ext=['pcap','pcapng']
out_names_ext=['json','txt']
read_files = args.create_profile
out_names = args.output_file

if len(read_files)!=len(out_names):
	print '[+] Number of Input Files Should be the same as Output Files'
	print '[+] Exiting... :('
	sys.exit(0)

for file in read_files:
	if file.split('.')[-1] in read_file_ext:
		pass
	else:
		print '>> Only .pcap or pcapng are allowed'
		print '>> Exiting... :('
		sys.exit(0)
    

for file in out_names:
	if file.split('.')[-1] in out_names_ext:
		pass
	else:
		print '>> Only .txt or .json are allowed'
		print '>> Exiting... :('
		sys.exit(0)

#print read_files
#print out_names

print '>> Processing...'

def json_list(list):
    lst = []
    for pn in list:
        d = {}
        d['pkt_payload']=pn
        lst.append(d)
        print pn
    return json.dumps(lst)


def _104pcap_json(pcap_files,json_out_names):
	for pcap_file,json_file in zip(pcap_files,json_out_names):
		print '\nProcessing : %s '%(pcap_file)
		print '\nOutput File : %s'%(json_file)
		cmd=["tshark","-r",pcap_file,"-T","fields","-e","tcp.payload","104apci"]
		proc=subprocess.Popen(cmd,stdin=PIPE,stdout=PIPE,stderr = PIPE)
		data=[]
		while proc.poll() is None:
			pkt=proc.stdout.readline().strip('\r').strip('\n')
			if len(pkt)>0:
				data.append(pkt)
		#print data
		if json_file.endswith('.txt'):
			fp=open(json_file,'w')
			#for data_pkt in json_list(data).split(','):
			#fp.write(data_pkt+'\n')
			for i in data:
				fp.write(i+"\n")
				print i
			fp.close() 
		else:
			fp=open(json_file,'w')
			#for data_pkt in json_list(data).split(','):
			#fp.write(data_pkt+'\n')
			fp.write(json_list(data))
			fp.close() 
		
	
	return str(json_list(data))


_104pcap_json(read_files,out_names)
print '\nTCP Payload Extracted'
print 'Processing File(s)Complete'
print 'File(s) Successfully Saved.\n'
