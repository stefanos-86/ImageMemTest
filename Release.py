# Utility script to quickly create a release.
import os
import shutil

def my_position():
    return os.path.dirname(os.path.abspath(__file__))

def release_subfolder():
    return  os.path.join(my_position(), "ImageMemoryTest")

def delete_old_release():
    if os.path.isdir(release_subfolder()):
        shutil.rmtree(release_subfolder())
        print "Deleted old folder"

def make_new_folder():
    os.mkdir(release_subfolder())
    print "Created new folder"

def copy_files():
    release_content = [
        # Program files
        "Elements.py",
        "ExperimentLoader.py",
        "GuiFacade.py",
        "main.py",
        "Steps.py",
        # Dependencies
        "requirements.txt",
        # Windows niceties
        "install.bat",
        "MemoryTest.bat",
        # Documentation
        "Instructions.pdf",
        "License.txt"
    ]
    for file in release_content:
        source = os.path.abspath(file)
        destination = os.path.join(release_subfolder(), file)
        print "Copy " + source + " " + destination
        shutil.copy(source, destination)

if __name__ == "__main__":
    delete_old_release()
    make_new_folder()
    copy_files()