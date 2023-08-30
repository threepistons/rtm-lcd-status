# Remember The Milk status monitor for Adafruit LCD backpack

## What it does

- Uses RTM API to get a count of tasks according to urgency and importance.
- Displays task count on LCD backpack
- Changes LCD's backlight to reflect task status

## Dependancies

You need:
- Python 3
- Pip3
- A RTM API key and shared secret, from https://www.rememberthemilk.com/services/api/

## Installation

1. Clone this repo and enter the directory made by Git.
2. Install the dependancies `pip3 install -r requirements.txt`.  If you get an error about "error: externally-managed-environment" then refer to the section "Installation and invocation with venv".
3. Copy **rtmstatus.conf.template** to **rtmstatus.conf** and put the API key and secret in indicated.
4. Chmod rtmstatus.conf to 600.
4. Run the script without arguments (see Invocation section), sign in to RTM in the web browser that opens, and put the token in rtmstatus.conf.
5. Customise the filter strings as desired.
6. Connect the LCD backpack to your computer's USB port.

## Invocation

- ```./rtmstatus.py``` runs the script.  Press CTRL-C to exit.
- ```./rtmstatus.py debug``` runs the script with stuff sent to stdout.  Useful if you don't have a LCD backpack (yet) and want to check your filters.

## Installation and invocation with venv

To install the dependancies in "Installation" step 2, be in the directory made by Git and run `python3 -m venv .`, then `bin/pip3 install -r requirements.txt`.

To run the script, instead of `./rtmstatus.py`, you must now say `bin/python3 rtmstatus.py`.

## Future work

See issues page.
