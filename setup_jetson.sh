try_install() {
	sudo apt-get install $1 || echo "Failed to install $1";
}

try_install python3
try_install python3-dev
try_install python3-pip
try_install python3-venv

