# Lackey v0.4.0a1 #
## A Graphical Python Automation Suite ##
[![Documentation Status](https://readthedocs.org/projects/lackey/badge/?version=latest)](http://lackey.readthedocs.io/en/latest/?badge=latest) [![Build status](https://ci.appveyor.com/api/projects/status/l1q68dnp6vm8sre9?svg=true)](https://ci.appveyor.com/project/glitchassassin/lackey)

Developed by [Jon Winsley](https://github.com/glitchassassin)

## Third Party Library Requirements ##

* numpy
* pillow
* opencv (included)

## Introduction ##

Lackey is a Python implementation of Sikuli script, allowing you to run automation scripts developed in the Sikuli editor with pure Python. If you're trying to run Sikuli scripts in a Java-free environment or integrate them into an existing Python testing structure, this is the library for you.

## Usage ##

### Installation ##

Installation is easy:

    pip install Lackey

Then you can just import Lackey at the head of your Sikuli-script python file:
    
    from lackey import *

**WARNING** Be aware that this will create global methods that will *overwrite certain Python functions*, such as `type()`. For more information, see the **Sikuli Patching** section below.

### General ###

The Lackey library is divided up into classes for finding and interacting with particular regions of the screen. Patterns are provided as bitmap files (supported formats include `.bmp`, `.pbm`, `.ras`, `.jpg`, `.tiff`, and `.png`). These patterns are compared to a Region of the screen, and, if they exist, can target a mouse move/click action.

If you've used Sikuli, you'll feel right at home. Lackey is designed to be a drop-in shim for Sikuli.

Sample code:

    from lackey import *

    click("Start_Button.png")
    wait("Control_Panel.png", 5) # Maybe the Start menu is slow
    click("Notepad.png")

## Documentation ##

Full API documentation can be found at [ReadTheDocs](http://lackey.readthedocs.io/en/latest/).

## Rationale ##

In my line of work, I have a lot of tasks walking through line-of-business applications to do boring things that any computer could do. Laziness being the mother of invention, I decided to script what I could. I found [SikuliX](http://sikulix.com/) to be a tremendously valuable tool for the job, but its Java dependencies and limited Python coupling posed problems in several cases. So, I decided to implement my own graphical automation library in pure Python.

There are some existing libraries for this purpose, like `pywinauto` and `autopy`, but they didn't work for me for one reason or another. I wasn't doing a lot of Windows GUI interaction with these particular applications, so `pywinauto`'s approach wouldn't help. I needed something that could search for and use images on screen. `autopy` was closer, but it had quite a few outstanding issues and hadn't been updated in a while.

Most of my automation is in Windows, so I've begun this library with only Windows support. However, it's designed to eventually be extended with support for Mac OS X and Linux by implementing additional "PlatformManager" classes. I'll get around to these at some point, but if you'd like to contribute one sooner, please feel free!

### Sikuli Patching ###

My goal with this project is to be able to reuse my existing library of Sikuli scripts with minimal modifications. To that end, Lackey will map certain functions of the screen region (`find()`, `click()`, etc.) to the global scope. This means you can use the Sikuli IDE for development, and run the final product with pure Python! Add the following line to your Sikuli python script, and you should be able to run it in Python largely without issue:

    from lackey import *

Note that I *have* had to adjust some of my image search similarity settings in a couple cases. Your mileage may vary. Please report any issues that you encounter and I'll try to get them patched.

Be aware that **some Sikuli-script methods actually overwrite Python-native functions**, namely `type()` and `input()`. Where this is the case, I've remapped the native functions by prefixing them with an underscore. They can be accessed as follows:

    from lackey import *

    username = _input("Enter your username: ")

## Structure ##

Each platform (Windows/OSX/Linux) needs its own PlatformManager (see documentation above) to abstract OS-level functionality, like simulating mouse clicks or key presses. Ideally, these should be implemented with as few 3rd-party library dependencies as possible. If you'd like to contribute a PlatformManager for your OS, feel free to submit a pull request! 

Don't forget to update the unit tests and verify that they still run.

## Fair Warning ##

This library is currently under development, and is missing many features needed for full Sikuli compatibility (and may have serious bugs). Fork at your own risk!

## Build Instructions ##

To build the wheel from source, run:

    python setup.py bdist_wheel

(Note that you may need to make sure `wheel` is installed)