import subprocess, sys
import time

delay1 = time.time()

oid = " ".join(sys.argv[4:])
freq_arg = sys.argv[2]
time_samp = float(freq_arg)
time_samp = 1/time_samp
#time_samp = int(1/freq_samp)


samples_arg = sys.argv[3]
samples = float(samples_arg)
samples = int(samples)

args = sys.argv[1]
args = args.split(':')
ip = args[0]
port = args[1]
comm = args[2]

if(samples >= 2):
	loop = samples+1 
elif(samples == -1):
	loop = 1
elif(samples == 0 or samples == 1):
	loop = 0
else:
	print("Incorrect samples value entered")
	exit()

time_ticks11 = 0.0
old_arr = []

num = 1
while 1:

	cmd = "snmpget -v1 -c"+comm+" "+ip+":"+port+" 1.3.6.1.2.1.1.3.0 "+oid

	try:

		############### Old Counter Value Calculation Statements #######################	
		if(samples == -1):
			pass
		elif(num <= loop):
			pass
		else:
			break

		out = []
		out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
		change_line = out
		change_line = change_line.splitlines()
		change_type = 0
		time_ticks22 = 0.0
		new_arr = []
		uptime = change_line[0]
		uptime = uptime.split(' ')
		oid_id = []
		time_ticks = uptime[3]
		time_ticks = time_ticks.replace('(', '')
		time_ticks = time_ticks.replace(')', '')
		time_ticks22 = float (time_ticks)
		i = 1
		while i < len(change_line):	
			change_value = change_line[i].split(' ')
			oid_id.append(change_value[0])
			change_type = float (change_value[3])	
			new_arr.append(change_type)
			i += 1
		delay2 = time.time()
		samp_new = time_samp - (delay2 - delay1)
		if(samp_new < 0):
			pass
		else:
			time.sleep(samp_new)
		delay1 = time.time()
		
		############## Rate of Change of Counter Values Calculation Statements #################
		output = []
		if(num == 1):
			pass
		else:
			time_ticks = (time_ticks22 - time_ticks11)/100
			if(time_ticks < 0):
				print ("The Device has been Rebooted")
			else:
				output.append(int(round(time.time())))
				k = 0
				while k < len(new_arr):	
					rate_calc = new_arr[k]-old_arr[k]
					if(rate_calc < 0):
						rate_calc = rate_calc + 0xffffffff
						rate_calc = rate_calc/time_ticks
						output.append(int(round(rate_calc)))
					else:	
						rate_calc = rate_calc/time_ticks
						output.append(int(round(rate_calc)))
					k = k + 1
		print ' | '.join(map(str, output))
		old_arr = new_arr
#		print "########################################################"
		time_ticks11 = time_ticks22		
	except subprocess.CalledProcellssError as e:
		print e.output
	num = num + 1
