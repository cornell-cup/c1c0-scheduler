#-------------------------------------------------------------------------------
# This script is used to setup an environment for the c1co project. It requires
# a linux environment with apt-get and git installed. It will install all the
# repositories for the c1c0 modules. Credit for this script goes to  Christopher
# De Jesus, and Mohammad Khan.
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
bord() { aqua && echo "--------------------------------------------------------------------------" && none; }

# Installation utilities
try_install() { # $1 = package name
    info "\tInstalling $1...\n"

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
    info "\tCloning $1...\n"

    if [ ! -d "$2/.git" ]; then
        if [ "$verbose" = true ]; then git clone "$1" "$2" || perr "Failed to clone $1\n";
        else git clone "$1" "$2" &> /dev/null || perr "Failed to clone $1\n"; fi
    fi

    if  [ ! -d "$2/.git" ]; then return 1;
    else return 0; fi
}

try_checkout() { #1 = local path, $2 = branch name
    info "\tChecking $2...\n"

    if [ $(git -C $1 rev-parse --abbrev-ref HEAD) != $2 ]; then
        if [ "$verbose" = true ]; then git -C $1 checkout $2 || perr "Failed to checkout $2\n";
        else git -C $1 checkout $2 &> /dev/null || perr "Failed to checkout $2\n"; fi
    fi

    if [ $(git -C $1 rev-parse --abbrev-ref HEAD) != "$2" ]; then return 1;
    else return 0; fi
}

# Install python related packages
bord && info "Installing libraries...\n"
try_install python3
try_install python3-dev
try_install python3-pip
try_install python3-venv

# Set up path planning
path_continue=true
path_remote="git@github.com:cornell-cup/C1C0_path_planning.git"
path_local="../c1c0-path-planning"

bord && info "Building path planning...\n"
if [ $path_continue = true ]; then try_clone $path_remote $path_local || path_continue=false; fi
if [ $path_continue = true ]; then try_checkout $path_local "integration" || path_continue=false; fi
if [ $path_continue = false ]; then perr "Failed to build path planning\n"; fi

# if $path_continue; then python3 -m venv "${path_local}/venv" || path_continue=false; fi 
# if $path_continue; then source "${path_local}/venv/bin/activate" || path_continue=false; fi
# if $path_continue; then pip install -r "${path_local}/requirements.txt" || path_continue=false; fi
# if $path_continue; then deactivate || path_continue=false; fi

# Set up facial recognition
facial_continue=true
facial_remote="git@github.com:cornell-cup/r2-facial_recognition_client.git"
facial_local="../r2-facial_recognition_client"

bord && info "Building facial recognition...\n"
if [ $facial_continue = true ]; then try_clone $facial_remote $facial_local || facial_continue=false; fi
if [ $facial_continue = true ]; then try_checkout $facial_local "updating" || facial_continue=false; fi
if [ $facial_continue = false ]; then perr "Failed to build facial recognition\n"; fi 

# Set up chatbot
chat_continue=true
chat_remote="git@github.com:cornell-cup/r2-chatbot.git"
chat_local="../r2-chatbot"

bord && info "Building chatbot...\n"
if [ $chat_continue = true ]; then try_clone $chat_remote $chat_local || chat_continue=false; fi
if [ $chat_continue = true ]; then try_checkout $chat_local "master" || chat_continue=false; fi
if [ $chat_continue = false ]; then perr "Failed to build chatbot\n"; fi

# Set up object detection
object_continue=true
object_remote="git@github.com:cornell-cup/r2-object_detection.git"
object_local="../r2-object_detection"

bord && info "Building object detection...\n"
if [ $object_continue = true ]; then try_clone $object_remote $object_local || object_continue=false; fi
if [ $object_continue = true ]; then try_checkout $object_local "blue-arm" || object_continue=false; fi
if [ $object_continue = false ]; then perr "Failed to build objection detection\n"; fi

# Set up movement
move_continue=true
move_remote="git@github.com:cornell-cup/c1c0-movement.git"
move_local="../c1c0-movement"

bord && info "Building movement...\n"
if [ $move_continue = true ]; then try_clone $move_remote $move_local || move_continue=false; fi
if [ $move_continue = true ]; then try_checkout $move_local "main" || move_continue=false; fi
if [ $move_continue = false ]; then perr "Failed to build movement\n"; fi

# Ending script
bord
