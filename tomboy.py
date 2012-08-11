#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Author: Seowon Jung
# Email: jswlinux@gmail.com
# irc.freenode #ubuntu-ko Seony

import re
import os

def replace_decorations(string_content, link):
	string_content = string_content.replace('</bold>', '</b>')
	string_content = string_content.replace('<bold>', '<b>')
	string_content = string_content.replace('</highlight>', '</font>')
	string_content = string_content.replace('<highlight>', '<font style="background-color: yellow">')
	string_content = string_content.replace('</italic>', '</i>')
	string_content = string_content.replace('<italic>', '<i>')
	string_content = string_content.replace('</size:small>', '</font>')
	string_content = string_content.replace('<size:small>', '<font size="2">')
	string_content = string_content.replace('</size:large>', '</font>')
	string_content = string_content.replace('<size:large>', '<font size="4">')
	string_content = string_content.replace('</size:huge>', '</font>')
	string_content = string_content.replace('<size:huge>', '<font size="5">')
	string_content = string_content.replace('</list-item>', '</li>')
	string_content = string_content.replace('<list-item dir="ltr">', '\t<li>')
	string_content = string_content.replace('</list>', '\n</ul>\n')
	string_content = string_content.replace('<list>', '<ul>\n')
	string_content = string_content.replace('<br>', '<br>\n')

	# It won't work properly if a memo has two or more links. Needed to improve
	string_content = string_content.replace('</link:internal>', '</a>')
	string_content = string_content.replace('<link:internal>', '<a href="%s.html">' %link)
	return string_content

HOME_DIR = os.path.expanduser('~')
WORK_DIR = '%s/.local/share/tomboy' %HOME_DIR

for f in os.listdir(WORK_DIR):
	ext = os.path.splitext(f)[-1]

	if ext == '.note':
		print 'File name: %s' %f,
		sourceFile = open(os.path.join(WORK_DIR, f))
		content = sourceFile.read()

		title = re.findall(r'<title>(.+)</title>', content)
		dup_title = re.findall(r'<note-content(\sversion="\d.\d">|>)(.*)', content)
		link = re.findall(r'<link:internal>(.+)</link:internal>', content)
		content = content.replace(dup_title[0][1], '')
		content = content.replace('\n', '<br>')

		note_content = re.findall(r'<note-content(\sversion="\d.\d">|>)(.+)</note-content>', content)

		try:
			html_content = '<font size="4"><b>%s</b></font>%s' %(title[0], replace_decorations(note_content[0][1], link[0]))
		except:
			html_content = '<font size="4"><b>%s</b></font>%s' %(title[0], replace_decorations(note_content[0][1], ''))

		header = '<html>\n<head>\n\t<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n\t<title>%s</title>\n</head>\n<body>\n\n' %title[0]
		footer = '\n</body>\n</html>'
		output = open('%s/%s.html' %(WORK_DIR, title[0]), 'w')
		output.write(header+html_content+footer)
		output.close()

		if os.path.isfile(os.path.join(WORK_DIR, '%s.html' %title[0])) and os.path.getsize(os.path.join(WORK_DIR, '%s.html' %title[0])) > 0:
			print '-> %s.html created.' %title[0]
		else:
			print '-> Error' %title[0]

		sourceFile.close()

print 'Done'