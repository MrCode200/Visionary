import win32gui
import win32process
import psutil

def get_active_process_count(process_name: str):
    cmd_count = 0
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            if proc.info['name'] == process_name:
                print(proc.info)
                cmd_count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return cmd_count

def get_foreground_process() -> psutil.Process:
    fg_hwnd = win32gui.GetForegroundWindow()
    _, fg_pid = win32process.GetWindowThreadProcessId(fg_hwnd)
    fg_proc = psutil.Process(fg_pid)
    return fg_proc

if __name__ == '__main__':
    from time import sleep

    while True:
        print(get_foreground_process().name(), get_foreground_process().pid)
        sleep(1)


