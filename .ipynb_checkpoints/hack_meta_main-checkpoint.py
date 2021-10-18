#import numpy as np
import os 
import time

#amps = #np.arange(0.01, 1.501, 0.01) 
#amps = list(range(0.01,1.501,0.01))
amps = [0.01*k for k in range(1,151)]
ampsp = [amps[k:(15+k)] for k in range(10)] #np.split(amps,10) #

for ampi in ampsp:
    mina =min(ampi)
    maxa = max(ampi)
    try:
        os.system("rm mcondor.sub")
    except Exception:
        pass

    file = open("mcondor.sub","w")
    for L in range(1,15):
        info = f"executable=subash.sh \n \n"\
        f"L={L}\n"\
        f"output = jobs/outs/$(Item)_$(L).out\n"\
        f"error = jobs/errs/$(Item)_$(L).err\n"\
        f"log = jobs/logs/$(Item)_$(L).log\n"\
        f"request_cpus = 1\n"\
        f"+flavour='medium'\n\n"\
        f"args=$(Item) $(L)\n"\
        f"queue from seq {mina} 0.01 {maxa}| \n \n \n"
        file.write(info)

    os.system("chmod +x mcondor.sub")
    os.system("condor_submit mcondor.sub")
    break #time.sleep(0.1)