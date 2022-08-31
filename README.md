# MTG Proxy sheet maker
Script to makes array of images for printing Magic the Gathering proxies and tokens

## Requirements
- Python 3.9

## Usage
- Create and enable virtual env
  ```bash
  python3 -m venv venv
  source bin/venv/activate
  ```
- Install dependencies
  ```
  pip install -r requirements.txt
  ```
- Put images you want to print into the folder. Let's say it at `path/to/folder`
- Run `python make_list path/to/folder`. It will generate `settings.json` at that folder
- Edit `settings.json` to adjust amount of times each specific file gets printed by changing `"quantity"` in file objects
- Run `python make_sheet path/to/folder`. Results can be found at `path/to/folder/output`
