import sys
from random import randint
import platform
import re
import time
import requests
import string
import winsound
import operator
import threading
import sqlite3
import os
import asyncio
import msvcrt
import ctypes
#from ctypes import windll, byref
from ctypes.wintypes import SMALL_RECT
from ctypes import *
from msvcrt import getch
os.system('cls');
os.system('title Database manager');
#winsound.PlaySound('.\\music.dll', winsound.SND_ASYNC)


language_pl=[];
language_en=[];


def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    letter = ord('A')
    while bitmask > 0:
        if bitmask & 1:
            drives.append(chr(letter) + ':\\')
        bitmask >>= 1
        letter += 1

    return drives


def SetWindow ( width,  height):	
	coord = wintypes._COORD()
	coord.x=width
	coord.y=height
	rect = wintypes.SMALL_RECT()
	rect.Top = 0
	rect.Left = 0
	rect.Bottom = height - 1
	rect.Right = width - 1
#handle = ctypes.windll.kernel32.GetStdHandle(-11)
	STDOUT = -11
	hdl = windll.kernel32.GetStdHandle(STDOUT)
#bufsize = wintypes._COORD(100, 320) # rows, columns
#bufsize2 = wintypes._COORD(200, 220) # rows, columns
	windll.kernel32.SetConsoleScreenBufferSize(hdl, coord)
#windll.kernel32.SetConsoleScreenBufferSize(hdl, bufsize2)
#rect = wintypes.SMALL_RECT(0, 30, 150, 150) # (left, top, right, bottom)
	windll.kernel32.SetConsoleWindowInfo(hdl, True, byref(rect))

window_width=80;
window_height=40;
SetWindow(window_width,window_height);





class _CursorInfo(ctypes.Structure):
	_fields_ = [("size", ctypes.c_int),
	("visible", ctypes.c_byte)]
def hide_cursor():
	ci = _CursorInfo()
	handle = ctypes.windll.kernel32.GetStdHandle(-11)
	ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
	ci.visible = False
	ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12
hide_cursor();
def show_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
class COORD(Structure):
	pass
 
COORD._fields_ = [("X", c_short), ("Y", c_short)]

def print_at(r, c, s):
	h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
	windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))
	c = s.encode("windows-1252","ignore")
	windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)
 
SHORT = c_short
WORD = c_ushort
class SMALL_RECT(Structure):
  """struct in wincon.h."""
  _fields_ = [
    ("Left", SHORT),
    ("Top", SHORT),
    ("Right", SHORT),
    ("Bottom", SHORT)]

class CONSOLE_SCREEN_BUFFER_INFO(Structure):
  """struct in wincon.h."""
  _fields_ = [
    ("dwSize", COORD),
    ("dwCursorPosition", COORD),
    ("wAttributes", WORD),
    ("srWindow", SMALL_RECT),
    ("dwMaximumWindowSize", COORD)]

# wincon.h
FOREGROUND_BLACK     = 0x0000
FOREGROUND_BLUE      = 0x0001
FOREGROUND_GREEN     = 0x0002
FOREGROUND_CYAN      = 0x0003
FOREGROUND_RED       = 0x0004
FOREGROUND_MAGENTA   = 0x0005
FOREGROUND_YELLOW    = 0x0006
FOREGROUND_GREY      = 0x0007
FOREGROUND_INTENSITY = 0x0008 # foreground color is intensified.

BACKGROUND_BLACK     = 0x0000
BACKGROUND_BLUE      = 0x0010
BACKGROUND_GREEN     = 0x0020
BACKGROUND_CYAN      = 0x0030
BACKGROUND_RED       = 0x0040
BACKGROUND_MAGENTA   = 0x0050
BACKGROUND_YELLOW    = 0x0060
BACKGROUND_GREY      = 0x0070
BACKGROUND_INTENSITY = 0x0080 # background color is intensified.

stdout_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute
GetConsoleScreenBufferInfo = windll.kernel32.GetConsoleScreenBufferInfo
def get_text_attr():
	"""Returns the character attributes (colors) of the console screen
	buffer."""
	csbi = CONSOLE_SCREEN_BUFFER_INFO()
	GetConsoleScreenBufferInfo(stdout_handle, byref(csbi))
	return csbi.wAttributes

def set_text_attr(color):
	"""Sets the character attributes (colors) of the console screen
	buffer. Color is a combination of foreground and background color,
	foreground and background intensity."""
	SetConsoleTextAttribute(stdout_handle, color)




default_colors = get_text_attr()
default_bg = default_colors & 0x0070
default_fg = default_colors & 0x0007
set_text_attr(FOREGROUND_BLACK | BACKGROUND_RED | FOREGROUND_INTENSITY)
print_at(10, 35, "Load database")
set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
print_at(11, 35, "Save database")
print_at(12, 35, "Options")
print_at(13, 35, "Help")
print_at(14, 35, "Exit")
counter =1;
koniec=0;


def chess():
	os.system('cls');
	for i in range(0,79):
		for ii in range(0,39):
			if ((i%2==0 and ii%2==0)):
				for n in range(1):
					print_at(ii,i,chr(219));


	time.sleep(20.0);
	
def loading():
	os.system('cls');
	print_at(0,0,"Initializing kernel...");
	time.sleep(1.5);
	print_at(1,0,"Detected CPU: "+platform.processor()+" ... OK");
	time.sleep(2.5);
	print_at(2,0,"Detected operating system: "+platform.system()+" ... OK");
	time.sleep(2.0);
	print_at(3,0,"Python version: "+platform.python_version()+" ... OK");
	time.sleep(1.0);
	print_at(4,0,"Loading main thread");
	for i in range(2):
		print_at(4,20,".  ");
		time.sleep(1.0);
		print_at(4,20,".. ");
		time.sleep(1.0);
		print_at(4,20,"...");
		time.sleep(1.0);

	os.system('cls');
	print_at(20,35,"Loading resources...");
	print_at(26,70,"0 % ");
	mn=0;
	loader=chr(219)+chr(219)+chr(219)+chr(219)+chr(219)+chr(219)+chr(219)+chr(219)+chr(219)+chr(219);
	set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY);
	for i in range (5):
		print_at(25,15+i*10,chr(219)+chr(219)+chr(219)+chr(219)+chr(219)+chr(219)+chr(219)+chr(219)+chr(219)+chr(219));
		print_at(26,15+i*10,chr(219)+chr(219)+chr(219)+chr(219)+chr(219)+chr(219)+chr(219)+chr(219)+chr(219)+chr(219));
		#print_at(27,15+i*5,chr(219)+chr(219)+chr(219)+chr(219)+chr(219));
		#print_at(28,15+i*5,chr(219)+chr(219)+chr(219)+chr(219)+chr(219));
	set_text_attr(FOREGROUND_RED| default_bg | FOREGROUND_INTENSITY);
	for i in range(5):
		time.sleep(0.2);
		mn=mn+20;
		print_at(25,15,loader);
		print_at(26,15,loader);
		loader=loader+chr(219)+chr(219)+chr(219)+chr(219)+chr(219)+chr(219)+chr(219)+chr(219)+chr(219)+chr(219);
		#print_at(27,15+i*5,chr(219)+chr(219)+chr(219)+chr(219)+chr(219));
		#print_at(28,15+i*5,chr(219)+chr(219)+chr(219)+chr(219)+chr(219));
		set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY);
		print_at(26,70,str(mn)+" % ");
		set_text_attr(FOREGROUND_RED| default_bg | FOREGROUND_INTENSITY);
	os.system('cls');
	set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY);
def logo():
	print_at(0, 4, chr(219));
	print_at(1, 4, chr(219));
	print_at(2, 4, chr(219));
	print_at(3, 4, chr(219));
	print_at(4, 4, chr(219));
	print_at(0, 5, chr(219));
	print_at(0, 6, chr(219));
	print_at(0, 7, chr(219));
	print_at(1, 7, chr(219));
	print_at(2, 7, chr(219));
	print_at(2, 6, chr(219));
	print_at(2, 5, chr(219));

	print_at(0, 9, chr(219));
	print_at(1, 9, chr(219));
	print_at(2, 9, chr(219));
	print_at(3, 9, chr(219));
	print_at(4, 9, chr(219));
	print_at(0, 10, chr(219));
	print_at(0, 11, chr(219));
	print_at(0, 12, chr(219));
	print_at(1, 12, chr(219));
	print_at(2, 12, chr(219));
	print_at(2, 11, chr(219));
	print_at(2, 10, chr(219));
	print_at(3, 11, chr(219));
	print_at(4, 12, chr(219));

	print_at(0, 14, chr(219));
	print_at(0, 15, chr(219));
	print_at(0, 16, chr(219));
	print_at(0, 17, chr(219));
	print_at(1, 17, chr(219));
	print_at(2, 16, chr(219));
	print_at(3, 15, chr(219));
	print_at(4, 14, chr(219));
	print_at(4, 15, chr(219));
	print_at(4, 16, chr(219));
	print_at(4, 17, chr(219));

	print_at(0, 19, chr(219));
	print_at(0, 20, chr(219));
	print_at(0, 21, chr(219));
	print_at(0, 22, chr(219));
	print_at(1, 19, chr(219));
	print_at(2, 19, chr(219));
	print_at(3, 19, chr(219));
	print_at(4, 19, chr(219));
	print_at(2, 19, chr(219));
	print_at(2, 20, chr(219));
	print_at(2, 21, chr(219));
	print_at(2, 22, chr(219));
	print_at(4, 19, chr(219));
	print_at(4, 20, chr(219));
	print_at(4, 21, chr(219));
	print_at(4, 22, chr(219));

	print_at(0, 24, chr(219));
	print_at(1, 24, chr(219));
	print_at(2, 24, chr(219));
	print_at(3, 24, chr(219));
	print_at(4, 24, chr(219));
	print_at(1, 25, chr(219));
	print_at(2, 26, chr(219));
	print_at(1, 27, chr(219));
	print_at(0, 28, chr(219));
	print_at(1, 28, chr(219));
	print_at(2, 28, chr(219));
	print_at(3, 28, chr(219));
	print_at(4, 28, chr(219));

	print_at(0, 30, chr(219));
	print_at(0, 31, chr(219));
	print_at(0, 32, chr(219));
	print_at(0, 33, chr(219));
	print_at(1, 30, chr(219));
	print_at(2, 30, chr(219));
	print_at(3, 30, chr(219));
	print_at(4, 30, chr(219));
	print_at(2, 30, chr(219));
	print_at(2, 31, chr(219));
	print_at(2, 32, chr(219));
	print_at(2, 33, chr(219));
	print_at(4, 30, chr(219));
	print_at(4, 31, chr(219));
	print_at(4, 32, chr(219));
	print_at(4, 33, chr(219));
	
	print_at(0, 35, chr(219));
	print_at(1, 35, chr(219));
	print_at(2, 35, chr(219));
	print_at(3, 35, chr(219));
	print_at(4, 35, chr(219));
	print_at(2, 36, chr(219));
	print_at(1, 37, chr(219));
	print_at(0, 38, chr(219));
	print_at(3, 37, chr(219));
	print_at(4, 38, chr(219));
def banner():
	x=40;
	print_at(22, x, "C");
	threading.Timer(1, banner).start();
	x=+1;
tyl = BACKGROUND_RED;
przod=FOREGROUND_GREY;


chess();
loading();
logo();
set_text_attr(przod| tyl | FOREGROUND_INTENSITY)
print_at(10, 35, "Load database")
set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
print_at(11, 35, "Save database")
print_at(12, 35, "Options")
print_at(13, 35, "Help")
print_at(14, 35, "Exit")

ll=0;
lll=0;
llll=0;
level=1;
skip=False;
disk_level=0;
przod_lista = [FOREGROUND_GREY,FOREGROUND_GREEN,FOREGROUND_YELLOW,FOREGROUND_RED,FOREGROUND_BLUE,FOREGROUND_CYAN,FOREGROUND_MAGENTA];
tyl_lista = [BACKGROUND_GREEN,BACKGROUND_YELLOW,BACKGROUND_RED,BACKGROUND_BLUE,BACKGROUND_CYAN,BACKGROUND_MAGENTA,BACKGROUND_BLACK];
path=os.getcwd();
plik_bazy=str(path+"\\default.cfg");
f = open(plik_bazy, 'w')
f.close()
#poczatek programu

while True:
	

	logo();
	if (level==1):
		key = ord(getch())
	if (key == 72 and counter==2) or (key==13 and counter==10) or (level==0):
		os.system('cls');
		counter=1;
		level=1;
		set_text_attr(przod| tyl | FOREGROUND_INTENSITY)
		print_at(10, 35, "Load database")
		set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
		print_at(11, 35, "Save database")
		print_at(12, 35, "Options")
		print_at(13, 35, "Help")
		print_at(14, 35, "Exit")
	elif (key==13 and counter==1):
		os.system('cls');
		#show_cursor();
		files=[]
		dirs=[]
		path=os.getcwd();
		position=0;
		dirs.append("..");
		for name in os.listdir(path):
			if os.path.isfile(os.path.join(path,name)):
				files.append(name);
			if os.path.isdir(os.path.join(path,name)):
				dirs.append(name);
		#SetWindow(window_width,len(dirs)+len(files)+3);
		os.system('cls');
		position=position+1;
		print ("Current directory: "+path);
		#print("<DIR> ..");
		for index in range(len(dirs)):
			if index==position:
				set_text_attr(przod | tyl | FOREGROUND_INTENSITY);
				print_at(index+2,0,"<DIR> "+dirs[index]);
				set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)				
			else:
				print_at(index+2,0,"<DIR> "+dirs[index]);
		for nnn in range(len(files)):
			if position==nnn+len(dirs):
				set_text_attr(przod | tyl | FOREGROUND_INTENSITY);
				print_at(nnn+len(dirs)+2,0,"      "+files[nnn]);
				set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
			elif position>len(dirs)+len(files):
				position=position-1
			else:
				print_at(nnn+len(dirs)+2,0,"      "+files[nnn]);
		index=0;
		nnn=0;
		while True:

			if (skip==False):
				key2 = ord(getch());
			if (skip==True):
				skip=False;
				#disk_level=0;

			if (key2==80) and (position<(len(dirs) + len(files)-1) and (disk_level==0)   ):
				os.system('cls');
				position=position+1;
				print ("Current directory: "+path);
				#print("<DIR> ..");
				for index in range(len(dirs)):
					if index==position:
						set_text_attr(przod | tyl | FOREGROUND_INTENSITY);
						print_at(index+2,0,"<DIR> "+dirs[index]);
						set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
					
					else:
						print_at(index+2,0,"<DIR> "+dirs[index]);
				for nnn in range(len(files)):
					if position==nnn+len(dirs):
						set_text_attr(przod | tyl | FOREGROUND_INTENSITY);
						print_at(nnn+len(dirs)+2,0,"      "+files[nnn]);
						set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
					elif position>len(dirs)+len(files):
						position=position-1
					else:
						print_at(nnn+len(dirs)+2,0,"      "+files[nnn]);
				index=0;
				nnn=0;
				if (position+2<window_height):
					print_at(0,35," ");
			if ( ((key2==13)) and (position==0) and (disk_level==0) ):
				os.system('cls');
				#print("test");
				#os.system('title '+str(disk_level));

				files=[]
				dirs=[]
				head, tail = os.path.split(path)
				if (tail==""):
					disk_level=1;
					#skip=False;
				path=head;
				position=0;
				dirs.append("..");
				for name in os.listdir(path):
					if os.path.isfile(os.path.join(path,name)):
						files.append(name)
					if os.path.isdir(os.path.join(path,name)):
						dirs.append(name);
				print ("Current directory: "+path);
				#SetWindow(window_width,len(dirs)+len(files)+3);
				#print("<DIR> ..");
				for index in range(len(dirs)):
					if index==position:
						set_text_attr(przod | tyl | FOREGROUND_INTENSITY);
						print_at(index+2,0,"<DIR> "+dirs[index]);
						set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
					
					else:
						print_at(index+2,0,"<DIR> "+dirs[index]);
				for nnn in range(len(files)):
					if position==nnn+len(dirs):
						set_text_attr(przod | tyl | FOREGROUND_INTENSITY);
						print_at(nnn+len(dirs)+2,0,"      "+files[nnn]);
						set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
					elif position>len(dirs)+len(files):
						position=position-1
					else:
						print_at(nnn+len(dirs)+2,0,"      "+files[nnn]);
				index=0;
				nnn=0;
				if (position+2<window_height):
					print_at(0,35," ");
				#os.system('pause');
				if (skip==True):
					break;
				#key3 = ord(getch())
				#if key3==27:
				#	break;
			if ( (key2==13) and (position==0) and (tail=="") and (disk_level==1) ):
				#head, tail = os.path.split(path)
				#if (tail==""):
				os.system('cls');
				print ("Available disks: ");
				iterator=1;
				dyski=get_drives();
				#os.system('title '+str(disk_level));
				for i in range(len(dyski)):
					print(dyski[i]);
				print_at(iterator,30,"<-");
				while True:
					key3 = ord(getch());
					
					if  (key3==80) and (iterator<len(dyski)):
						os.system('cls');
						print ("Available disks: ");
						for i in range(len(dyski)):
							print(dyski[i]);
						iterator+=1;
						print_at(iterator,30,"<-");

					if  (key3==72) and (iterator>1):
						os.system('cls');
						print ("Available disks: ");
						for i in range(len(dyski)):
							print(dyski[i]);
						iterator-=1;
						print_at(iterator,30,"<-");

					if (key3==13):
						disk_level=0;
						path=dyski[iterator-1];
						os.system('title '+str(disk_level));
						key2=13;
						position=1;
						skip=True;
						break;
			if ( (key2==13) and (position>0) and (position<len(dirs)) ):
				os.system('cls');
				#print("test");
				head, tail = os.path.split(path)
				path=path+"\\"+dirs[position];
				files=[]
				dirs=[]
				position=0;
				dirs.append("..");
				try:
					for name in os.listdir(path):
						if os.path.isfile(os.path.join(path,name)):
							files.append(name)
						if os.path.isdir(os.path.join(path,name)):
							dirs.append(name);
				except:
						print("Access denied. ");
						os.system('pause');
						os.system('cls');
						level=0;
						break;
				print ("Current directory: "+path);
				#SetWindow(window_width,len(dirs)+len(files)+3);
				#print("<DIR> ..");
				for index in range(len(dirs)):
					if index==position:
						set_text_attr(przod | tyl | FOREGROUND_INTENSITY);
						print_at(index+2,0,"<DIR> "+dirs[index]);
						set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
					
					else:
						print_at(index+2,0,"<DIR> "+dirs[index]);
				for nnn in range(len(files)):
					if position==nnn+len(dirs):
						set_text_attr(przod | tyl | FOREGROUND_INTENSITY);
						print_at(nnn+len(dirs)+2,0,"      "+files[nnn]);
						set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
					elif position>len(dirs)+len(files):
						position=position-1
					else:
						print_at(nnn+len(dirs)+2,0,"      "+files[nnn]);
				index=0;
				nnn=0;
				if (position+2<window_height):
					print_at(0,35," ");
			if (key2==72) and (position>0) and (disk_level==0):
				os.system('cls');
				position=position-1;
				print ("Current directory: "+path);
				#print("<DIR> ..");
				for index in range(len(dirs)):
					if index==position:
						set_text_attr(przod | tyl | FOREGROUND_INTENSITY);
						print_at(index+2,0,"<DIR> "+dirs[index]);
						set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
					
					else:
						print_at(index+2,0,"<DIR> "+dirs[index]);
				for nnn in range(len(files)):
					if position==nnn+len(dirs):
						set_text_attr(przod | tyl | FOREGROUND_INTENSITY);
						print_at(nnn+len(dirs)+2,0,"      "+files[nnn]);
						set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
					elif position>len(dirs)+len(files):
						position=position-1
					else:
						print_at(nnn+len(dirs)+2,0,"      "+files[nnn]);
				index=0;
				nnn=0;
				if (position+2<window_height):
					print_at(0,35," ");
			if ( (key2==13) and (position>0)):
				os.system('cls');
				plik_bazy=path+"\\"+files[position-len(dirs)];
				db = sqlite3.connect(plik_bazy);
				level=0;
				position=0;
				break;
			if (key2==27):
				os.system('cls');
				level=0;
				break;
		#print("Select file to load:");
		#plik_bazy=input();
		#db = sqlite3.connect(plik_bazy);
		#hide_cursor();
		#level=0
		#os.system('cls');
	elif (key==13 and counter==2):
		os.system('cls');
		db = sqlite3.connect(plik_bazy);
		cursor = db.cursor();
		db.execute('''CREATE TABLE IF NOT EXISTS LISTA (ID INTEGER PRIMARY KEY AUTOINCREMENT,IMIE TEXT NOT NULL, NAZWISKO TEXT NOT NULL);''');
		db.commit();
		while True:
			if level==0:
				key = ord(getch());
			if key == 51:
				os.system('cls');
				show_cursor();
				print ("Write full name splitted by space character: ");
				try:
					napis = input().split()
					db.execute("INSERT  INTO LISTA (IMIE,NAZWISKO) VALUES (?,?)",(napis[0],napis[1]));
					db.commit();
					hide_cursor();
					print ("New item was inserted into database successfully. ");
				except sqlite3.Error as e:
					hide_cursor();
					print ("Error")
					continue

			if (key == 49) or (level==1):
				os.system('cls');
				show_cursor();
				v=0;
				print ("Database "+plik_bazy+" loaded succesfully ");
				print_at (2,0,"\n");
				print_at (3,0,"(1)-sort by name (2)-sort by surname (3)-new (4)-delete (5)-save to (6)-url\n");
				cursor = db.execute("SELECT  imie, nazwisko  from LISTA ORDER BY IMIE")
				print_at (4,0,"\n");
				print ("---------------------------------------------------------------------");
				print ("| Nr    | Name                     | Surname                        |");
				print ("---------------------------------------------------------------------");
				z=8;
				print_at(z,0,"|");
				print_at(z,8,"| ");
				print_at(z,35,"| ");
				print_at(z,68,"|");
				for row in cursor:
					v=v+1;
					print_at(z,0,"| "+str(v));
					print_at(z,8,"| ");
					print_at(z,10,row[0]);
					print_at(z,35,"| ");
					print_at(z,37,row[1]);
					print_at(z,68,"|");
					z=z+1;

				print ("\n---------------------------------------------------------------------");
				'''
				przerwa3="";
				przerwa4="";
				wiersze=[];
				element="";
				#max(map(len, row)
				
				 for row in cursor:
					for bbb in range(30-len(row[0])):
						przerwa3=przerwa3+" "; 
					for bbb in range(30-len(row[1])):
						przerwa4=przerwa4+" "; 	
					element="|"+row[0]+ przerwa3+"| "+row[1]+przerwa4+"| ";
					print (element);
					wiersze.append(element);
					v=v+1; 
				przerwa3="";
				przerwa4="";
				
				rrr=max(map(len, wiersze));
				linia="";
				for x in range(rrr):
					linia=linia+"-";
				print(");
				print_at(5,0,linia);
				element1="| First Name                  |Last Name                    |";
				print_at(6,0,element1);
				print_at(7,0,linia);
				'''
				print_at(1,0,"(total "+str(v)+" records sorted by name).");
				level=0;
				hide_cursor();
			if key == 52:
				os.system('cls');
				show_cursor();
				print ("Write surname to delete an element ");
				napis = input();
				db.execute("DELETE  FROM LISTA  WHERE NAZWISKO=?",(napis,));
				db.commit();
				print ("Selected item was deleted from database successfully. ");
				hide_cursor();
			if key == 50:
				os.system('cls');
				show_cursor();
				v=0;
				cursor = db.execute("SELECT  imie, nazwisko  from LISTA ORDER BY nazwisko")
				print ("Database "+plik_bazy+" loaded succesfully ");
				print_at (2,0,"\n");
				print_at (3,0,"(1)-sort by name (2)-sort by surname (3)-new (4)-delete (5)-save to (6)-url \n");
				print_at (4,0,"\n");
				'''
				print ("--------------------------------");
				
				przerwa3="";
				przerwa4="";
				wiersze=[];
				element="";
				#max(map(len, row)
				for row in cursor:
					for bbb in range(30-len(row[0])):
						przerwa3=przerwa3+" "; 
					for bbb in range(30-len(row[1])):
						przerwa4=przerwa4+" "; 	
					element="| "+row[0]+ przerwa3+"| "+row[1]+przerwa4+"| ";
					print (element);
					wiersze.append(element);
					v=v+1;
					przerwa3="";
					przerwa4="";
				if (len(wiersze)>0):
					rrr=max(map(len, wiersze));
					linia="";
					for x in range(rrr):
						linia=linia+"-";
					print(linia);
					print_at(5,0,linia);
				'''
				print ("---------------------------------------------------------------------");
				print ("| Nr    | Name                     | Surname                        |");
				print ("---------------------------------------------------------------------");
				z=8;
				print_at(z,0,"|");
				print_at(z,8,"| ");
				print_at(z,35,"| ");
				print_at(z,68,"|");
				for row in cursor:
					v=v+1;
					print_at(z,0,"| "+str(v));
					print_at(z,8,"| ");
					print_at(z,10,row[0]);
					print_at(z,35,"| ");
					print_at(z,37,row[1]);
					print_at(z,68,"|");
					z=z+1;

				print ("\n---------------------------------------------------------------------");
				print_at(1,0,"(total "+str(v)+" records sorted by surname).");

				hide_cursor();
			if key==53:
				os.system('cls');
				show_cursor();
				print ("Save database as (enter full path):");
				sciezka = input();
				os.system('copy '+plik_bazy+' '+sciezka);
				db.close();
				plik_bazy=sciezka;
				db = sqlite3.connect(plik_bazy);
				cursor = db.cursor();
				print ("File "+sciezka+" was created successfully");
				hide_cursor();
			if key==54:
				os.system('cls');
				show_cursor();	
				print("Enter URL adress: ");
				try:
					url=input();
					response = requests.get(url)
					object=response.text;
					object=object.replace(") ",", ");
					object=object.replace("\n",", ");
					array = object.split(", ");
					print ("------------------------------------------------------------------------------");
					print ("| Nr    | Name           | Surname                 | Album   | E-Mail         |");
					print ("------------------------------------------------------------------------------");
					zz=5;
					#for i in range(len(array)):
					rows=int(len(array)/5);
					h=0;
					for i in range(rows):
						print_at(zz,0,"|");
						print_at(zz,2,array[h]);
						print_at(zz,8,"|");
						print_at(zz,10,array[h+1]);
						print_at(zz,25,"|");
						print_at(zz,27,array[h+2]);
						print_at(zz,51,"|");					
						print_at(zz,53,array[h+3]);
						print_at(zz,61,"|");					
						print_at(zz,63,array[h+4]);
						print_at(zz,78,"|");
						zz=zz+1;
						h=h+5;
					
					print_at (zz,0,"------------------------------------------------------------------------------");
					hide_cursor();
				except ValueError:
					print ("Error...");
			if key==55:
				os.system('cls');
				show_cursor();	
				print("Enter absolute TXT file path: ");
				file_path=input();
				F = open(file_path,"r");
				hide_cursor();
			if key==27:
				db.close();
				break;
		level=0
		os.system('cls');

	elif (key == 80 and counter==1) or (key == 72 and counter==3):
		counter=2;
		print_at(10, 35, "Load database")
		set_text_attr(przod| tyl | FOREGROUND_INTENSITY)
		print_at(11, 35, "Save database")
		set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
		print_at(12, 35, "Options")
		print_at(13, 35, "Help")
		print_at(14, 35, "Exit")
	elif (key == 80 and counter==2) or (key == 72 and counter==4):
		counter=3;
		print_at(10, 35, "Load database")
		print_at(11, 35, "Save database")
		set_text_attr(przod | tyl | FOREGROUND_INTENSITY)
		print_at(12, 35, "Options")
		set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
		print_at(13, 35, "Help")
		print_at(14, 35, "Exit")
	elif (key == 80 and counter==3) or (key == 72 and counter==100):
		counter=4;
		print_at(10, 35, "Load database")
		print_at(11, 35, "Save database")
		print_at(12, 35, "Options")
		set_text_attr(przod | tyl| FOREGROUND_INTENSITY)
		print_at(13, 35, "Help")
		set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
		print_at(14, 35, "Exit")
	elif (key == 80 and counter==4):
		counter=100;
		print_at(10, 35, "Load database")
		print_at(11, 35, "Save database")
		print_at(12, 35, "Options")
		print_at(13, 35, "Help")
		set_text_attr(przod | tyl| FOREGROUND_INTENSITY)
		print_at(14, 35, "Exit")
		set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
		
	elif (key==13 and counter==3) or (key == 72 and counter==6):
		counter=5;
		os.system('cls');
		set_text_attr(przod | tyl| FOREGROUND_INTENSITY)
		print_at(10, 35, "Foreground color")
		print_at(10, 55, chr(219)+chr(219)+chr(219))
		print_at(11, 55, "   ")
		set_text_attr(default_fg| default_bg | FOREGROUND_INTENSITY)
		print_at(11, 35, "Background color")
		print_at(12, 35, "Screen width")
		if window_width>99:
			print_at(12, 55, str(window_width))
		else:
			print_at(12, 55, " "+str(window_width))
		print_at(13, 35, "Screen height")
		print_at(13, 55, " "+str(window_height))
		print_at(15, 35, "Apply settings")
		print_at(14, 35, "Language")
		print_at(14,56,"EN")

	elif (key == 77 and counter==5):
		przod=przod_lista[lll];
		if lll<len(przod_lista)-1:
			lll+=1;
		set_text_attr(przod | tyl| FOREGROUND_INTENSITY)
		print_at(10, 35, "Foreground color")
		set_text_attr(przod | tyl| FOREGROUND_INTENSITY)
		print_at(10, 55, chr(219)+chr(219)+chr(219))
		set_text_attr(default_fg| default_bg | FOREGROUND_INTENSITY)
		print_at(11, 35, "Background color")
		print_at(12, 35, "Screen width")
		print_at(13, 35, "Screen height")
		print_at(15, 35, "Apply settings")
		print_at(14, 35, "Language")
		print_at(14,56,"EN")
	elif (key == 75 and counter==5):
		przod=przod_lista[lll];
		if lll>0:
			lll-=1;
		set_text_attr(przod | tyl| FOREGROUND_INTENSITY)
		print_at(10, 35, "Foreground color")
		set_text_attr(przod | tyl| FOREGROUND_INTENSITY)
		print_at(10, 55, chr(219)+chr(219)+chr(219))
		set_text_attr(default_fg| default_bg | FOREGROUND_INTENSITY)
		print_at(11, 35, "Background color")
		print_at(12, 35, "Screen width")
		print_at(13, 35, "Screen height")
		print_at(15, 35, "Apply settings")
		print_at(14, 35, "Language")		
		print_at(14,56,"EN")


	
	elif (key == 80 and counter==5) or (key == 72 and counter==7):
		counter=6;
		print_at(10, 35, "Foreground color")
		set_text_attr(przod | tyl | FOREGROUND_INTENSITY)
		print_at(11, 35, "Background color")
		print_at(11, 55, "   ")
		set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
		print_at(12, 35, "Screen width")
		print_at(13, 35, "Screen height")
		print_at(15, 35, "Apply settings")
		print_at(14, 35, "Language")		
		print_at(14,56,"EN")
	elif (key == 77 and counter==6):
		tyl=tyl_lista[ll];
		if ll<len(tyl_lista)-1:
			ll+=1;
		print_at(10, 35, "Foreground color")
		set_text_attr(przod| tyl | FOREGROUND_INTENSITY)
		print_at(11, 35, "Background color")
		print_at(11, 55, "   ")
		set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
		print_at(12, 35, "Screen width")
		print_at(13, 35, "Screen height")
		print_at(15, 35, "Apply settings")
		print_at(14, 35, "Language")
		print_at(14,56,"EN")
	elif (key == 75 and counter==6):
		tyl=tyl_lista[ll];
		if ll>0:
			ll-=1;
		print_at(10, 35, "Foreground color")
		set_text_attr(przod| tyl | FOREGROUND_INTENSITY)
		print_at(11, 35, "Background color")
		print_at(11, 55, "   ")
		set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
		print_at(12, 35, "Screen width")
		print_at(13, 35, "Screen height")
		print_at(15, 35, "Apply settings")
		print_at(14, 35, "Language")
		print_at(14,56,"EN")
	elif (key == 80 and counter==6) or (key == 72 and counter==8):
		counter=7;
		print_at(10, 35, "Foreground color")
		print_at(11, 35, "Background color")
		set_text_attr(przod | tyl | FOREGROUND_INTENSITY)
		print_at(12, 35, "Screen width")
		set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
		print_at(13, 35, "Screen height")
		print_at(15, 35, "Apply settings")
		print_at(14, 35, "Language")
		print_at(14,56,"EN")
	elif (key == 77 and counter==7):
		window_width=window_width+1;
		SetWindow(window_width,window_height);
		print_at(10, 35, "Foreground color")
		print_at(11, 35, "Background color")
		set_text_attr(przod | tyl | FOREGROUND_INTENSITY)
		print_at(12, 35, "Screen width")
		set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
		if window_width>99:
			print_at(12, 55, str(window_width))
		else:
			print_at(12, 55, " "+str(window_width))
		print_at(13, 35, "Screen height")
		print_at(15, 35, "Apply settings")
		print_at(14, 35, "Language")
		print_at(14,56,"EN")
	elif (key == 75 and counter==7):
		window_width=window_width-1;
		SetWindow(window_width,window_height);
		print_at(10, 35, "Foreground color")
		print_at(11, 35, "Background color")
		set_text_attr(przod | tyl | FOREGROUND_INTENSITY)
		print_at(12, 35, "Screen width")
		set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
		if window_width>99:
			print_at(12, 55, str(window_width))
		else:
			print_at(12, 55, " "+str(window_width))
		print_at(13, 35, "Screen height")
		print_at(15, 35, "Apply settings")	
		print_at(14, 35, "Language")
		print_at(14,56,"EN")

	elif (key == 80 and counter==7) or (key == 72 and counter==9) :
		counter=8;
		print_at(10, 35, "Foreground color")
		print_at(11, 35, "Background color")
		print_at(12, 35, "Screen width")
		set_text_attr(przod | tyl | FOREGROUND_INTENSITY)
		print_at(13, 35, "Screen height")
		set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
		print_at(15, 35, "Apply settings")	
		print_at(14, 35, "Language")
		print_at(14,56,"EN")
	elif (key == 77 and counter==8):
		window_height=window_height+1;
		SetWindow(window_width,window_height);
		print_at(10, 35, "Foreground color")
		print_at(11, 35, "Background color")
		print_at(12, 35, "Screen width")
		set_text_attr(przod | tyl | FOREGROUND_INTENSITY)
		print_at(13, 35, "Screen height")
		set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
		if window_height>99:
			print_at(13, 55, str(window_height))
		else:
			print_at(13, 55, " "+str(window_height))
		print_at(15, 35, "Apply settings")
		print_at(14, 35, "Language")
		print_at(14,56,"EN")
	elif (key == 75 and counter==8):
		window_height=window_height-1;
		SetWindow(window_width,window_height);
		print_at(10, 35, "Foreground color")
		print_at(11, 35, "Background color")
		print_at(12, 35, "Screen width")
		set_text_attr(przod | tyl | FOREGROUND_INTENSITY)
		print_at(13, 35, "Screen height")
		set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
		if window_height>99:
			print_at(13, 55, str(window_height))
		else:
			print_at(13, 55, " "+str(window_height))
		print_at(15, 35, "Apply settings")
		print_at(14, 35, "Language")		
		print_at(14,56,"EN")
	elif (key == 80 and counter==8)  or (key == 72 and counter==10) :
		counter=9;
		print_at(10, 35, "Foreground color")
		print_at(11, 35, "Background color")
		print_at(12, 35, "Screen width")
		print_at(13, 35, "Screen height")
		print_at(15, 35, "Apply settings")	
		set_text_attr(przod | tyl | FOREGROUND_INTENSITY)
		print_at(14, 35, "Language")
		set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)
		print_at(14,56,"EN")
	elif (key == 80 and counter==9) :
		counter=10;
		print_at(10, 35, "Foreground color")
		print_at(11, 35, "Background color")
		print_at(12, 35, "Screen width")
		print_at(13, 35, "Screen height")


		
		set_text_attr(przod | tyl | FOREGROUND_INTENSITY)
		print_at(15, 35, "Apply settings")	
		set_text_attr(FOREGROUND_GREY| default_bg | FOREGROUND_INTENSITY)	
		print_at(14, 35, "Language")
		print_at(14,56,"EN")
	elif (key==13 and counter==4):
		os.system('cls');
		print ("DATABASE MANAGER v. 0.1 build 21.04.2017");
		print ("Author: Przemyslaw Zaworski");
		print();
		print("LOAD DATABASE -> set handle to specific file.");
		print("SAVE DATABASE -> <1> key -> Sort elements by first name.");
		print("SAVE DATABASE -> <2> key -> Sort elements by last name.");
		print("SAVE DATABASE -> <3> key -> Create new element.");
		print("SAVE DATABASE -> <4> key -> Delete existing element.");		
		print("SAVE DATABASE -> <5> key -> Save copy of the loaded database");	
		print("OPTIONS -> set various environment options.");	
		print();
		print("When no database is specified by LOAD DATABASE section, application create");
		print("temporal database in current directory - file <default.cfg> ");
		print("Please remember that all operations like creating and deleting elements work at");
		print("current database and cannot be undone. To avoid issues, please first make");
		print("a copy of the loaded database by <5> key.");
		print();
		os.system('pause');
		#os.system('cls');
		level=0;
	elif (key==13 and counter==100):
		os.system('cls');
		show_cursor();
		koniec=1;
		set_text_attr(FOREGROUND_GREY | BACKGROUND_BLACK | FOREGROUND_INTENSITY)
		window_width=80;
		window_height=40;
		SetWindow(window_width,window_height);
		exit();