import os
import sys
import re

def changeCropping(t,l,b,r):
	lines = []
	with open("/etc/hyperion/hyperion.config.json", "r") as config:
		for line in config:
			if line.strip().startswith("\"cropTop"):
				line = re.sub("\d+", str(t), line)
			if line.strip().startswith("\"cropLeft"):
				line = re.sub("\d+", str(l), line)
			if line.strip().startswith("\"cropBottom"):
				line = re.sub("\d+", str(b), line)
			if line.strip().startswith("\"cropRight"):
				line = re.sub("\d+", str(r), line)
			lines.append(line)
	with open("/etc/hyperion/hyperion.config.json", "w") as config:
		config.writelines(lines)


if __name__ == '__main__':
	changeCropping(sys.argv[1], sys.argv[2], 320-int(sys.argv[3]), 480-int(sys.argv[4]))
