import os
import sys
from appl import appl_accumulator
import shutil
import json

from jinja2 import Template

def proc(root_path, target_path, depth = 0):
	# Pass
	if os.path.exists(os.path.join(root_path, 'pass')):
		return

	# Get base Data
	data_path = root_path
	for i in range(0, depth, 1):
		if not os.path.exists(os.path.join(data_path, 'data.json')):
			data_path = os.path.dirname(data_path)

	data = {}
	jsonfile_path = os.path.join(data_path, 'data.json')
	if os.path.exists(jsonfile_path):
		json_file = open(jsonfile_path, 'r')
		try:
			data = json.loads(json_file.read())
		except:
			data = {}
		json_file.close()


	# Expand
	if os.path.exists(os.path.join(root_path, 'expand')):
		target_path = os.path.dirname(target_path)

	# Check if folder exists
	if os.path.exists(target_path) == False:
		os.makedirs(target_path)

	# Get Folder list
	directories = [d for d in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, d))]
	
	# Check static folder
	if 'static' in directories :
		static_path = os.path.join(root_path, 'static')
		static_files = os.listdir(static_path)

		for file in static_files :
			shutil.copy(os.path.join(static_path, file), os.path.join(target_path, file))
	

	# Check tmpl folder
	if 'tmpl' in directories :
		tmpl_path = os.path.join(root_path, 'tmpl')
		tmpl_files = os.listdir(tmpl_path)

		for file in tmpl_files :
			# Read template file
			f_base = open(os.path.join(tmpl_path, file), 'r')
			tmpl = Template(f_base.read())
			f_base.close()

			# Write output file
			f_out = open(os.path.join(target_path, file), 'w')
			f_out.write(tmpl.render(data = data))
			f_out.close()
	
	# Check appl folder
	if 'appl' in directories :
		appl_path = os.path.join(root_path, 'appl')
		appl_files = os.listdir(appl_path)

		for file in appl_files :
			# Check if target file already exits
			target_filepath = os.path.join(target_path, file)
			if os.path.exists(target_filepath) == False :
				open(target_filepath, 'w+').close() # Create file

			appl_accumulator(target_filepath, os.path.join(appl_path, file), '')
	

	# Check subdirectories
	sub_directories = [d for d in directories if d.find('sub_') == 0]
	for subdir in sub_directories :
		subdir_path = os.path.join(target_path, subdir.replace('sub_', ''))
		proc(os.path.join(root_path, subdir), subdir_path, depth + 1)


if __name__ == "__main__" :
	if len(sys.argv) != 3 :
		print("Input argument is invalid")
		print("Usgae : ")
		print("\tautogenerator <root_path> <target_path>")
		exit()

	proc(sys.argv[1], sys.argv[2])		