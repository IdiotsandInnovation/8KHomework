import os
import shutil
import subprocess

source_exe = r"C:\Users\1065187\Downloads\tailscale-setup-1.104.5.exe"
target_dir = r"C:\Tailscale"
target_exe = os.path.join(target_dir, "tailscale-setup.exe")

print(f"Creating protected directory: {target_dir}")
os.makedirs(target_dir, exist_ok=True)

print("Copying installer to protected path...")
shutil.copy2(source_exe, target_exe)

print("Executing installer from protected path...")
subprocess.run([target_exe, "/verysilent", "/norestart"], check=True)

print("SUCCESS: Tailscale installed successfully!")
