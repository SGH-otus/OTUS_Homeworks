import os
import subprocess
import hashlib

inpfile_ext = ".in"
outfile_ext = ".out"
solfile_ext = ".solve"
solver_name = "solver.py"

for curr_file in os.listdir("."):
    if curr_file.endswith(inpfile_ext):
        subprocess.call("python " + solver_name + " " + curr_file)    

        out_file = curr_file.replace(inpfile_ext, outfile_ext)
        hasher = hashlib.md5()
        hasher.update(open(out_file, "rb").read())
        md5_o = hasher.hexdigest()

        sol_file = curr_file.replace(inpfile_ext, solfile_ext)
        hasher = hashlib.md5()
        hasher.update(open(sol_file, "rb").read())
        md5_s = hasher.hexdigest()
        
        print curr_file, md5_o == md5_s
        
        os.unlink(sol_file)
        