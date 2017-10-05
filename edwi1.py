#author: Przemyslaw Zaworski
#Python version 3.6.0

import urllib.request
import os
import re
os.system('cls');

def process_html(input):
  s = re.compile('<.*?>')
  output = re.sub(s, '', input) #delete HTML tags
  output = re.sub(r'[^\w\s]','',output) #delete punctuation marks
  return output.lower() #set all lower case

print("Enter URL address: ");
try:
	url = input();
	html = urllib.request.urlopen(url).read();
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