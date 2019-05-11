import os
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from pygame import mixer
import time
from mutagen.mp3 import MP3
import threading
from tkinter import ttk


root = Tk()

root.title('WINK')
root.iconbitmap('Images/Wink.ico')


statusbar = ttk.Label(root, text='Welcome to WINK', relief=SUNKEN, anchor=W)					# W stands for west(anchor does not take argument left or right etc. It takes North, south etc.)
statusbar.pack(side=BOTTOM, fill=X)


leftframe = Frame(root)
leftframe.pack(side = LEFT, padx=30)


def browse_file():
	global filename_path
	filename_path = filedialog.askopenfilename()
	add_to_playlist(filename_path)

playlist = []

def add_to_playlist(filename):
	filename = os.path.basename(filename)
	index = 0
	playlistbox.insert(index, filename)
	playlist.insert(index, filename_path)
	#index += 1


playlistbox = Listbox(leftframe)
playlistbox.pack()

addbtn = ttk.Button(leftframe, text = '+ Add', command = browse_file)
addbtn.pack(side=LEFT)


def del_song():
	selected_song = playlistbox.curselection()
	selected_song = int(selected_song[0])
	playlistbox.delete(selected_song)
	playlist.pop(selected_song)


delbtn = ttk.Button(leftframe, text = '- Del', command = del_song)
delbtn.pack(side=LEFT)

rightframe = Frame(root)
rightframe.pack()

topframe = Frame(rightframe)
topframe.pack()

lengthlabel = ttk.Label(topframe, text = "Total length : --:--")
lengthlabel.pack(pady=5)

currenttimelabel = ttk.Label(topframe, text = "Current time : --:--", relief = GROOVE)
currenttimelabel.pack()



def show_details(play_song):
	
	file_data = os.path.splitext(play_song)

	if file_data[1] == ".mp3":
		audio = MP3(play_song)
		total_length = audio.info.length

	else: 
		a = mixer.Sound(play_song)
		total_length = a.get_length()

	# div- total_length/60, mod- total_length % 60
	mins, secs = divmod(total_length, 60)
	mins = round(mins)
	secs = round(secs)
	time_format = "{:02d}:{:02d}".format(mins, secs)
	lengthlabel['text'] = "Total length : "+ time_format

	t1 = threading.Thread(target=start_count, args=(total_length,))
	t1.start()



def start_count(t):
	global paused
	# mixer.music.get_busy() returns False when we press the stop button (music stops playing)
	current_time = 0
	while  current_time <= t and mixer.music.get_busy():
		if paused:
			continue
		else:
			mins, secs = divmod(current_time, 60)
			mins = round(mins)
			secs = round(secs)
			time_format = "{:02d}:{:02d}".format(mins, secs)
			currenttimelabel['text'] = "Current time : "+ time_format
			time.sleep(1)
			current_time+=1


# Create the menubar
menubar = Menu(root)
root.config(menu=menubar)



# Create the submenu
submenu = Menu(menubar, tearoff=0)          # tearoff removes the dashed line at the top of the submenu
menubar.add_cascade(label="File", menu=submenu)
submenu.add_command(label="Open", command=browse_file)
submenu.add_command(label="Exit", command=root.destroy)


def about_us():
	tkinter.messagebox.showinfo('About WINK', 'This is a music player built using Python Tkinter by Aman Kushwaha.')



submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=submenu)
submenu.add_command(label="About us", command=about_us)

mixer.init()   # initializing the mixer


def play_music():
	global paused

	if paused:
		mixer.music.unpause()
		statusbar['text'] = "Playing... " + os.path.basename(filename_path)
		paused = False

	else:
		try:
			stop_music()
			time.sleep(1)
			selected_song = playlistbox.curselection()
			selected_song = int(selected_song[0])
			play_it = playlist[selected_song]
			mixer.music.load(play_it)
			mixer.music.play()
			statusbar['text'] = "Playing... " + os.path.basename(play_it)
			show_details(play_it)
		except:
			tkinter.messagebox.showerror('File not found!', 'WINK could not find the file. Please check again.')


paused=False
def pause_music():
	global paused
	paused = True
	mixer.music.pause()
	statusbar['text'] = "Music paused."

def stop_music():
	mixer.music.stop()
	statusbar['text'] = "Music stopped."



def rewind_music():
	global paused
	paused = False
	play_music()

def set_vol(val):
	volume = float(val)/100         # We divide the volume by 100 because the value only varies from 0-1
	mixer.music.set_volume(volume)

muted = False
def mute_music():
	global muted
	if muted:
		volumeButton.configure(image=volumePhoto)
		mixer.music.set_volume(0.7)
		scale.set(70)
		muted = False
	else:
		volumeButton.configure(image=mutePhoto)
		mixer.music.set_volume(0)
		scale.set(0)
		muted = True



# Creating Middle Frame for main play buttons

middleframe = Frame(rightframe)
middleframe.pack(pady=30, padx=30)

playPhoto = PhotoImage(file="Images/play.png")
playButton = ttk.Button(middleframe, image = playPhoto, command = play_music)
playButton.grid(row=0, column=0, padx=10)

stopPhoto = PhotoImage(file="Images/stop.png")
stopButton = ttk.Button(middleframe, image = stopPhoto, command = stop_music)
stopButton.grid(row=0, column=1, padx=10)

pausePhoto = PhotoImage(file="Images/pause.png")
pauseButton = ttk.Button(middleframe, image = pausePhoto, command = pause_music)
pauseButton.grid(row=0, column=2, padx=10)


# Creating Bottom Frame extra buttons

bottomframe = Frame(rightframe)
bottomframe.pack(pady=20)

rewindPhoto = PhotoImage(file="Images/rewind.png")
rewindButton = ttk.Button(bottomframe, image = rewindPhoto, command = rewind_music)
rewindButton.grid(row=0, column=0)

volumePhoto = PhotoImage(file="Images/volume.png")
mutePhoto = PhotoImage(file="Images/mute.png")
volumeButton = ttk.Button(bottomframe, image = volumePhoto, command = mute_music)
volumeButton.grid(row=0, column=1)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient = HORIZONTAL, command = set_vol)
scale.set(70)         # Set the scale to default = 70
mixer.music.set_volume(0.7)         # Set the volume to default = 70
scale.grid(row=0, column=2, pady=15, padx=30)


def on_closing():
	stop_music()
	root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)					# overriding close(X) buttton

root.mainloop()