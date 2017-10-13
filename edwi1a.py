#author: Przemyslaw Zaworski
#Python version 3.6.0

import urllib.request
import os
import re
from html.parser import HTMLParser
os.system('cls');

def process_html(input):
	s = re.compile('<.*?>')
	output = re.sub(s, '', input) #delete HTML tags
	output = re.sub(r'[^\w\s]','',output) #delete punctuation marks
	return output.lower() #set all lower case

class parsing_html(HTMLParser):
	images=list()
	def handle_starttag(self, tag, attrs):
		if tag == "img":
			for name, value in attrs:
				if name == "src":
					self.output=value;
					
print("Enter URL address: ");
try:
	url = input();
	html = urllib.request.urlopen(url).read();
	parser = parsing_html();
	parser.feed(str(html));
	
	temp_link=url.split('/');
	base=temp_link[0]+'//'+temp_link[2]+'/'+parser.output;
	image_html = urllib.request.urlopen(base).read();
	in_dir = parser.output.split('/');
	if len(in_dir)==1:
		image_file=open(parser.output, 'wb');
		image_file.write(image_html);
		image_file.close();
	if len(in_dir)==2:
		os.makedirs(in_dir[0]);
		image_file=open(in_dir[0]+'/'+in_dir[1], 'wb');
		image_file.write(image_html);
		image_file.close();
	html_file = open("output.html", 'wb');
	html_file.write(html);
	html_file.close(); 
except ValueError:
	print ("Invalid URL address !");

try:	
	temp = open("output.html",'r'); 
	s = temp.read() ;
	pt = process_html(s);
	txt_file = open("output.txt", 'w');
	txt_file.write(pt);
	txt_file.close();
except ValueError:
	print ("Could not create TXT file.");