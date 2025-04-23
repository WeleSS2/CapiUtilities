import os
import sys
import json

venvList = []
envName = ""

def initWorkspace(args):
    if len(args) == 0:
        print("No arguments provided")
        return
    
    for arg in args:
        if arg == "--web":
            venvList.append("web")
        elif arg == "--desktop":
            venvList.append("desktop")
        elif arg == "--mobile":
            venvList.append("mobile")
        elif arg == "--oauth":
            venvList.append("oauth")
        elif arg == "--name":
            envName = args[args.index(arg) + 1]

    location = "/app-manager/pvenv"

    venv_path = os.path.join(location, envName)
    python_executable = sys.executable
    command = f'{python_executable} -m {envName} {venv_path}'

    # Run the command to create the virtual environment
    os.system(command)
    

    return

def main(args):
    print("Starting...")

    print("Arguments: ", args)

    # Load config from db

    config = None

    with open('config.json') as f:
        config = json.load(f)

    if config is None:
        print("No config found")
        return
    
    if config["initialized"] is False:
        print("Creating workspace")
        initWorkspace(args)

        return
        
    for arg in args:
        if arg == "--help":
            print("Usage: start.py [options]")
            print("Options:")
            print("  --help  Show this help message")
            return
        


        

# Get the location from the command-line argument
location = "/app-manager/pvenv"

# Create the virtual environment
venv_path = os.path.join(location, 'venv')
python_executable = sys.executable
command = f'{python_executable} -m venv {venv_path}'

# Run the command to create the virtual environment
os.system(command)