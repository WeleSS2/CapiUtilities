import os
import sys
import json
#import subprocess

argList = []

nameVenv = ""
nameExists = False

debug = True
debugLevel = 5

venvInstall = []
venvExists = False
venvPath = ""

def log(message, *args):
    if debug:
        print(message, *args)

def generalLog(message, *args):
    if debugLevel >= 4:
        print(message, *args)

def debugLog(message, *args):
    if debugLevel >= 5:
        print(message, *args)

# ----------------------------------------------------------------------------

def generateWebDjangoVenv():
    installer = os.path.join(os.path.dirname(__file__), "installer", "web-django.txt")
    return generateVenv("web-django", installer)

def generateWebFastApiVenv():
    installer = os.path.join(os.path.dirname(__file__), "installer", "web-fastapi.txt")
    return generateVenv("web-fastapi", installer)

def generateDesktopVenv():
    global venvExists, venvPath, nameVenv
    packFile = readFile(os.path.join(os.path.dirname(__file__), "installer", "desktop.txt"))

    if packFile is None:
        generalLog("No packages to install")
        return -1
    
    debugLog("Packages to install: %s", packFile)

    venvRet = generateVenv(nameVenv)
    
    if venvRet != 0:
        generalLog("Failed to create virtual environment")
        return -1

    packRet = installPackages(packFile)

    if packRet != 0:
        generalLog("Failed to install packages")
        return -1

    return 0

def generateMobileVenv():
    installer = os.path.join(os.path.dirname(__file__), "installer", "mobile.txt")
    return generateVenv("mobile", installer)

def generateAuthVenv():
    installer = os.path.join(os.path.dirname(__file__), "installer", "auth.txt")
    return generateVenv("auth", installer)

def generateAdditionalPackages():
    
    return None

# ----------------------------------------------------------------------------

def generateVenv(name):
    global venvExists, venvPath
    
    # Create the virtual environment
    venv_path = os.path.join("/app-manager/pvenv/", name.replace(" ", "_"))
    python_executable = sys.executable
    command = f'{python_executable} -m venv {venv_path}'

    generalLog("Command: %s", command)

    # Run the command to create the virtual environment
    ret = os.system(command)

    if ret != 0:
        generalLog("Failed to create virtual environment")

        return ret
    else:
        generalLog("Virtual environment created successfully")
        venvExists = True
        venvPath = venv_path

    return ret

# ----------------------------------------------------------------------------

def readFile(file_path):
    generalLog("Reading file: %s", file_path)

    if not os.path.isfile(file_path):
        generalLog("File not found: %s", file_path)
        return None

    with open(file_path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    packages = [line for line in lines if line and not line.startswith("#")]

    if not packages:
        generalLog("No packages to install in %s", file_path)
        return None

    return packages

# ----------------------------------------------------------------------------

def installPackages(packages):
    global venvExists, venvPath
    generalLog("Installing packages: %s", packages)

    if not venvExists:
        generalLog("Virtual environment does not exist")
        return -1
    
    if not os.path.isdir(venvPath):
        generalLog("Virtual environment path does not exist")
        return -1
    
    venv_dir = os.path.join(venvPath, "bin", "python")

    package_str = " ".join(packages)

    cmd = f"{venv_dir} -m pip install {package_str}"

    generalLog("Running command: %s", cmd)
    retcode = os.system(cmd)

    generalLog("Running command: %s", " ".join(cmd))

    retcode = os.system(cmd)

    return retcode
    
# ----------------------------------------------------------------------------

def transformArgs(args):
    generalLog("Transforming args")

    for arg in args:
        debugLog("Argument: " + arg)
        if "start.py" not in arg:
            argList.append(arg)

    args_to_concat = []
    for arg in argList[:]:
        debugLog("Current argument: " + arg)
        if arg.startswith("--"):
            debugLog("Encountered -- argument")
            if args_to_concat:
                debugLog("Concatenating accumulated args: " + str(args_to_concat))
                concat_arg = " ".join(args_to_concat)
                debugLog("Concatenated arg: " + concat_arg)
                argList.insert(argList.index(arg), concat_arg)
                debugLog("Inserted concatenated arg at position " + str(argList.index(concat_arg)))
                args_to_concat = []
        else:
            debugLog("Accumulating non- -- argument: " + arg)

            args_to_concat.append(arg)
            argList.remove(arg)

    # Final check for remaining args
    if args_to_concat:
        debugLog("Concatenating remaining args: " + str(args_to_concat))
        concat_arg = " ".join(args_to_concat)

        debugLog("Concatenated arg: " + concat_arg)
        argList.append(concat_arg)


    generalLog("Arguments: " + str(argList))

# ----------------------------------------------------------------------------

def initWorkspace(args):
    global venvExists, nameVenv, nameExists
    
    if len(args) == 0:
        generalLog("No arguments provided")
        return
    
    transformArgs(args)

    for arg in argList:
        debugLog("Argument: " + arg)
        debugLog("Arglist: " + str(argList))

        if arg == "--name":
            nameVenv = argList[argList.index(arg) + 1]
            nameExists = True
            generalLog("Name: %s", nameVenv)

    if nameExists :
        generalLog("Name exists")
    else:
        generalLog("Name does not exist")
        exit(-1)

    for arg in argList:
        pos = argList.index(arg)

        if arg == "--webd":
            generateWebDjangoVenv()

        elif arg == "--webf":
            generateWebFastApiVenv()

        elif arg == "--desktop":
            if generateDesktopVenv() == -1:
                generalLog("Failed to generate desktop venv")
                exit(-1)
        
        elif arg == "--mobile":
            generateMobileVenv()
        
        elif arg == "--auth":
            generateAuthVenv()
        
        elif arg == "--all":
            generateDesktopVenv()
            generateMobileVenv()
            generateAuthVenv()

        elif arg == "--add":
            generateAdditionalPackages()
            

    location = "/app-manager/pvenv"


    
    #venv_path = os.path.join(location, envName.replace(" ", "_"))
    #python_executable = sys.executable
    #command = f'{python_executable} -m {envName} {venv_path}'

    # Run the command to create the virtual environment
    #os.system(command)
    
    return

def main(args):
    generalLog("Starting...")

    generalLog("Arguments: %s", args)

    # Load config from db

    config = None

    with open('config.json') as f:
        config = json.load(f)

    if config is None:
        generalLog("No config found")
        return
    
    if config["initialized"] is False:
        generalLog("Creating workspace")
        initWorkspace(args)

        return
        
main(sys.argv)

        

# Get the location from the command-line argument
#location = "/app-manager/pvenv"

# Create the virtual environment
#venv_path = os.path.join(location, 'venv')
#python_executable = sys.executable
#command = f'{python_executable} -m venv {venv_path}'

# Run the command to create the virtual environment
#os.system(command)
