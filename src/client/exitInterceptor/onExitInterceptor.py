import atexit
import os
import sys
import signal
import subprocess
import time

file_name = os.path.basename(__file__)

#import keyboard as kb

def reopen_in_new_terminal(**kwargs):
    subprocess.Popen("start cmd", shell=True)
    time.sleep(1)
    #kb.write(f"python {file_name}")
    time.sleep(0.1)
    #kb.press_and_release("enter")
    time.sleep(1)

atexit.register(reopen_in_new_terminal)
signal.signal(signal.SIGINT, reopen_in_new_terminal)
signal.signal(signal.SIGTERM, reopen_in_new_terminal)
try:
    while True:
        input("Press Enter to continue...")
except KeyboardInterrupt as e:
    print("Exception: ", e)
    reopen_in_new_terminal()
    print(e)