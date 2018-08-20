# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup, find_packages

packages = find_packages(exclude=["contrib", "docs", "tests*"])
print(packages)

setup(
	name="Faster Than Light",
	version="1.0",
	description="Display dynamically the ping.",
	long_description="Faster Than Light is a python script that display dynamically the ping between your computer and"
	                 "a chosen server with TKinter and matplotlib.",
	author="Valentin Berger",
	url="https://github.com/Cynnexis/FasterThanLight",
	license="GNU Affero General Public License v3",
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Environment :: Other Environment",
		"Intended Audience :: End Users/Desktop",
		"License :: OSI Approved :: GNU Affero General Public License v3",
		"Natural Language :: English",
		"Programming Language :: Python",
		"Topic :: Internet"
	],
	keywords="ping internet game url hostname",
	packages=packages,
	scripts=["faster_than_ping.py"],
	project_urls={
		"Source Code": "https://github.com/Cynnexis/FasterThanLight"
	},
	install_requires=["matplotlib==2.1.1", "tk"]
	#data_files=None,
	#entry_points=None
)
