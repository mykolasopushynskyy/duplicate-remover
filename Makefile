# Define the name of your virtual environment directory
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
BLACK = $(VENV_DIR)/bin/black
AUTOFLAKE = $(VENV_DIR)/bin/autoflake

# Define the directories or files to format and check
SRC_DIRS = .

# Target to create a virtual environment
$(VENV_DIR)/bin/activate:
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install black autoflake

# Target to apply code style using black
format: $(VENV_DIR)/bin/activate
	$(BLACK) $(SRC_DIRS)

# Target to remove unused imports and variables using autoflake
clean-imports: $(VENV_DIR)/bin/activate
	$(AUTOFLAKE) --in-place --remove-all-unused-imports --recursive $(SRC_DIRS)

# Target to run both formatting and import cleanup
lint: format clean-imports

.PHONY: format clean-imports lint $(VENV_DIR)/bin/activate