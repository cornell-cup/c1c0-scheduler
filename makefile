SCHEDULER_PATH := $(shell pwd)
PYTHON_VER     := 3.11

FACIAL_BIN := ../r2-facial_recognition_client/venv/bin
FACIAL_DIR := ../r2-facial_recognition_client
FACIAL_EXC := facial_comm.py
FACIAL_PRV := clients/facial.py

MANUAL_BIN := $(SCHEDULER_PATH)/venv/bin
MANUAL_DIR := temp
MANUAL_EXC := manual_comm.py
MANUAL_PRV := clients/manual.py

all: venv
	venv/bin/python scheduler.py

facial:
	cd $(FACIAL_DIR) && $(FACIAL_BIN)/python $(FACIAL_EXC) $(SCHEDULER_PATH)

manual:
	cd $(MANUAL_DIR) && $(MANUAL_BIN)/python $(MANUAL_EXC) $(SCHEDULER_PATH)

build:
	mkdir -p $(FACIAL_DIR) && cp $(FACIAL_PRV) $(FACIAL_DIR)/$(FACIAL_EXC)
	mkdir -p $(MANUAL_DIR) && cp $(MANUAL_PRV) $(MANUAL_DIR)/$(MANUAL_EXC)

clean:
	rm -f $(FACIAL_DIR)/$(FACIAL_EXC)
	rm -f $(MANUAL_DIR)/$(MANUAL_EXC)
	rm -rf */__pycache__/ temp/

venv:
	rm -rf venv/
	python$(PYTHON_VER) -m venv venv/
	venv/bin/pip install -r requirements.txt
