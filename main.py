import os
from array import array
from os.path import expanduser
from pathlib import Path

android_sdk_root = os.getenv("ANDROID_SDK_ROOT")
user_dir = expanduser("~")
os.environ["ANDROID_SDK_ROOT"]  = user_dir + '\\AppData\\Local\\Android\\Sdk'
if not os.path.isdir(str(android_sdk_root)+'\\build-tools\\22.0.1'):
    print("a")
print(android_sdk_root)