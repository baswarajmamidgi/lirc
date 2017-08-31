# -*- coding: utf-8 -*-
# author baswaraj mamidgi
#date 1 july 2017

import subprocess
import numpy as np
import shlex

#creates the template for remote configuration file with the given remote name
def createconfig( remotename):                    
	file=open(remotename+".conf",'w')
	file.write('#IR Remote configuration File \n')
	file.write('#created by baswaraj mamidgi \n \n \n')
	file.write('begin remote \n')
	file.write('name'+'	'+remotename+'\n')
	file.write('flags	RAW_CODES \n')
	file.write('eps		30 \n')
	file.write('aeps	100\n \n')
	file.write('begin raw_codes \n \n')
	#remote data here
	file.close()

#welcome mesasge with instructions
print("\nirscript -  python script for recording IR-codes for usage with lirc\n\n"+
	
	"This program will record the signals from your remote control"+
	" and create a config file for lircd.\n\n"+
	"A proper config file for lircd is maybe the most vital part of this package,"+
	" so you should invest some time to create a working config file.\n"+
	"Although I put a good deal of effort in this program it is often "+
	" not possible  to automatically recognize all features of a remote\n"+
	"control. Often short-comings of the receiver hardware make it nearly"+
	" impossible. If you have problems to create a config file READ THE\n"+
	"DOCUMENTATION at https://sf.net/p/lirc-remotes/wiki\n")
	
raw_input("\nPress RETURN to continue.\n")

remote_name=raw_input("Enter remote name\n")

createconfig(remote_name)
subprocess.call(shlex.split('sudo pkill -f /dev/lirc0'))          #kill runninig lirc services
subprocess.call(shlex.split('sudo /etc/init.d/lirc stop'))        #stop lirc

button_name=raw_input("\nEnter button name :")

cmd='mode2 -m -d /dev/lirc0 >> ~/'+button_name+'.txt'             #recording data from remote

process=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)   #mode2 command      

print('press any key and enter after clicking button on remote')

interrupt=raw_input()                                             #interrupting the remote recording

a=np.genfromtxt(button_name+'.txt',dtype=None, delimiter="\n")    #first button
with open(remote_name+'.conf','a') as f:
    f.write('name    '+button_name+'\n' )
    subprocess.call(shlex.split('rm '+button_name+'.txt'))	    
    for el in np.delete(a,(0),axis=0):
        f.write(str(el)+'\n')


#----------------------------------------------------------------------------
#loop for multiple buttons

button_name=raw_input("Please enter the name for the next button (press <ENTER> to finish recording) \n")
while len(button_name)>1:

    subprocess.call(shlex.split('pkill -f /dev/lirc0'))
    
    cmd='mode2 -m -d /dev/lirc0 >> ~/'+button_name+'.txt'                  #recording data from remote

    process=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    print('press any key and enter after clicking button on remote')

    interrupt=raw_input()  #interrupting the remote recording

    """readfile=open(button_name+'.txt','r')
    print readfile.read()
    readfile.close() """

    a=np.genfromtxt(button_name+'.txt',dtype=None, delimiter="\n")   
    with open(remote_name+'.conf','a') as f:
        f.write('\n\nname    '+button_name+'\n' )
        subprocess.call(shlex.split('rm '+button_name+'.txt'))	    
        for el in np.delete(a,(0),axis=0):
            f.write(str(el)+'\n')

    button_name=raw_input("Please enter the name for the next button (press <ENTER> to finish recording)\n")

    
file=open(remote_name+'.conf','a')
file.write('\n\nend raw_codes \n')
file.write('end remote')
file.close()
print ('\nconfiguration file genereated')










