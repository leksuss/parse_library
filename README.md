# Book Downloader

This tool is for download books from [tululu.org](https://tululu.org) e-library. It also has the published version of website as result of using this tool located here:
https://leksuss.github.io/parse_library/website/pages/index1.html

## How to download and run local copy of this library

1. Get the source code of library: on this pag you can see green button named 'code'. After clicking on it you should select 'Download zip' item.

2. Unpack zip-archive and double click on file located at `parse_library-master/website/pages/index1.html`

3. Enjoy reading!

## How to install

### Requirements

 - python3.6+
 - `beautifulsoup4`
 - `requests`
 - `pathvalidate`
 - `lxml`
 - `jinja2`
 - `livereload`
 - `more-itertools`


### How to setup and run

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
Run simple webserver:
```
python3 render_website.py
```




## How to download more books from library

There are two scripts. Script named `downloader.py` can download books and covers by it's id range. Script named `parse_tululu_category.py` can download books from certain category (Fantastic section).

### downloader.py

Each book in tululu e-library identifies by id. Script accept two positional arguments: `start id` and `end id` to set a range books needs to be downloaded. By default script try to download books with ids from 1 to 10 (inclusively).
Books are downloaded to `books` folder, and book covers are downloaded to `images` folder, in the same place where script is located. 

Run script without arguments:
```
python3 downloader.py
```

Run script with arguments:
```
python3 downloader.py 20 30
```

### parse_tululu_category.py

This script also creates two folders (if required, and depend on arguments) for book texts (`books`) and book covers(`images`). But also it create a json file with all metadata of each book. 

It has parameters:
 - `--start_page` - an id page from which you need to start parse books. Default is 1.
 - `--end_page` - to which page id you need to parse books (not inclusively). if not set, script will download all pages till the end
 - `--dest_folder` - path to save parsed books, where is `books`, `images` folders and json file `books.json` will be located. Default is current directory.
 - `--skip_imgs` - flag to skip downloading book covers. Default is `False`, i.e. not skip
 - `--skip_txt` - flat to skip downloading book texts. Default is `False`, i.e. not skip
 - `--json_path` - custom path to json file with books metadata. Overwrites `--dest_folder` param for json file if set.

Here is some examples:
```
python3 parse_tululu_category.py --start_page 301 --end_page 303 --dest_folder ~/fantastic_books
python3 parse_tululu_category.py --start_page 700 --dest_folder ~/fantastic_books --json_path ~/fantastic_books/json_folder/data.json --skip_imgs
python3 parse_tululu_category.py --end_page 4 --skip_imgs --skip_txt --json_path ~/path/to/json/folder/books.json
```

## Goals
This project is made for study purpose.