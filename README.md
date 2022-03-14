# Passport appointment finder

I was too lazy waking up early on Monday to find a passport appointment. So I created a bot to do it for me.
This project has not matiruity at all and is not aimed at evolving much.

# Requirements

- [poetry](https://python-poetry.org/) to install packages 
- python >=3.7
- maybe a Mac as the notification system depends on `osascript` but you can disable this part

# Usage

## Install

Make sure poetry uses the right python version with:
```bash
poetry env use <path_to_your_python>
```

Install python packages with:
```bash
poetry install
```

## Launch

```bash
python search_appointments.py
```

If you're not on Mac, you might have issues because the script depends on `osascript`. Thus, you can disable notification by running:

```bash
python search_appointments.py --disable-notification
```
