# Anki Example Usage Adder

This Python program adds example usage sentences to each note in a specified Anki deck using the Anki Connect plugin.

## Prerequisites

To use this program, you will need the following:

1. **Anki** installed (tested with version 24.06.3)
2. **Anki Connect Plugin** (ID: 2055492159)
    - Install instructions: [Anki Connect Plugin](https://ankiweb.net/shared/info/2055492159)
    - Documentation: [Anki Connect Documentation](https://foosoft.net/projects/anki-connect/)

3. **Python 3.7 or above** installed via **pyenv**
4. **Pipenv** for managing dependencies

## Important Notes

- Make sure that Anki is running when you use the program.
- Ensure that you are not viewing the note you are updating in the Anki browser, otherwise, fields will not update. Refer to [this issue](https://github.com/FooSoft/anki-connect/issues/16) for more details.

## Setup Instructions

### Step 1: Install System Dependencies

For a proper setup on Ubuntu (or similar systems), install the required system packages using the following command:

```bash
sudo apt update; sudo apt install --no-install-recommends make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev \
libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

### Step 3: Install Pyenv, Python, Pip and Pipenv
You can install pyenv to manage Python versions using the command below:
```bash
curl https://pyenv.run | bash
```

For detailed installation instructions, visit the [pyenv GitHub page](https://github.com/pyenv/pyenv#installation).

After installing pyenv, you need to restart your terminal and run the following command to install Python:
```bash
pyenv install 3.12
pyenv global 3.12
```

Ensure pip is installed:
```bash
sudo apt-get install python3-pip
```

Then, install Pipenv using the following command:
```bash
pip install --user pipenv
```

### Step 3: Set Up the Virtual Environment

Navigate to the project directory and install the dependencies listed in the Pipfile by running:
```bash
pipenv install
```
This will create a virtual environment with the necessary dependencies.

### Step 4: Running the Program
Before running the program, ensure that Anki is open. Then, activate the virtual environment
```bash
pipenv shell
```

Edit for your needs and run the script as follows:
```bash
pipenv shell
python ./update_examples.py
```
The script will connect to Anki via the Anki Connect API and update the notes with example usage sentences from your specified deck.

## Troubleshooting
- Ensure that you are not viewing the note in Anki's browser during the update, as this will prevent fields from updating.
- If any issues occur with dependencies or pyenv installation, refer to the official documentation of pyenv and Pipenv.
