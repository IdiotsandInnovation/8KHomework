import psutil
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def getProcesses(targetFolder):
    processes = []
    for process in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            if targetFolder in str(process.info['exe']):
                processes.append(process)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes

def killProcesses(processes):
    for process in processes:
        try:
            process.terminate()
            logging.info(f"Terminated {process.name()} (PID: {process.pid})")
        except psutil.AccessDenied:
            logging.warning(f"Access Denied to {process.name()} (PID: {process.pid})")
        except psutil.NoSuchProcess:
            logging.info(f"Already terminated {process.name()} (PID: {process.pid})")

def main():
    targetFolder = r"DyKnow"
    interval = 1
    logging.info("Monitoring started...")
    try:
        while True:
            processes = getProcesses(targetFolder)
            if processes:
                killProcesses(processes)
            else:
                logging.info("No matching processes found.")
            time.sleep(interval)
    except KeyboardInterrupt:
        logging.info("Monitoring stopped.")

if __name__ == "__main__":
    main()
