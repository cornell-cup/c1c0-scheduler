#-------------------------------------------------------------------------------
# This script is used to setup an environment for the c1co project. It requires
# a linux environment with apt-get and git installed. It will install all the
# repositories and dependencies for the c1c0 modules. Credit for this script
# goes to CupRobotics, Christopher De Jesus, and Mohammad Khan.
#
# Script Usage:
# chmod +x setup_jetson.sh
# ./setup_jetson.sh [-v (verbose mode)]
#-------------------------------------------------------------------------------

# Parse command line arguments
if [ "$1" = "-v" ]; then verbose=true;
else verbose=false; fi

# Pretty printing utilities
ruby() { printf "\e[1;31m"; }
aqua() { printf "\e[1;32m"; }
none() { printf "\e[0m"; }
info() { aqua && printf "$1" && none; }
perr() { ruby && printf "$1" && none; }

# Installation utilities
try_install() { # $1 = package name
    info "Installing $1...\n"

    dpkg -s "$1" &> /dev/null
    if [ ! $? -eq 0 ]; then
        if [ "$verbose" = true ]; then sudo apt-get install "$1" || perr "Failed to install $1\n";
        else sudo apt-get install "$1" &> /dev/null || perr "Failed to install $1\n"; fi
    fi

    dpkg -s "$1" &> /dev/null
    if [ ! $? -eq 0 ]; then return 1;
    else return 0; fi
}

try_clone() { # $1 = repo link, $2 = local path
    info "Cloning $1...\n"

    if [ ! -d "$2/.git" ]; then
        if [ "$verbose" = true ]; then git clone "$1" "$2" || perr "Failed to clone $1\n";
        else git clone "$1" "$2" &> /dev/null || perr "Failed to clone $1\n"; fi
    fi

    if  [ ! -d "$2/.git" ]; then return 1;
    else return 0; fi
}

try_checkout() { #1 = local path, $2 = branch name
    if [ "$verbose" = true ]; then git -C $1 checkout $2 || perr "Failed to checkout $2\n";
    else git -C $1 checkout $2 &> /dev/null || perr "Failed to checkout $2\n"; fi

    if [ $(git rev-parse --abbrev-ref HEAD) != "$2" ]; then return 1;
    else return 0; fi
}

# Install python related packages
try_install python3
try_install python3-dev
try_install python3-pip
try_install python3-venv

# Set up path_planning
path_continue=true
path_remote="git@github.com:cornell-cup/C1C0_path_planning.git"
path_local="../c1c0-path-planning"

info "Building path planning...\n"
if $path_continue; then try_clone $path_remote $path_local || path_continue=false; fi
if $path_continue; then try_checkout $path_local "integration" || path_continue=false; fi
if $path_continue; then python3 -m venv "${path_local}/venv" || path_continue=false; fi 
if $path_continue; then source "${path_local}/venv/bin/activate" || path_continue=false; fi
if $path_continue; then pip install -r "${path_local}/requirements.txt" || path_continue=false; fi
if $path_continue; then deactivate || path_continue=false; fi
  
# Set up facial recognition
# try_clone git@github.com:cornell-cup/r2-facial_recognition_client.git ../r2-facial_recognition_client
