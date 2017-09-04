import subprocess, sys
import time

oid = " ".join(sys.argv[3:])
time_arg = sys.argv[2]
delay1 = time.time()
samp = float(time_arg)
samp = int(samp)
args = sys.argv[1]
args = args.split(':')
ip = args[0]
port = args[1]
comm = args[2]

while 1:
	
	cmd = "snmpget -v1 -c"+comm+" "+ip+":"+port+" 1.3.6.1.2.1.1.3.0 "+oid

	try:

############### First/Old Counter Value Calculation Statements #######################	

		out1 = []
		out1 = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
		change_line1 = out1
		change_line1 = change_line1.splitlines()
		change_type1 = 0
		time_ticks11 = 0
		old_arr = []
		uptime1 = change_line1[0]
		uptime1 = uptime1.split(' ')
		oid_id = []
		time_ticks1 = uptime1[3]
		time_ticks1 = time_ticks1.replace('(', '')
		time_ticks1 = time_ticks1.replace(')', '')
		time_ticks11 = float (time_ticks1)
		i = 1
		while i < len(change_line1):	
			change_value1 = change_line1[i].split(' ')
			oid_id.append(change_value1[0])
			change_type1 = float (change_value1[3])	
			old_arr.append(change_type1)
			i += 1
		delay2 = time.time()
		samp_new = samp - (delay2 - delay1)
		if(samp_new < 0):
			pass
		else:
			time.sleep(samp_new)
		delay1 = time.time()
	
###############	Second/New Counter Value Calculation Statements #######################
		out2 = []
		out2 = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
		change_line2 = out2
		change_line2 = change_line2.splitlines()
		change_type2 = 0
		time_ticks22 = 0
		uptime2 = change_line2[0]
		uptime2 = uptime2.split(' ')
		time_ticks2 = uptime2[3]
		time_ticks2 = time_ticks2.replace('(', '')
		time_ticks2 = time_ticks2.replace(')', '')
		time_ticks22 = float (time_ticks2)
		new_arr = []
		j = 1
		while j < len(change_line2):	
			change_value2 = change_line2[j].split(' ')		
			change_type2 = float (change_value2[3])		
			new_arr.append(change_type2)
			j += 1
	
		
############## Rate of Change of Counter Values Calculation Statements #################
		time_ticks = (time_ticks22 - time_ticks11)/100
		if(time_ticks < 0):
			print ("The Device has been Rebooted")
		else:
			k = 0
			while k < len(new_arr):
				rate_calc = new_arr[k]-old_arr[k]
				if(rate_calc < 0):
					rate_calc = rate_calc + 0xffffffff
					rate_calc = rate_calc/time_ticks
					print oid_id[k], " Rate : ", int(round(rate_calc))
				else:
					rate_calc = rate_calc/time_ticks
					print oid_id[k], " Rate : ", int(round(rate_calc))
				k += 1
		print "########################################################"
	except subprocess.CalledProcessError as e:
		print e.output
	
