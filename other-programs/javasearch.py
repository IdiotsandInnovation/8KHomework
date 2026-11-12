import os
import glob
import shutil

def locate_java():
    # 1. Check if java is already in the system PATH
    system_java = shutil.which("javaw") or shutil.which("java")
    if system_java:
        return system_java
        
    # 2. Search common school/developer directories in Program Files
    search_patterns = [
        r"C:\Program Files\Microsoft\*\bin\javaw.exe",
        r"C:\Program Files\Eclipse Adoptium\*\bin\javaw.exe",
        r"C:\Program Files\Java\*\bin\javaw.exe",
        r"C:\Program Files (x86)\Microsoft\*\bin\javaw.exe",
        r"C:\Program Files\JetBrains\*\jbr\bin\javaw.exe" # In case IntelliJ is installed
    ]
    
    for pattern in search_patterns:
        matches = glob.glob(pattern)
        if matches:
            return matches[0] # Returns the first valid javaw.exe found
            
    return None

# Assign it dynamically
JAVA_PATH = locate_java()

if not JAVA_PATH:
    print("Error: Could not find any Java installation on this PC!")
else:
    print(f"Found Java at: {JAVA_PATH}")

