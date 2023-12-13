#! python3
# mapIt.py - Launches a map in the browser using an address from the
# command line or clipboard.
import webbrowser
import sys
import pyperclip
import urllib.parse
if len(sys.argv) > 1:
 # Get address from command line.
 address = ' '.join(sys.argv[1:])
else:
 # Get address from clipboard.
 address = pyperclip.paste()

 encoded_address = urllib.parse.quote_plus(address)

webbrowser.open(f'https://www.google.com/maps/search/{encoded_address}')
