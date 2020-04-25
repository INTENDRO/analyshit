"""
Analyshit

Analyzing the defecational behavior over the span of one year.

Diagrams and Outputs:
- Average values (consistency, size)
- Counts (glück, ninja, etc.)
- Heat Map (consistency, size)
- Average values on Weekdays (consistency, size)


"""

import argparse
import os

def parse_input_arguments():
	parser = argparse.ArgumentParser(description="Analyzing the defecational behavior over the span of one year.")
	parser.add_argument("-f", "--file", help="Specify the desired file.")
	args = parser.parse_args()
	return args

def get_project_directory():
	return os.path.dirname(os.path.realpath(__file__))

def get_newest_filename():
	return sorted(os.listdir("./data"))[-1]

def check_file_exists(file):
	return os.path.exists("./data/"+file)

def main():
	args = parse_input_arguments()
	home_dir = get_project_directory()
	if args.file:
		print(check_file_exists(args.file))
	else:
		filename = get_newest_filename()
		print(filename)



if __name__ == "__main__":
	main()