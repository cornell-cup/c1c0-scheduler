SCHEDULER_PATH := $(shell pwd)
PYTHON_VER := 3.11

MANUAL_DIR := .
MANUAL_EXC := clients/manual.py

FACIAL_DIR := ../r2-facial_recognition_client
FACIAL_PRV := clients/facial.py
FACIAL_EXC := facial.py

all: venv
	venv/bin/python scheduler.py

build:
	cp $(FACIAL_PRV) $(FACIAL_DIR)/$(FACIAL_EXC)

clean:
	rm $(FACIAL_DIR)/$(FACIAL_EXC)

venv:
	python$(PYTHON_VER) -m venv venv
	venv/bin/pip install -r requirements.txt

manual:
	cd $(MANUAL_DIR) && venv/bin/python $(MANUAL_EXC) $(SCHEDULER_PATH)

facial:
	cd $(FACIAL_DIR) && venv/bin/python $(FACIAL_EXC) $(SCHEDULER_PATH)
