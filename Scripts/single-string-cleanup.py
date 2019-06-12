import os
import getpass
import sys

def findReplace(files, find, replace, filePattern):
    """
    This does a find/replace of a single string.

    :param files: This reads from the list above.
    :param find: This is the initial input.
    :param replace: What you're trying to replace
    :param filePattern: Again, just a simple text file
    :return:
    """
    print("Ok - lets clean them up...\n")
    for files in fileList:
        with open(files) as f:
            s = f.read()
        s = s.replace(find, replace)
        with open(files, "w") as f:
            f.write(s)

def yes_no_cont(answer):
    yes = {'yes','y','YES','Y'}
    no = {'no','n','NO','N'}
    while True:
        choice = input(answer).lower()
        if choice in yes:
            break
        elif choice in no:
            sys.exit("OK - Exiting Script")
        else:
            print("Try again.")

findWHERE = input("Enter the directory tree (ie. /your/folder/here): ")
findME = getpass.getpass('Enter what you want to clean up: ')

# Default replacement string.  Adjust as necessary
replaceME = '&&&&'

print("")

fileList = []
for root, dirs, files in os.walk(findWHERE):
    for name in files:
        if name.endswith('.txt'):
            filepath = os.path.join(root, name)
            if findME in open(filepath, 'r').read():
                fileList.append(filepath)

if len(fileList) == 0:
    sys.exit('String not present, exiting')
else:
    print("OK, that string is in ", len(fileList), " files.  Here are the files names: ")
    print(fileList)
    print("")

yes_no_cont("Does this files list above look correct? (yes or no) ")
findReplace(fileList, findME, replaceME, "*.txt")
