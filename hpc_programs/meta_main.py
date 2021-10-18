import time
import os
import subprocess

for l in range(1,6,3):
    lmin = l
    lmax = l+3

    file = open("mcondor.sub","w")
    for L in range(lmin,lmax):

        info = f"executable=subash.sh \n"
        f""
        'executable=subash.sh \n\
        output = jobs/outs/$(Item)_$(L).out\n\
        error = jobs/errs/$(Item)_$(L).err\n\
        log = jobs/logs/$(Item)_$(L).log\n\
        request_cpus = 1\n\
        +flavour="medium"\n\n'

        f"L={L}\n"\
        f"args=$(Item) $(L)\n"\
        f"queue from seq 10.01 0.01 10.5| \n"

        file.write(info)

    os.system("chmod +x mcondor.sub")
    os.system('GREPDB="condor_submit mcondor.sub"; /bin/bash -c "$GREPDB"')
#    os.system("condor_submit mcondor.sub")
    #subprocess.call('/bin/bash -c "$GREPDB"', shell=True, env={'GREPDB': 'condor_submit mcondor.sub'})
    time.sleep(1)
