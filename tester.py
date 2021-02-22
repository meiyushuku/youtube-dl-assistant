import sys
import threading
import time
from rename import rename_exe

VERSION = "0.9.0"
print("youtube-dl-assistant-private")
print("Version %s (2021) Developed by Meiyu Shuku" % VERSION)
print("")

def switch():
    global monit_mission
    input_menu_orig = input("Type here >>> ")
    input_menu = input_menu_orig.strip()
    if input_menu == "rename":
        rename_exe()
    elif input_menu == "monit -on":
        monit_mission = 1
        thread.start()
        return switch()
    elif input_menu == "":
        print("Not entered.")
        return switch()
    else:
        print("Command is not defined.")
        return switch()

def monit():
    while monit_mission:
        rename_exe()
        time.sleep(1)

thread = threading.Thread(target = monit)


controller = 1
while controller:
    switch()

    print('Task is completed. Type "menu" to return to menu or exit by any other.')
    input_end_orig = input("Type here >>> ")
    input_end = input_end_orig.strip()
    if input_end == "menu":
        print("Returned to menu.")
        pass
    else:
        sys.exit()