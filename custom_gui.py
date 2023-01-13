from tkinter import *
from tkinter import ttk
import pandas as pd
import os
import customtkinter as ctk
from tkinter import filedialog
from tkinter import filedialog
from tensorflow.keras.models import load_model
import pandas as pd
from scipy.io import wavfile
import librosa
from predict import make_prediction
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


root = ctk.CTk()
root.title('kick-manager')
root.geometry('800x430')

# Creating a list of sizes
classes = [
	"Hip Hop",
	"House",
	"Pop",
	"Techno",
	"Trap",
	"Tropical House"
]

# Create a list of colors
hip_hop=[]
house=[]
pop=[]
techno=[]
trap=[]
tropical_house=[]


my_dir=''
def my_fun():
	my_dir=filedialog.askdirectory()
	l3.configure(text=my_dir)
	make_prediction(my_dir)
	classes_list(classes, my_dir)

def sort_wavs(f, sort_dir, dir_path):
	sort_file = os.path.join(sort_dir, f)
	my_file = os.path.join(dir_path, f)
	wav, rate = librosa.load(my_file)
	if os.path.exists(sort_file):
		return
	wavfile.write(sort_file, rate=rate, data=wav)

def check_dir(path):
    if os.path.exists(path) is False:
        os.mkdir(path)

def classes_list(classes, my_dir):
	result = pd.read_csv('predictions.csv')
	#sort_root = my_dir.split('.')[0]+'_sorted'
	my_dir_parent = os.path.dirname(my_dir)
	sort_root = os.path.join(my_dir_parent, 'KICK-MANAGER')
	check_dir(sort_root)
	for c in classes:
		sort_dir = os.path.join(sort_root, c)
		check_dir(sort_dir)
		wav_file = result[result.genre == c].iloc[:,3]
		for f in wav_file:
			dir_path = result[result.samples == f].iloc[0,4]
			if c == 'Hip Hop':
				hip_hop.append(f)
			if c == 'House':
				house.append(f)
			if c == 'Pop':
				pop.append(f)
			if c == 'Techno':
				techno.append(f)
			if c == 'Trap':
				trap.append(f)
			if c == 'Tropical House':
				tropical_house.append(f)
			sort_wavs(f, sort_dir, dir_path)

# Frame
my_frame = ctk.CTkFrame(root, corner_radius=10)
my_frame.pack(pady=10)


#ttk style
#s = ttk.Style()
#s.configure('b1', font=("Lucida Console",14), height=10, width=10)
# Adding directories

b1 = ctk.CTkButton(my_frame,
width=25,
height=30,
corner_radius=5,
 text='Select directory',
 font=("Lucida Console",12,"bold"),
command=lambda:my_fun())
b1.grid(row=0, column=0, pady=5)

l3_frame = ctk.CTkFrame(my_frame, corner_radius=5)
l3_frame.grid(row=0, column=1, pady=5, padx=5)
l3 = ctk.CTkLabel(l3_frame, text=my_dir, font=("Lucida Console",12, 'bold'), corner_radius=5, width=20, fg_color='#292929', text_color='white')
l3.pack()
# List boxes

list1_frame = ctk.CTkFrame(my_frame, corner_radius=10)
list1_frame.grid(row=2, column=0, pady=5, padx=10)


l1 = ctk.CTkLabel(list1_frame, text="Genres", width=20, font=("Lucida Console",13,"bold"),corner_radius=5, text_color='white')
l1.pack(padx=5, pady=5)

my_list1 = Listbox(list1_frame, 
font=("Lucida Console",14),
height=17,
width=20,
bd=0,
bg='#292929',
fg='white')
my_list1.pack(pady=3, padx=10)
#my_list1.pack(row=2, column=0, pady=5)


list2_frame = ctk.CTkFrame(my_frame, corner_radius=10)
list2_frame.grid(row=2, column=1, pady=5, padx=10)


l2 = ctk.CTkLabel(list2_frame, text="Samples", width=55,font=("Lucida Console",13,"bold"),corner_radius=8, text_color='white')
l2.pack(padx=5, pady=5)

my_list2 = Listbox(list2_frame, 
font=("Lucida Console",14),
height=17,
width=55,
bd=0,
bg='#292929',
fg='white')
my_list2.pack(pady=3, padx=10)




def list_color(e):
	my_list2.delete(0, END)
	if my_list1.get(ANCHOR) == "Hip Hop":
		for item in hip_hop:
			my_list2.insert(END, item)
	if my_list1.get(ANCHOR) == "House":
		for item in house:
			my_list2.insert(END, item)
	if my_list1.get(ANCHOR) == "Pop":
		for item in pop:
			my_list2.insert(END, item)
	if my_list1.get(ANCHOR) == "Techno":
		for item in techno:
			my_list2.insert(END, item)
	if my_list1.get(ANCHOR) == "Trap":
		for item in trap:
			my_list2.insert(END, item)
	if my_list1.get(ANCHOR) == "Tropical House":
		for item in tropical_house:
			my_list2.insert(END, item)

# add items to list1
for item in classes:
	my_list1.insert(END, item)

# Bind The Listbox
my_list1.bind("<<ListboxSelect>>", list_color)

root.mainloop()