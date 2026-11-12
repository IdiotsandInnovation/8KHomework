import os
import urllib.request
import zipfile
import ssl

# Bypass proxy SSL inspection certificate blocks
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

handler = urllib.request.HTTPSHandler(context=ctx)
opener = urllib.request.build_opener(handler)
urllib.request.install_opener(opener)

repo_url = "https://github.com/debrouxl/tilp_and_gfm/archive/refs/heads/master.zip"
zip_path = os.path.expandvars(r"%USERPROFILE%\Downloads\tilp_src.zip")
extract_dir = os.path.expandvars(r"%USERPROFILE%\Documents\tilp_source")

print("Downloading TiLP source repository from GitHub...")
urllib.request.urlretrieve(repo_url, zip_path)

print("Extracting repository contents...")
os.makedirs(extract_dir, exist_ok=True)
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

print("SUCCESS: TiLP source code downloaded and extracted!")
