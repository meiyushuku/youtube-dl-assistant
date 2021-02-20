import time
import sys

VERSION = "0.9.0"
print("youtube-dl-assistant-private")
print("Version %s (2021) Developed by Meiyu Shuku" % VERSION)
print("")

def switch():
    input_menu_orig = input("Type here >>> ")
    input_menu = input_menu_orig.strip()
    if input_menu == "filing":
        import filing
    elif input_menu == "":
        print("Not entered.")
        return switch()
    else:
        print("Command is not defined.")
        return switch()

controller = time.time()
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