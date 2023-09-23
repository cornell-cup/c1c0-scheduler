#-------------------------------------------------------------------------------
# This script is used to setup an environment for the C1C0 project. It requires
# a linux environment with apt-get and git installed. It will install all the
# repositories for the C1C0 modules, set up their virtual environments, and
# download requirements. Credit for this script goes to Christopher De Jesus,
# and Mohammad Khan.
#
# Script Usage:
# chmod +x setup_jetson.sh
# ./setup_jetson.sh [-v (verbose mode)]
#-------------------------------------------------------------------------------

#!/bin/bash

# Parse command line arguments
if [ "$1" = "-v" ]; then verbose=true;
else verbose=false; fi

# Changes terminal text color
ruby() { printf "\e[1;31m"; }
aqua() { printf "\e[1;32m"; }
none() { printf "\e[0m"; }

# Prints a message in color
info() { aqua && printf "$1" && none; }
perr() { ruby && printf "$1" && none; }
bord() { aqua && echo "----------------------------------------" && none; }

# Attempts to get the given linux package. Returns 0 if successful, 1 if not.
try_get() { # $1 = package name
    info "\tGetting $1...\n"

    dpkg -s "$1" &> /dev/null
    if [ ! $? -eq 0 ]; then
        if [ "$verbose" = true ]; then sudo apt-get install "$1" || perr "\tFailed to get $1\n";
        else sudo apt-get install "$1" &> /dev/null || perr "\tFailed to get $1\n"; fi
    fi

    dpkg -s "$1" &> /dev/null
    if [ ! $? -eq 0 ]; then return 1;
    else return 0; fi
}

# Attempts to clone the given git repository to the given repo path. Returns 0
# if successful, 1 if not.
try_clone() { # $1 = repo link, $2 = repo path
    info "\tCloning $1...\n"

    if [ ! -d "$2/.git" ]; then
        if [ "$verbose" = true ]; then git clone "$1" "$2" || perr "\tFailed to clone $1\n";
        else git clone "$1" "$2" &> /dev/null || perr "\tFailed to clone $1\n"; fi
    fi

    if  [ ! -d "$2/.git" ]; then return 1;
    else return 0; fi
}

# Attempts to checkout to the given branch of the given git repository. Returns
# 0 if successful, 1 if not.
try_checkout() { # $1 = repo path, $2 = branch name
    info "\tChecking $1:$2...\n"

    if [ $(git -C $1 rev-parse --abbrev-ref HEAD) != $2 ]; then
        if [ "$verbose" = true ]; then git -C $1 checkout $2 || perr "\tFailed to checkout $1:$2\n";
        else git -C $1 checkout $2 &> /dev/null || perr "\tFailed to checkout $1:$2\n"; fi
    fi

    if [ $(git -C $1 rev-parse --abbrev-ref HEAD) != "$2" ]; then return 1;
    else return 0; fi
}

# Attempts to create a python virtual environment in the given venv path. Returns
# 0 if successful, 1 if not.
try_venv() { # $1 = venv path
    info "\tCreating $1...\n"

    if [ ! -d "$1" ]; then
        if [ "$verbose" = true ]; then python3 -m venv "$1" || perr "Failed to create $1\n";
        else python3 -m venv --system-site-packages "$1" &> /dev/null || perr "Failed to create $1\n"; fi
    fi

    if [ ! -d "$1" ]; then return 1;
    else return 0; fi
}

# Attempts to install the given pip package using the given pip path. Returns 0
# if successful, 1 if not.
try_pip() { # $1 = pip path, $2 = package name
    info "\t\tInstalling $2\n"

    $1 show $2 &> /dev/null
    if [ ! $? -eq 0 ]; then
        if [ "$verbose" = true ]; then $1 install $2 || perr "\t\tFailed to install $2\n";
        else $1 install $2 &> /dev/null || perr "\t\tFailed to install $2\n"; fi
    fi
    $1 show $2 &> /dev/null
    if [ ! $? -eq 0 ]; then return 1;
    else return 0; fi
}

# No check for blis and others (maybe)
special_pip() {
    info "\t\tInstalling $2\n"

    $1 show $2 &> /dev/null
    if [ ! $? -eq 0 ]; then
        if [ "$verbose" = true ]; then $1 install $2 || perr "\t\tFailed to install $2\n";
        else $1 install $2 &> /dev/null || perr "\t\tFailed to install $2\n"; fi
    fi
    info "Running $1 show $2\n"
}

# Attempts to read the given requirements file and install all packages that don't
# need to be built from source. Returns 0 if successful, 1 if not.
try_requirements() { # $1 = pip path, $2 = requirements file
    info "\tReading $2...\n"

    declare -A special
    special["blis"]="BLIS_ARCH=\"arm64\" $1 install" \
    status=0

    info "\tUpgrading $1...\n"
    if [ "$verbose" = true ]; then $1 install --upgrade pip || perr "\t\tFailed to upgrade pip\n";
    else $1 install --upgrade pip &> /dev/null || perr "\t\tFailed to upgrade pip\n"; fi

    while read -r line; do
        for key in ${!special[@]}; do
            if [[ "$line" == *"$key"* ]]; then eval "${special[$key]} $line"; fi
        done

        try_pip $1 $line || status=1

	if [ "$status" = 1 ]; then perr "\t\tFailed to install $line\n"; break 1; fi
    done < $2

    return $status
}

# Attempts to download a zip and extract it into a subfolder


# NOTE: dlib & pyrealsense2 require their own functions due to aarch64 specific build instructions
# Atttempts to install dlib and requisite sublibraries
try_dlib() {
    # Enters ../dlib/build
    cd ../dlib
    # TODO: Check if .whl exists in dist/

    info "\tUpdating submodules...\n"
    git submodule init
    git submodule update

    info "\tRunning cmake...\n"
    mkdir build &> /dev/null # Silently fail
    cd build
    if [ "$verbose" = true ]; then cmake -D DLIB_USE_CUDA=1 ../ || perr "Failed to run cmake pt 1.\n";
    else cmake -D DLIB_USE_CUDA=1 ../ &> /dev/null || perr "Failed to run cmake pt 1.\n"; fi

    if [ "$verbose" = true ]; then cmake --build . --config Release || perr "Failed to run cmake pt 2.\n";
    else cmake --build . --config Release &> /dev/null || perr "Failed to run cmake pt 2.\n"; fi
    
    # TODO: Replace with home dir for script
    cd ../../c1c0-scheduling
    info "\tBuilding python wrapper..."
    python3 setup.py bdist_wheel
}

# Solution from https://github.com/35selim/RealSense-Jetson/blob/main/build_pyrealsense2_and_SDK.sh
try_pyrealsense2() {
    # Enters ../pyrealsense2/build
    # TODO: variable path
    cd ../pyrealsense2
    mkdir build &> /dev/null
    cd build
    sed -i '3iset(CMAKE_CUDA_COMPILER /usr/local/cuda/bin/nvcc)\' ../CMakeLists.txt
    cmake ../ -DBUILD_PYTHON_BINDINGS:bool=true -DPYTHON_EXECUTABLE=/usr/bin/python3 -DCMAKE_BUILD_TYPE=release -DBUILD_EXAMPLES=true -DBUILD_GRAPHICAL_EXAMPLES=true -DBUILD_WITH_CUDA:bool=true
    sudo make uninstall && sudo make clean
    sudo make -j$(($(nproc)-1)) && sudo make install
    echo 'export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.6/pyrealsense2' >> ~/.bashrc
    sudo cp ../config/99-realsense-libusb.rules /etc/udev/rules.d/ && sudo udevadm control --reload-rules && udevadm trigger
    # Exits ../pyrealsense2/build
    cd ../../c1c0-scheduling
}

# Install python related packages
bord && info "Getting Python packages...\n"
try_get python3
try_get python3-dev
try_get python3-pip
try_get python3-venv
try_get python3-wheel


# DLib install
# dlib_continue=true
dlib_continue=false && info "Skipping dlib, will still recheck deps.\n"
dlib_remote="https://github.com/davisking/dlib.git"
dlib_local="../dlib"

bord && info "Building dlib... \n"
# dlib deps
if [ $dlib_continue = true ]; then dlib_deps || info "\tSkipping dlib's dependency check\n" || dlib_continue=false; fi

if [ $dlib_continue = true ]; then try_clone $dlib_remote $dlib_local || dlib_continue=false; fi
if [ $dlib_continue = true ]; then try_dlib || dlib_continue=false; fi

# Pyrealsense2 install
# pyrs2_continue=true
pyrs2_continue=false && info "Skipping pyrealsense2, will still recheck deps.\n"
pyrs2_remote="https://github.com/IntelRealSense/librealsense.git"
pyrs2_local="../pyrealsense2"

bord && info "Building pyrealsense2... \n"
# pyrealsense2 deps
try_get libssl-dev
try_get libxinerama-dev
try_get libxcursor-dev
try_get libcanberra-gtk-module
try_get libcanberra-gtk3-module

if [ $pyrs2_continue = true ]; then try_clone $pyrs2_remote $pyrs2_local || pyrs2_continue=false; fi
if [ $pyrs2_continue = true ]; then try_pyrealsense2 || pyrs2_continue=false; fi

# Path planning information
# path_continue=true
path_continue=false && info "Skipping path-planning, will still recheck deps.\n"
path_remote="git@github.com:cornell-cup/C1C0_path_planning.git"
path_local="../c1c0-path-planning"
path_branch="integration"
path_venv="$path_local/venv"
path_pip="$path_venv/bin/pip"
path_req="$path_local/requirements.txt"

# Set up path planning
bord && info "Building path planning...\n"
if [ $path_continue = true ]; then try_clone $path_remote $path_local || path_continue=false; fi
if [ $path_continue = true ]; then try_checkout $path_local $path_branch || path_continue=false; fi
if [ $path_continue = true ]; then try_venv $path_venv || path_continue=false; fi
if [ $path_continue = true ]; then try_requirements $path_pip $path_req || path_continue=false; fi
if [ $path_continue = false ]; then perr "Failed to build path planning\n"; fi

# Facial recognition information
# facial_continue=true
facial_continue=false && info "Skipping facial-recognition, will still recheck deps.\n"
facial_remote="git@github.com:cornell-cup/r2-facial_recognition_client.git"
facial_local="../r2-facial_recognition_client"
facial_branch="updating"
facial_venv="$facial_local/venv"
facial_pip="$facial_venv/bin/pip"
facial_req="$facial_local/requirements.txt"

# Set up facial recognition
bord && info "Building facial recognition...\n"
if [ $facial_continue = true ]; then try_clone $facial_remote $facial_local || facial_continue=false; fi
if [ $facial_continue = true ]; then try_checkout $facial_local $facial_branch || facial_continue=false; fi
if [ $facial_continue = true ]; then try_venv $facial_venv || facial_continue=false; fi
if [ $facial_continue = true ]; then try_requirements $facial_pip $facial_req || facial_continue=false; fi
if [ $facial_continue = false ]; then perr "Failed to build facial recognition\n"; fi

# Chatbot information
chat_continue=true
chat_remote="git@github.com:cornell-cup/r2-chatbot.git"
chat_local="../r2-chatbot"
chat_branch="chatgpt-integration"
chat_venv="$chat_local/r2_chatterbot/venv"
chat_pip="$chat_venv/bin/pip"
chat_req="$chat_local/r2_chatterbot/requirements.txt"

# Set up chatbot
bord && info "Building chatbot...\n"
try_get portaudio19-dev
try_get python-pyaudio
try_get python3-pyaudio
try_get curl
# As per https://github.com/jetson-nano-wheels/python3.6-blis-0.7.4
np_url="https://github.com/jetson-nano-wheels/python3.6-numpy-1.19.4/releases/download/v0.0.2/numpy-1.19.4-cp36-cp36m-linux_aarch64.whl"
blis_url="https://github.com/jetson-nano-wheels/python3.6-blis-0.7.4/releases/download/v0.0.1/blis-0.7.4-cp36-cp36m-linux_aarch64.whl"

if [ $chat_continue = true ]; then try_clone $chat_remote $chat_local || chat_continue=false; fi
if [ $chat_continue = true ]; then try_checkout $chat_local $chat_branch || chat_continue=false; fi
if [ $chat_continue = true ]; then try_venv $chat_venv || chat_continue=false; fi
# temp
if [ $chat_continue = true ]; then special_pip $chat_pip $np_url || chat_continue=false; fi
if [ $chat_continue = true ]; then special_pip $chat_pip $blis_url || chat_continue=false; fi
# TODO: Fix
if [ $chat_continue = true ]; then $chat_venv/bin/python -m nltk.downloader stopwords $chat_pip $blis_url || chat_continue=false; fi
# end temp
if [ $chat_continue = true ]; then try_requirements $chat_pip $chat_req || chat_continue=false; fi
if [ $chat_continue = false ]; then perr "Failed to build chatbot\n"; fi

# Downloads stanford_ner
# TODO: Later
stanford_ner_file="stanford-ner-4.2.0.zip"
stanford_ner_url="https://downloads.cs.stanford.edu/nlp/software/$stanford_ner_file"
# TODO: Add verbose
# pwd
# curl -o $stanford_ner_file $stanford_ner_url
# tar -xf $stanford_ner_file &> /dev/null

# Object detection information
object_continue=true
object_remote="git@github.com:cornell-cup/r2-object_detection.git"
object_local="../r2-object_detection"
object_branch="blue-arm"
object_venv="$object_local/venv"
object_pip="$object_venv/bin/pip"
object_req="$object_local/requirements.txt"

# Set up object detection
bord && info "Building object detection...\n"
if [ $object_continue = true ]; then try_clone $object_remote $object_local || object_continue=false; fi
if [ $object_continue = true ]; then try_checkout $object_local $object_branch || object_continue=false; fi
if [ $object_continue = true ]; then try_venv $object_venv || object_continue=false; fi
if [ $object_continue = true ]; then try_requirements $object_pip $object_req || object_continue=false; fi
if [ $object_continue = false ]; then perr "Failed to build objection detection\n"; fi

# Movement information
move_continue=true
move_remote="git@github.com:cornell-cup/c1c0-movement.git"
move_local="../c1c0-movement"
move_branch="main"

# Set up movement
bord && info "Building movement...\n"
if [ $move_continue = true ]; then try_clone $move_remote $move_local || move_continue=false; fi
if [ $move_continue = true ]; then try_checkout $move_local $move_branch || move_continue=false; fi
if [ $move_continue = false ]; then perr "Failed to build movement\n"; fi

# Ending script
bord && exit 0
