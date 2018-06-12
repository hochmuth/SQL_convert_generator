# Parses through the folder and lists all the files.
import glob

file_list = []
for filename in glob.glob('*.csv'):
	file_list.append(filename)