# One

import tkinter as tk
from tkinter import ttk
from ReaderWindow import ReaderWindow


def main():
	root = tk.Tk();
	root.geometry = ('500x650') 
	root.resizable(0, 0)
	root.pack_propagate(0)
	
	app = ReaderWindow(root);

	root.mainloop();

if( __name__ == "__main__"):
	main();