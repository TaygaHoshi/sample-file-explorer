# sample-file-explorer
This is a sample file explorer combined with a simple system monitor, written in Python with PyQt6. I don't know how long I will continue improving this, but it's functional already.

## Installation
These steps below should be self-explanatory. I advise you to check the .sh files and the makefile first, before running these commands.
```bash
git clone https://github.com/TaygaHoshi/sample-file-explorer.git
virtualenv sample-file-explorer
cd sample-file-explorer
chmod u+x install.sh
chmod u+x start.sh
make install
```

## Running
After installing, you can either "chmod u+x gui.py" and double click gui.py or use one of these commands below:
```
make
make run
```
