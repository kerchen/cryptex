# cryptex
A dedicated hardware device for securely storing passwords.

# Background
In Dan Brown's _The Da Vinci Code_, a _cryptex_ is a physical device used to
store a scroll or piece of paper (which has a secret written on it). The
cryptex's contents can only be accessed by someone who knows the combination to
unlock it. Furthermore, it has some protections against brute-force attempts to
bypass the combination. 

This project is similar to Brown's cryptex in that it is also a physical device
whose contents are protected by a passcode, but the contents are purely digital
(passwords, usernames, URLs, etc). At its simplest, it works like this:
when one connects the cryptex to the USB port of a computer, the cryptex 
enumerates as a standard USB keyboard, and, using the user interface on the
cryptex itself, one selects which data the cryptex should send. To the
connected computer, the data sent by the cryptex is the same as if someone
had typed it from a keyboard.

Of course, there are plenty of perfectly good, existing solutions to the
problem of securely storing passwords, but I wanted to make one tailored to my
needs and uses, specifically, one that meets all of these criteria:
* Private data is stored on a dedicated hardware device, not on the computer
that uses it nor on a third-party server. When the device is not in use, it is
physically impossible to access the data on it.
* The device can only be powered by USB. No extra power adapters, etc.
* Private data is cryptographically secure yet easily used and updated.
* Nothing needs to be installed on the computer that the cryptex is connected
to--no drivers, no apps. All of the needed software is on the cryptex itself.
* Can be made from inexpensive off-the-shelf parts and open-source software.
* Has to work with Microsoft Windows.
* Uses technologies that I want to learn more about. 

# Components
## Hardware
* Raspberry Pi zero
* Adafruit 2.2" TFT (non-touch) display with four tactile buttons
* A rotary encoder

## Software
* Adafruit Raspian Linux distro with extensions to support the TFT display
* Python 2.7
* bottle (Python web framework)

# Basic Operation
Upon plugging the cryptex into a computer, it boots and presents itself as an
RNDIS network adapter. To start using the cryptex, one needs to open a web
browser and navigate to 'http://cryptex.local/login'. Once logged in, the user
can use the web interface to manage existing passwords, etc. or the cryptex can
be put into 'keyboard' mode. In keyboard mode, all interactions with the
cryptex are made through the dedicated display and input hardware.

# Open Questions/Issues
As of this writing (26 Nov 2017), the project is in its infancy, with lots of
unanswered questions. I'm also still experimenting with different 
hardware and software, so there are plenty of things that still need to be
figured out. See the Issues section of this repo.

