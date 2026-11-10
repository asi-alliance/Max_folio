import subprocess

DESCRIPTION = "Execute a shell command."

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return "SUCCESS, RETURN: " + result.stdout + result.stderr
