# Remember The Milk status monitor for Adafruit LCD backpack

## What it does

- Uses RTM API to get a count of tasks according to urgency and importance.
- Displays task count on LCD backpack
- Changes LCD's backlight to reflect task status

## Dependancies

You need:
- Python 2.7ish
- PIP
- The RtmAPI from https://bitbucket.org/rtmapi/rtmapi/overview or type ```pip install rtmapi```
- The LCD backpack library from https://github.com/dinofizz/adafruit-usb-serial-lcd-backpack or type ```pip install lcdbackpack```
- A RTM API key and shared secret, from https://www.rememberthemilk.com/services/api/

## Installation

1. Install the dependancies and get an API key.
2. Clone this repo.
3. Copy **rtmcreds.py.template** to **rtmcreds.py** and put the API key and secret in indicated.
4. Chmod the rtmstatus.py to 700 and rtmcreds.py to 600.
4. Run the script without arguments (see Invocation section), sign in to RTM in the web browser that opens, and put the token in rtmcreds.py.
5. Customise the filter strings as desired.
6. Connect the LCD backpack to your computer's USB port.

## Invocation

- ```./rtmstatus.py``` runs the script.  Press CTRL-C to exit.
- ```./rtmstatus.py debug``` runs the script with stuff sent to stdout.  Useful if you don't have a LCD backpack (yet) and want to check your filters.

## Future work

See issues page.
