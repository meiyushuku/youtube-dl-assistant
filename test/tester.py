from doc import tool

config = tool.json_reader("doc/config.json")

path = config["general"]["workDir"]
isvideo = config["general"]["isVideo"]

print(path)
print(isvideo)