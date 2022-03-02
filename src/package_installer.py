import os, sys

for argv in sys.argv: os.system('python3 -m pip install {}'.format(argv))

with open('py_installed', 'w') as file:
	file.write("")

print("All packeges installed!")