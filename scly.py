'''
IMPORTANT NOTE:
I am not responsible for any trouble you get in for using this program, and your mileage WILL vary, as this is a pretty untested script and I am just generally terrible at coding in Python.
Please run this script in another desktop, terminal/shell windows are quite sus to your teachers and peers.
Do not redistribute this to anyone. If it spreads too fast then it will get patched. Don't leak this script.
It your teacher asks why they can't see you on Securly, say some BS excuse, and quickly do Ctrl + C in the terminal/shell to terminate this script.
'''
import psutil
import time

target_process = "Classroom.exe"
# If it doesn't work properly, try directing it to C:\Program Files\Securly\Classroom\1.3.34.28\Classroom.exe
# Note that the above directory may vary, it should be correct as of November 2026, but if it's not right, go to Task Manager, right-click the Classroom process, Properties, then see what path it has.

print(f"Looking for {target_process}...")

while True:
    try:
        found = False
        for proc in psutil.process_iter(['name', 'pid']):
            if proc.info['name'] and proc.info['name'].lower() == target_process.lower():
                found = True
                pid = proc.info['pid']
                print(f"Found {target_process} (PID: {pid}). Attempting to terminate...")
                
                try:
                    # Attempt to terminate the process
                    proc.terminate()
                    
                    # Wait briefly to confirm it has stopped
                    gone, alive = psutil.wait_procs([proc], timeout=1)
                    
                    if alive:
                        # If still alive, force kill
                        print("Termination stop failed, attempting force kill...")
                        proc.kill()
                        gone, alive = psutil.wait_procs([proc], timeout=1)
                        
                        if alive:
                            print(f"[ERROR]: Failed to stop {target_process} (PID: {pid}). Process is still running (Access Denied or Protected).")
                        else:
                            print(f"Successfully killed {target_process} (PID: {pid}).")
                    else:
                        print(f"Successfully terminated {target_process} (PID: {pid}).")
                        
                except psutil.AccessDenied:
                    print(f"Stopped")
                except psutil.NoSuchProcess:
                    print(f"Process {target_process} (PID: {pid}) was already closed.")
                except Exception as e:
                    print(f"[ERROR]: An unexpected error occurred while stopping {target_process}: {e}")
                    
        if not found:
            pass
            
    except Exception as e:
        print(f"[ERROR]: Error iterating processes: {e}")
    time.sleep(1)
