# -*- coding: utf-8 -*-
import argparse
import os
import socket
import sys
import time
import platform
import re
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime as dt
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
	
	plt.style.use('seaborn')
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	fig.suptitle("Faster Than Ping")
	
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
		ax.plot(x, y, color="#64dfe5", linestyle="solid", marker='o', label="Ping")
		ax.set_ylim(ymin=0)
		if len(y) > 0:
			ax.set_ylim(ymax=max(y) + 10)
		ax.legend()
		ax.text(1, 1, "min = {0:4.2f} ms\nmax = {1:4.2f} ms".format(min(pings), max(pings)), transform=plt.gcf().transFigure)
	
	ani = animation.FuncAnimation(fig, refresh, interval=1000)
	plt.legend()
	plt.show()
	pass


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--url", help="URL or hostname of the connection. Default is www.google.com",
						type=str, default="www.google.com")
	parser.add_argument("-d", "--debug", help="Print debug information in the console",
						action="store_true")
	args = parser.parse_args()
	main(args.__dict__)
