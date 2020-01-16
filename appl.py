from jinja2 import Template
import re
import os

def appl_accumulator(target_filepath, base_filepath, signature):
	comment_begin = re.compile('\/\* USER CODE BEGIN \w+ \*\/')
	comment_end = re.compile('\/\* USER CODE END \w+ \*\/')

	user = {}

	# Read target file
	f_target = open(target_filepath, 'r')
	while True:
		line = f_target.readline().replace('\t', '')
		if not line: break

		tag_check = comment_begin.findall(line)
		if tag_check:
			tag = tag_check[0].split('/* USER CODE BEGIN ')[1].split(' */')[0]
			user[tag] = ''
			while True:
				line = f_target.readline().replace('\t', '')
				if not line: break
				if comment_end.findall(line): break

				user[tag] = user[tag] + line

			if len(user[tag]):
				user[tag] = user[tag][:-1]


	f_target.close()

	# Write target file
	f_base = open(base_filepath, 'r')
	tmpl_base = Template(f_base.read())
	f_base.close()

	f_target = open(target_filepath, 'w')
	f_target.write(tmpl_base.render(user = user, signature = signature))
	f_target.close()