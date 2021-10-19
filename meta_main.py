import time
import os
import subprocess


name = "too.sub"
for l in range(1,2,1):
    lmin = l
    lmax = l+1

    for L in range(lmin,lmax):

        
        info =  f"executable=subash.sh \n"\
                f"L={L}\n"\
                f"output = jobs/outs/$(Item)_$(L).out\n"\
                f"error = jobs/errs/$(Item)_$(L).err\n"\
                f"log = jobs/logs/$(Item)_$(L).log\n"\
                f"request_cpus = 1\n"\
                f"+flavour='medium'\n\n"\
                f"args=$(Item) $(L)\n"\
                f"queue from seq 10.01 0.01 10.5| \n"

        
        file = open(name,"w")
        file.write(info)

        print(info)

        subprocess.Popen("condor_submit too.sub", shell=True, executable='/bin/bash')
        #comm="condor_submit too.sub"#
        #os.system('GREPDB={}; /bin/bash -c "$GREPDB"'.format(comm))
        
        time.sleep(1)
