#!/usr/bin/env python

import sys, getopt, time, os
from collections import namedtuple		

###############################################################
# Returns a dictionary containing all program parameters
# (and default values for those that weren't given)
#
def init_params(argv):

	# Set default values for parameters	
	t_params = {'tools_path':  "/home/xfabia/tools",  # path to the tools directory 
	            'binary_path': "/usr/bin/sumo-gui", 	# path to the sumo or sumo-gui binary
	            'cfg':		     "./xml/proj.sumocfg"}   # path to the project config file
	try:
		opts, args = getopt.getopt(argv,"c:",["tools=", "bin="])
	except getopt.GetoptError:
		print "SIN-project:\n [--tools=] \t Path to the sum/tools library\n" \
												 "[--bin=]   \t Path to 'sumo-gui' or 'sumo' binary file\n" \
												 "[-c path]  \t Path to the configuration file\n"
		raise
	
	# Set given values for parameters
	for opt, arg in opts:
		if opt == "--tools":
			t_params['tools_path'] = arg
		elif opt == "--bin":
			t_params['binary_path'] = arg
		elif opt == '-c':
			t_params['cfg'] = arg
			
	return t_params


###############################################################
# Try to import the traci library. This succeeds only if 
# tools_path is set  correctly
#
def import_traci(tools_path):
	global traci
	sys.path.append(tools_path)	
	try:	
		import traci
	except:
		print "Failed to import traci library."
		if os.getuid() == 0:
			print "Use '--tools=' parameter to set path to sumo/tools directory to fix this"
		else:
			print "This program must be run with sudo."
		exit(1)

###############################################################
# ---------------------- MAIN FUNCTION ---------------------- #
###############################################################
def main():
	t_params = init_params(sys.argv[1:])
	
	import_traci(t_params['tools_path'])
	try:
		# Each parameter of '.start' represents one parameter that will be 
		# passed to the 'sumo' or 'sumo-gui' binary as described in 'sumo --help' 
		traci.start([t_params['binary_path'], "-c", t_params['cfg']]) 
	except Exception as ex:
		if (type(ex) == OSError):
			print "Probably couldn't find sumo binary. Use parameter --bin='path_to_sumo' to fix this"
			exit(1)
		raise
		
	step = 0
	while step < 1000:
		traci.simulationStep()
		traci.trafficlights.setPhase("0", 0)
		step += 1

	traci.close()

# ------------------- Call main -------------------- #
main()

