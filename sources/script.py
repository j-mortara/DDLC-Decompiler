import os
import platform
import shutil
import subprocess

extraction_directory = os.path.join("..", "extracted_files")
rpatool_py_path = os.path.join("..", "scripts", "rpatool", "rpatool.py")
unrpyc_py_path = os.path.join("..", "scripts", "unrpyc", "unrpyc.py")

python_cmd = "py -2 " if platform.system() == 'Windows' else "python2 "


def rpa_unpacking_commands(rpa_dir):
    rpa_files = [f for f in listdir_fullpath(rpa_dir) if f.endswith(".rpa")]
    for f in rpa_files:
        basename = file_basename(f)
        print("Extracting " + basename)
        yield python_cmd + rpatool_py_path + " -x " + f + " -o " + os.path.join(extraction_directory,
                                                                                basename.split(".")[0])


def rpyc_decompiling_command():
    return python_cmd + unrpyc_py_path + " " + os.path.join(extraction_directory, "scripts")


def extract_rpas(directory):
    for command in rpa_unpacking_commands(directory):
        execute(command)


def extract_scripts():
    print("Extracting script files")
    execute(rpyc_decompiling_command())
    for rpy in [f for f in listdir_fullpath(os.path.join(extraction_directory, "scripts")) if f.endswith(".rpy")]:
        move_file(rpy, os.path.join(extraction_directory, "extracted_scripts"))


def execute(cmd):
    subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, shell=True).communicate()


def file_basename(f):
    return f.split("\\")[-1]


def listdir_fullpath(d):
    return (os.path.join(d, f) for f in os.listdir(d))


def move_file(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    shutil.move(src, os.path.join(dst, file_basename(src)))


if __name__ == '__main__':
    ddlc_dir = input("Path to the \"game\" directory of DDLC : ")
    extract_rpas(ddlc_dir)
    extract_scripts()
    print("Done !")
