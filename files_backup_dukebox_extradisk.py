import glob
import os.path
import shutil

SRC_DIR = r"/hdd/backup/" #your source directory
TARG_DIR = "/media/tomqi/ZW/" #your target directory

GLOB_PARMS = "*" #maybe "*.pdf" ?
original_folder = glob.glob(os.path.join(SRC_DIR, GLOB_PARMS))
new_folder = glob.glob(os.path.join(TARG_DIR, GLOB_PARMS))
new_folder_set = set([os.path.basename(item) for item in new_folder])

for file_path in original_folder:
    file_name = os.path.basename(file_path)
    if file_name not in new_folder_set:
        print("copy:"+file_name)
        shutil.copytree(file_path,TARG_DIR+file_name)
    else:
        print("{} existed".format(
            file_name))
        # This is just a print command that outputs to console that the
        # file was already in directory
