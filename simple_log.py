def warning(message:str):
    # prints a warning text
    print("<?> WARNING: " + message)

def error(message:str):
    # prints an error text
    print("<!> ERROR: " + message)

def info(message:str):
    # prints an informing text
    print("<i> INFO: " + message)

def log(message:str, type:str="i"):
    # API for this library

    if type == "w":
        warning(message)
    elif type == "e":
        error(message)
    else:
        info(message)
