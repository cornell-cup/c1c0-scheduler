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
try_install() { # $1 = package name, $2 = terminal command
    info "Installing $1...\n"
    if ! [ -x "$(command -v $2)"]; then
        if [ "$verbose" = true ]; then
            sudo apt-get install "$1" || perr "Failed to install $1\n";
        else
            sudo apt-get install "$1" &> /dev/null || perr "Failed to install $1\n";
        fi
    fi
}

try_clone() { # $1 = repo link, $2 = local path
    info "Cloning $1...\n"
    if [ ! -d "$2/.git" ]; then
        if [ "$verbose" = true ]; then
            git clone "$1" "$2" || perr "Failed to clone $1\n";
        else
            git clone "$1" "$2" &> /dev/null || perr "Failed to clone $1\n";
        fi
    fi
}

# Install python related packages
try_install python3
try_install python3-dev
try_install python3-pip
try_install python3-venv

# Set up facial recognition
try_clone git@github.com:cornell-cup/r2-facial_recognition_client.git ../r2-facial_recognition_client
