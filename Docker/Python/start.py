
import os
import sys
import json

argList = []
venvList = []
nameVenv = ""
nameExists = False

debug = True
debugLevel = 4

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

def generateWebVenv():
    
    
    return

def generateDesktopVenv():
    return

def generateMobileVenv():
    return

def generateAuthVenv():
    return

def generateAdditionalPackages():
    return

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

def initWorkspace(args):
    if len(args) == 0:
        generalLog("No arguments provided")
        return
    
    transformArgs(args)

    for arg in argList:
        if arg == "--name":
            nameVenv = argList[argList.index(arg) + 1]
            nameExists = True
            generalLog("Name: %s", nameVenv)
        else:
            generalLog("Missing name, exiting")
            exit(-1)

    for arg in argList:
        pos = argList.index(arg)
        
        if arg == "--web":
            generateWebVenv()

        elif arg == "--desktop":
            generateDesktopVenv()
        
        elif arg == "--mobile":
            generateMobileVenv()
        
        elif arg == "--auth":
            generateAuthVenv()
        
        elif arg == "--all":
            generateWebVenv()
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