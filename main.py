import os
from os.path import expanduser

user_dir = expanduser("~")

java_home = os.getenv("JAVA_HOME")
android_home = os.getenv("ANDROID_HOME")
android_sdk_root = os.getenv("ANDROID_SDK_ROOT")
print(f'{user_dir}{os.linesep}{java_home}{os.linesep}{android_home}{os.linesep}{android_sdk_root}')

os.environ["DEBUSSY"] = "1"

if java_home:
    print('certo')
else:
    print('errado')

print(os.getenv("DEBUSSY"))
def criaEnvVar(txt, path):
    print('a')

#


