from zipfile import ZipFile
import Tkinter as tk
import tkFileDialog
import tkMessageBox
import platform
import requests
import time
import os

## Lackey sub-files

from .PlatformManagerWindows import PlatformManagerWindows
from .KeyCodes import Button, Key, KeyModifier
from .RegionMatching import Pattern, Region, Match, Screen, Location, Mouse, Keyboard, App
from .Exceptions import FindFailed
from .Settings import Debug, Settings
import SikuliGui

VALID_PLATFORMS = ["Windows"]

## Sikuli patching: Functions that map to the global Screen region
## Don't try this at home, kids!

# First, save the native functions by remapping them with a prefixed underscore:

_type = type
_input = input
#_zip = zip

## Sikuli Convenience Functions

def sleep(seconds):
	""" Convenience function. Pauses script for `seconds`. """
	time.sleep(seconds)

def exit(value):
	""" Convenience function. Exits with code `value`. """
	sys.exit(value)

def setShowActions(value):
	""" Convenience function. Sets "show actions" setting (True or False) """
	Settings.ShowActions = bool(value)

def getBundlePath():
	""" Convenience function. Returns the path of the \*.sikuli bundle. """
	return Settings.BundlePath
def getBundleFolder():
	""" Convenience function. Same as `getBundlePath()` plus the OS default path separator. """
	return getBundlePath() + os.path.sep
def setBundlePath(path):
	""" Convenience function. Changes the path of the \*.sikuli bundle. """
	if os.path.exists(path):
		Settings.BundlePath = path
	else:
		raise FileNotFoundError(path)
def getImagePath():
	""" Convenience function. Returns a list of paths to search for images. """
	return [getBundlePath()] + Settings.ImagePaths
def addImagePath(new_path):
	""" Convenience function. Adds a path to the list of paths to search for images. Can be a URL (but must be accessible). """
	if os.path.exists(new_path):
		Settings.ImagePaths.append(new_path)
	elif "http://" in new_path or "https://" in new_path:
		request = requests.get(new_path)
		if request.status_code < 400:
			# Path exists
			Settings.ImagePaths.append(new_path)
		else:
			raise FileNotFoundError("Unable to connect to", new_path)
	else:
		raise FileNotFoundError(new_path)
def addHTTPImagePath(new_path):
	""" Convenience function. Same as `addImagePath()`. """
	addImagePath(new_path)

def getParentPath():
	""" Convenience function. Returns the parent folder of the \*.sikuli bundle. """
	return os.path.dirname(Settings.BundlePath)
def getParentFolder():
	""" Convenience function. Same as `getParentPath()` plus the OS default path separator. """
	return getParentPath() + os.path.sep
def makePath(*args):
	""" Convenience function. Returns a path from a series of path components. Same as `os.path.join`. """
	return os.path.join(*args)
def makeFolder(*args):
	""" Convenience function. Same as `makePath()` plus the OS default path separator. """
	return makePath(*args) + os.path.sep

## Sikuli implements the unzip() file, below. Included here to avoid breaking old
## scripts. ``zipfile()`` is coded here, but not included in Sikuli, so I've
## commented it out for the time being. Note that ``zip`` is a reserved keyword
## in Python.

def unzip(fromFile, toFolder):
	""" Convenience function. Extracts files from the zip file `fromFile` into the folder `toFolder`. """
	with ZipFile(os.path.abspath(fromFile), 'r') as to_unzip:
		to_unzip.extractall(os.path.abspath(toFolder))
#def zipfile(fromFolder, toFile):
#	with ZipFile(toFile, 'w') as to_zip:
#		for root, dirs, files in os.walk(fromFolder):
#			for file in files:
#				to_zip.write(os.path.join(root, file))


## Popup/input dialogs

def popat(*args):
	""" Convenience function. Sets the popup location (currently not used). """
	if len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int):
		# popat(x,y)
		Settings.PopupLocation = Location(args[0],args[1])
	elif len(args) == 1 and isinstance(args[0], Location):
		# popat(location)
		Settings.PopupLocation = args[0]
	elif len(args) == 1 and isinstance(args[0], Region):
		Settings.PopupLocation = args[0].getCenter()
	elif len(args) == 0:
		Settings.PopupLocation = SCREEN.getCenter()
	else:
		raise TypeError("Unrecognized parameter(s) for popat")

def popup(text, title="Lackey Info"):
	""" Creates an info dialog with the specified text. """
	root = tk.Tk()
	root.withdraw()
	tkMessageBox.showinfo(title, text)
def popError(text, title="Lackey Error"):
	""" Creates an error dialog with the specified text. """
	root = tk.Tk()
	root.withdraw()
	tkMessageBox.showerror(title, text)
def popAsk(text, title="Lackey Decision"):
	""" Creates a yes-no dialog with the specified text. """
	root = tk.Tk()
	root.withdraw()
	return tkMessageBox.askyesno(title, text)

# Be aware this overwrites the Python input() command-line function.
def input(msg="", default="", title="Lackey Input", hidden=False):
	""" Creates an input dialog with the specified message and default text. If `hidden`, creates a password dialog instead. Returns the entered value. """
	root = tk.Tk()
	input_text = tk.StringVar()
	input_text.set(default)
	dialog = SikuliGui.PopupInput(root, msg, default, title, hidden, input_text)
	root.focus_force()
	root.mainloop()
	return str(input_text.get())
def inputText(message="", title="Lackey Input", lines=9, width=20, text=""):
	""" Creates a textarea dialog with the specified message and default text. Returns the entered value. """
	root = tk.Tk()
	input_text = tk.StringVar()
	input_text.set(text)
	dialog = SikuliGui.PopupTextarea(root, message, title, lines, width, text, input_text)
	root.focus_force()
	root.mainloop()
	return str(input_text.get())
def select(message="", title="Lackey Input", options=[], default=None):
	""" Creates a dropdown selection dialog with the specified message and options. `default` must be one of the options. Returns the selected value. """
	if len(options) == 0:
		return ""
	if default is None:
		default = options[0]
	if default not in options:
		raise ValueError("<<default>> not in options[]")
	root = tk.Tk()
	input_text = tk.StringVar()
	input_text.set(text)
	dialog = SikuliGui.PopupList(root, message, title, options, default, input_text)
	root.focus_force()
	root.mainloop()
	return str(input_text.get())
def popFile(title="Lackey Open File"):
	""" Creates a file selection dialog with the specified message and options. Returns the selected file. """
	root = tk.Tk()
	root.withdraw()
	return str(tkFileDialog.askopenfilename())

# If this is a valid platform, set up initial Screen object. Otherwise, might be ReadTheDocs
if platform.system() in VALID_PLATFORMS:
	SCREEN = Screen(0)
	for prop in dir(SCREEN):
		if callable(getattr(SCREEN, prop, None)) and prop[0] != "_":
			# Property is a method, and is not private. Dump it into the global namespace.
			globals()[prop] = getattr(SCREEN, prop, None)
			