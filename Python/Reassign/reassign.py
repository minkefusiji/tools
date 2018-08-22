import os  
import time
import subprocess
import sys

machine_name = 'BN1AAP7051060C4'
#machine_name = 'BN1AAP6FD7FE1A3'
ap_tool_path = 'D:\\app\\APTools.ap_08_13_10_8_5005_3828\\'
get_machine_info_command = 'dmclient -c \"GetMachineInfo -m {0}\"'
reassign_command = 'manualrepair -a reassign -r "reassign" -m {0} -l'

lower_bound = 'PODBN2SCH05048'
upper_bound = 'PODBN2SCH05059'

def main():
	total = 0
	while 1:
		command = ap_tool_path + get_machine_info_command.format(machine_name)
		print (command)
		rc,out = subprocess.getstatusoutput(command)
		out = out.split("\n\n")
		out = out[2].split(",")
		pod = out[1][:14]
		if pod >= lower_bound and pod <= upper_bound:
			print("Pod {} for {} is in maintenance after {} times reassignment,  start new round...".format(pod, machine_name, total))
		else:
			print("Pod {} for {} is available after {} times reassignment,  exiting...".format(pod, machine_name, total))
			break
		command = ap_tool_path + reassign_command.format(machine_name)	
		print (command)
		rc,out = subprocess.getstatusoutput(command)
		print (out)

		total += 1
		time.sleep(1800)

#	data = sys.stdin.readlines()

if __name__ == '__main__':
	main()