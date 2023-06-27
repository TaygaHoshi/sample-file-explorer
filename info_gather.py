import subprocess
from simple_log import log
import threading
from time import sleep
#from platform import platform

def normalize_out(cmd):
    return cmd.stdout.decode().strip()

def normalize_err(cmd):
    return cmd.stderr.decode().strip()

def run(cmd:str):
    return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def threaded_run(cmd:str):
    _th = threading.Thread(target=_run, args=[cmd])
    _th.start()

def _run(cmd:str):
    _subp = subprocess.run(cmd + " &", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    log(f"Running {cmd} in another thread.", "i")
    
    err = normalize_err(_subp)
    out = normalize_out(_subp)

    if err:
        _err = err.split("\n")
        for line in _err:
            log(line, "w")
    
    if out:
        _out = out.split("\n")
        for line in _out:
            log(line, "i")

def search_file(filename):
    return normalize_out(run("find -iname '*" + filename + "*'")).split("\n")

def get_battery_charge():
    try:
        return normalize_out(run("upower -i $(upower -e | grep 'BAT') | grep 'percentage' | awk '{print $2}'"))
    except:
        log("Unable to get battery charge.", "e")
        return "0%"

def get_kernel_version():
    try:
        return normalize_out(run("uname -r"))
    except:
        log("Error getting current kernel version.", "e")
        return ""

def get_desktop_environment():
    return normalize_out(run("echo $DESKTOP_SESSION"))

def get_ram_usage():
    used = normalize_out(run("free -m | head -2 | tail -1 | awk '{print $3}'"))
    total = normalize_out(run("free -m | head -2 | tail -1 | awk '{print $2}'"))
    return f"Memory ({int(used)*100//int(total)}%)\n{used}/{total} MB"

def update_dynamic_labels(dynamic_label, window):
    label_update = threading.Thread(target=_update_labels, args=[dynamic_label, window])
    label_update.start()


def _update_labels(label, window):
    while window.isVisible():
        
        battery = f"Battery\n{get_battery_charge()}\n\n"
        ram = get_ram_usage()

        label.setText(battery + ram)
        label.update()
    
        sleep(5)

# print(get_kernel_version())
# print(get_battery_charge()[:-1])
# print(get_desktop_manager())
