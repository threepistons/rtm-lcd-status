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

1. Install the dependancies `pip3 -r requirements.txt` and get an API key.
2. Clone this repo.
3. Copy **rtmstatus.conf.template** to **rtmstatus.conf** and put the API key and secret in indicated.
4. Chmod rtmstatus.conf to 600.
4. Run the script without arguments (see Invocation section), sign in to RTM in the web browser that opens, and put the token in rtmstatus.conf.
5. Customise the filter strings as desired.
6. Connect the LCD backpack to your computer's USB port.

## Invocation

- ```./rtmstatus.py``` runs the script.  Press CTRL-C to exit.
- ```./rtmstatus.py debug``` runs the script with stuff sent to stdout.  Useful if you don't have a LCD backpack (yet) and want to check your filters.

## Future work

See issues page.
