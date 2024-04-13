SCHEDULER_PATH := $(shell pwd)
PYTHON_VER     := 3.6

FACIAL_BIN := ../r2-facial_recognition_client/venv/bin
FACIAL_DIR := ../r2-facial_recognition_client
FACIAL_EXC := facial_comm.py
FACIAL_PRV := clients/facial.py

MANUAL_BIN := $(SCHEDULER_PATH)/venv/bin
MANUAL_DIR := temp
MANUAL_EXC := manual_comm.py
MANUAL_PRV := clients/manual.py

MVMENT_BIN := $(SCHEDULER_PATH)/venv/bin
MVMENT_DIR := ../c1c0-movement/c1c0-movement/Locomotion
MVMENT_EXC := movement_comm.py
MVMENT_PRV := clients/movement.py

CONTRL_BIN := $(SCHEDULER_PATH)/venv/bin
CONTRL_DIR := temp
CONTRL_EXC := controller_comm.py
CONTRL_PRV := clients/controller.py

all: venv
	make -j 4 scheduler facial movement controller

scheduler: venv
	venv/bin/python scheduler.py

facial: build
	cd $(FACIAL_DIR) && $(FACIAL_BIN)/python $(FACIAL_EXC) $(SCHEDULER_PATH)

manual: build
	cd $(MANUAL_DIR) && $(MANUAL_BIN)/python $(MANUAL_EXC) $(SCHEDULER_PATH)

movement: build
	cd $(MVMENT_DIR) && $(MVMENT_BIN)/python $(MVMENT_EXC) $(SCHEDULER_PATH)

controller: build
	cd $(CONTRL_DIR) && $(CONTRL_BIN)/python $(CONTRL_EXC) $(SCHEDULER_PATH)

build: venv
	mkdir -p $(FACIAL_DIR) && cp $(FACIAL_PRV) $(FACIAL_DIR)/$(FACIAL_EXC)
	mkdir -p $(MANUAL_DIR) && cp $(MANUAL_PRV) $(MANUAL_DIR)/$(MANUAL_EXC)
	mkdir -p $(MVMENT_DIR) && cp $(MVMENT_PRV) $(MVMENT_DIR)/$(MVMENT_EXC)
	mkdir -p $(CONTRL_DIR) && cp $(CONTRL_PRV) $(CONTRL_DIR)/$(CONTRL_EXC)

clean:
	rm -f $(FACIAL_DIR)/$(FACIAL_EXC)
	rm -f $(MANUAL_DIR)/$(MANUAL_EXC)
	rm -f $(MVMENT_DIR)/$(MVMENT_EXC)
	rm -f $(CONTRL_DIR)/$(CONTRL_EXC)
	sudo rm -rf */__pycache__/ temp/

venv:
	python$(PYTHON_VER) -m venv --system-site-packages venv/
	venv/bin/pip install --upgrade pip setuptools wheel
	venv/bin/pip install -r requirements.txt
