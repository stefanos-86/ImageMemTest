# Utility script to quickly create a release.
import os
import shutil
import zipfile


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


def compress_folder():
    zipf = zipfile.ZipFile('ImageMemoryTest.zip', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(release_subfolder()):
        for file_to_add in files:
            zipf.write(os.path.join(root, file_to_add), os.path.basename(file_to_add))
    zipf.close()
    print "Compressed archive"


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
        "License.txt",
        # Examples
        "Demo"
    ]
    for file in release_content:
        source = os.path.abspath(file)
        destination = os.path.join(release_subfolder(), file)
        print "Copy " + source + " " + destination
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy(source, destination)

if __name__ == "__main__":
    delete_old_release()
    make_new_folder()
    copy_files()
    compress_folder()
    # TODO: tag the repo?