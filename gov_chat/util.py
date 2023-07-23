import shutil

def purge_directory(target_dir:str):
    try:
        shutil.rmtree(target_dir)
    except OSError as e:
        print("Error: %s : %s" % (target_dir, e.strerror))