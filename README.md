# Book Downloader

This tool is for download books from [tululu.org](https://tululu.org) e-library.

## Requirements

 - python3.6+
 - `beautifulsoup4`
 - `requests`
 - `pathvalidate`
 - `lxml`


## How to install

Get the source code of this repo:
```
git clone https://github.com/leksuss/parse_library.git
```

Go to this script:
```
cd parse_library
```

Python3 should be already installed. Then use pip (or pip3, if there is a conflict with Python2) to install dependencies:
```
# If you would like to install dependencies inside virtual environment, you should create it first.
pip3 install -r requirements.txt
```

## How to use

Each book in tululu e-library identifies by id. Script accept two positional arguments: `start id` and `end id` to set a range books needs to be downloaded. By default script try to download books with ids from 1 to 10 (inclusively).

Run script without arguments:
```
python3 main.py
```

Run script with arguments:
```
python3 main.py 20 30
```
