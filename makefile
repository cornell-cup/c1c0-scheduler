SCHEDULER_PATH := $(shell pwd)
PYTHON_VER     := 3.11
.PHONY: all scheduler facial manual movement controller chatbot

all: venv
	make -j 4 scheduler facial movement controller

gui: venv
	venv/bin/python gui.py

scheduler: venv
	venv/bin/python scheduler.py

FACIAL_BIN := ../c1c0-facial-recognition/venv/bin
FACIAL_DIR := ../c1c0-facial-recognition
FACIAL_EXC := facial_comm.py
FACIAL_PRV := clients/facial.py

facial:
	cd $(FACIAL_DIR) && sudo $(FACIAL_BIN)/python $(FACIAL_EXC) $(SCHEDULER_PATH)

OBJECT_BIN := ../r2-object_detection/venv/bin
OBJECT_DIR := ../r2-object_detection
OBJECT_EXC := object_comm.py
OBJECT_PRV := clients/object.py

object:
	cd $(OBJECT_DIR) && $(OBJECT_BIN)/python $(OBJECT_EXC) $(SCHEDULER_PATH)

MANUAL_BIN := $(SCHEDULER_PATH)/venv/bin
MANUAL_DIR := temp
MANUAL_EXC := manual_comm.py
MANUAL_PRV := clients/manual.py

manual:
	cd $(MANUAL_DIR) && $(MANUAL_BIN)/python $(MANUAL_EXC) $(SCHEDULER_PATH)

MVMENT_BIN := $(SCHEDULER_PATH)/venv/bin
MVMENT_DIR := ../c1c0-movement/c1c0-movement/Locomotion
MVMENT_EXC := movement_comm.py
MVMENT_PRV := clients/movement.py

movement:
	cd $(MVMENT_DIR) && $(MVMENT_BIN)/python $(MVMENT_EXC) $(SCHEDULER_PATH)

CONTRL_BIN := $(SCHEDULER_PATH)/venv/bin
CONTRL_DIR := temp
CONTRL_EXC := controller_comm.py
CONTRL_PRV := clients/controller.py

controller:
	cd $(CONTRL_DIR) && $(CONTRL_BIN)/python $(CONTRL_EXC) $(SCHEDULER_PATH)

CHATBT_BIN := ../c1c0-chatbot/venv/bin
CHATBT_DIR := ../c1c0-chatbot
CHATBT_EXC := chatbot_comm.py
CHATBT_PRV := clients/chatbot.py

chatbot:
	cd $(CHATBT_DIR) && $(CHATBT_BIN)/python $(CHATBT_EXC) $(SCHEDULER_PATH)

gui-wave:
	cd $(CHATBT_DIR) && $(CHATBT_BIN)/python $(CHATBT_EXC) $(SCHEDULER_PATH) wave.wav

gui-detect:
	cd $(CHATBT_DIR) && $(CHATBT_BIN)/python $(CHATBT_EXC) $(SCHEDULER_PATH) object.wav

build: venv
	mkdir -p $(FACIAL_DIR) && cp $(FACIAL_PRV) $(FACIAL_DIR)/$(FACIAL_EXC)
	mkdir -p $(OBJECT_DIR) && cp $(OBJECT_PRV) $(OBJECT_DIR)/$(OBJECT_EXC)
	mkdir -p $(MANUAL_DIR) && cp $(MANUAL_PRV) $(MANUAL_DIR)/$(MANUAL_EXC)
	mkdir -p $(MVMENT_DIR) && cp $(MVMENT_PRV) $(MVMENT_DIR)/$(MVMENT_EXC)
	mkdir -p $(CONTRL_DIR) && cp $(CONTRL_PRV) $(CONTRL_DIR)/$(CONTRL_EXC)
	mkdir -p $(CHATBT_DIR) && cp $(CHATBT_PRV) $(CHATBT_DIR)/$(CHATBT_EXC)

clean:
	rm -f $(FACIAL_DIR)/$(FACIAL_EXC)
	rm -f $(MANUAL_DIR)/$(MANUAL_EXC)
	rm -f $(MVMENT_DIR)/$(MVMENT_EXC)
	rm -f $(CONTRL_DIR)/$(CONTRL_EXC)
	rm -f $(CHATBT_DIR)/$(CHATBT_EXC)
	sudo rm -rf */__pycache__/ temp/

venv:
	python$(PYTHON_VER) -m venv --system-site-packages venv/
	venv/bin/pip install --upgrade pip setuptools wheel
	venv/bin/pip install -r requirements.txt

fix:
	sed -i '' 's/abs(val) \> self.axis_threshold/True/g' venv/lib/python*/xbox360controller/controller.py
