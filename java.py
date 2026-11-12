# 8KHomework © 2026 by IdiotsAndInnovation is licensed under CC BY-NC-SA 4.0.

import os
import zipfile
import urllib.request
import shutil
import tempfile
import subprocess

url = "https://github.com/adoptium/temurin25-binaries/releases/download/jdk-25.0.5+8/OpenJDK25U-jdk_x64_windows_hotspot_25.0.5_8.zip"
target_dir = r"C:\Java\25-jdk"

print("Downloading Java 25...")
temp_zip = os.path.join(tempfile.gettempdir(), "openjdk-25.zip")
urllib.request.urlretrieve(url, temp_zip)

print("Extracting archive...")
temp_extract = os.path.join(tempfile.gettempdir(), "jdk-extract")
if os.path.exists(temp_extract):
    shutil.rmtree(temp_extract, ignore_errors=True)

with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
    zip_ref.extractall(temp_extract)

extracted_contents = os.listdir(temp_extract)
source_jdk_path = os.path.join(temp_extract, extracted_contents[0])

print(f"Creating root directory at {target_dir}...")
os.makedirs(target_dir, exist_ok=True)

print("Copying files...")
for item in os.listdir(source_jdk_path):
    s = os.path.join(source_jdk_path, item)
    d = os.path.join(target_dir, item)
    if os.path.isdir(s):
        shutil.copytree(s, d, dirs_exist_ok=True)
    else:
        shutil.copy2(s, d)

print("Configuring system environment variables via PowerShell...")
# Use PowerShell .NET API to set machine-level JAVA_HOME and PATH cleanly
ps_env_script = f'''
[Environment]::SetEnvironmentVariable("JAVA_HOME", "{target_dir}", "Machine")
$path = [Environment]::GetEnvironmentVariable("PATH", "Machine")
$binPath = "{target_dir}\\bin"
if ($path -notlike "*$binPath*") {{
    [Environment]::SetEnvironmentVariable("PATH", "$path;$binPath", "Machine")
}}
'''
subprocess.run(["powershell", "-Command", ps_env_script], check=True)

print(f"SUCCESS: Java 25 successfully installed and configured at {target_dir}!")
