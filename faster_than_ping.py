# -*- coding: utf-8 -*-
import argparse
import os
import socket
import sys
import time
import platform
import re
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import datetime as dt
import tkinter as tk
import tkinter.ttk as ttk
from enum import Enum
from typing import Optional


class System(Enum):
	LINUX = 0,
	MAC = 1,
	WINDOWS = 2


def get_system() -> Optional[System]:
	name = platform.system().lower()
	if name == "linux" or name.endswith("nux"):
		return System.LINUX
	elif name == "windows" or name.startswith("win"):
		return System.WINDOWS
	elif name == "Darwin":
		return System.MAC
	else:
		return None


def is_compatible_system(system: System = None) -> bool:
	if system is None:
		system = get_system()
	
	return system is None


def assess_compatible_system(system: System = None) -> bool:
	if not is_compatible_system(system):
		raise EnvironmentError("Your OS '{}/{}' is not supported by this script.".format(platform.system(), os.name))
	return True


def ping(url: str, timeout_s: int = 2, port: int = 80) -> float:
	"""
	Send a ping to the given URL and measure the time between sending and receiving.
	:param url: The url where the ping must be send to.
	:type url: str
	:param timeout_s: Timeout in second for the connection. Default value is 2s.
	:type timeout_s: int
	:param port: Server port number
	:type port: int
	:return: Return the time of the ping in millis
	:rtype: float
	"""
	url = re.sub(r'^[a-zA-Z]+://', '', url)
	url = url.split('/')[0]
	
	host = socket.gethostbyname(url)
	start = dt.datetime.now()
	s = socket.create_connection((host, port), timeout_s)
	end = dt.datetime.now()
	s.close()
	return (end - start).total_seconds() * 1000


def main(args: dict = None):
	if args is None:
		args = {}
	
	pings = []
	
	root = tk.Tk()
	root.configure(background='white')
	root.wm_title("Faster Than Ping")
	
	style = ttk.Style()
	style.configure("My.TFrame", background="white")
	style.configure("My.TLabel", background="white")
	style.configure("Title.TLabel", background="white", anchor="center", foreground="#3d8491")
	style.configure("My.TEntry", background="white")
	style.configure("My.TButton", background="white")
	
	mainframe = ttk.Frame(master=root, style="My.TFrame")
	mainframe.pack(side=tk.TOP)
	#mainframe.configure(background="white")
	
	lb_title = ttk.Label(master=mainframe, font=("arial", 20, "bold"), text="Faster Than Ping", style="Title.TLabel")
	#lb_title.configure(background="white")
	lb_title.pack(side=tk.TOP, fill=tk.X)
	
	url_frame = ttk.Frame(master=mainframe, style="My.TFrame")
	#url_frame.configure(background="white")
	url_frame.pack(side=tk.TOP)
	
	lb_url = ttk.Label(master=url_frame, text="URL: ", style="My.TLabel")
	#lb_url.configure(background="white")
	lb_url.pack(side=tk.LEFT)
	
	et_url = ttk.Entry(master=url_frame, style="My.TEntry")
	#et_url.configure(background="white")
	et_url.pack(side=tk.LEFT)
	
	def bt_ok_callback():
		if et_url.get() is not None and len(et_url.get()) > 0:
			args["url"] = et_url.get()
	
	bt_ok = ttk.Button(master=url_frame, text="Ok", command=bt_ok_callback, style="My.TButton")
	#bt_ok.configure(background="white")
	bt_ok.pack(side=tk.LEFT)
	
	lb_min_max = ttk.Label(master=mainframe, text="", style="My.TLabel")
	#lb_min_max.configure(background="white")
	lb_min_max.pack(side=tk.BOTTOM, fill=tk.X)
	
	plt.style.use('seaborn')
	matplotlib.rcParams['toolbar'] = 'None'
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	
	def refresh(_):
		url = args.get("url", "www.google.com")
		p = ping(url)
		pings.append(p)
		
		x = range(len(pings))
		y = list(pings)
		if len(pings) > 10:
			x = x[-10:]
			y = y[-10:]

		message = "[{0}]: {1:.2f} ms".format(url, p)
		print(message)
		
		ax.clear()
		ax.set_xlabel("Pings")
		ax.set_ylabel("Time (ms)")
		ax.set_title(message)
		ax.xaxis.set_ticks(range(min(x), max(x)+1))
		ax.plot(x, y, color="#64dfe5", linestyle="solid", marker='o', label="Ping")
		ax.set_ylim(ymin=0)
		if len(y) > 0:
			ax.set_ylim(ymax=max(y) + 10)
		ax.legend()
		min_max = "min = {0:4.2f} ms\tmax = {1:4.2f} ms".format(min(pings), max(pings))
		lb_min_max["text"] = min_max
	
	canvas = FigureCanvasTkAgg(fig, master=mainframe)
	canvas.show()
	canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.X)

	# noinspection PyUnusedLocal
	ani = animation.FuncAnimation(fig, refresh, interval=1000, blit=False)
	plt.legend()
	
	def on_close():
		root.destroy()
		sys.exit(0)
	
	root.protocol("WM_DELETE_WINDOW", on_close)
	root.mainloop()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--url", help="URL or hostname of the connection. Default is www.google.com",
						type=str, default="www.google.com")
	parser.add_argument("-d", "--debug", help="Print debug information in the console",
						action="store_true")
	args = parser.parse_args()
	main(args.__dict__)
