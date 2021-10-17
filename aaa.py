
file = open("mcondor.sub","w")
file.write(info)

for L in range(1,5):

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
    f"queue from seq 0.01 0.1 1| \n"

    file.write(info)

import os
os.system("chmod +x mcondor.sub")
