import zipfile
with zipfile.PyZipFile("sstv-master.zip", mode="w") as zip_module:
    zip_module.writepy("setup.py")