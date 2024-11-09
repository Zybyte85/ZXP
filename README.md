<div>
  <img src="zxp.svg" alt="Zxp logo" width="20%">
</div>

# ZXP
Z-Explorer. The quickest file explorer you will use.

Features:
- Tiny binary size (About 7.7 MB)
- Fast and efficient
- Easy to use
- Quick to navigate
- Uses only about 13 MB of memory

## Usage
After you install it, just run `zxp` and it will open up. After that, you just type in the directories that you want to go to.

### File operations
- `path/to/source :delete, :d, :remove, :rm` deletes source file/directory
- `path/to/source :rename, :r new_name` renames source file/directory
- `path/to/source :move, :m path/to/destiation` moves a file/directory

### Commands
- `:quit, :q`  quits out of the program
- `:back, :b`  goes back a directory
- `:hidden, :h` toggles hidden files
- `$ <command>` runs whatever command you specify

## Installation
You can download the binary from the releases and put it in a PATH folder (such as ~/.local/bin/) or you can run this command to automatically do that for you
```
wget https://github.com/Zybyte85/ZXP/releases/latest/download/zxp -O ~/.local/bin/zxp && chmod +x ~/.local/bin/zxp
```
## Planned Features
- [ ] Add copy/cut/paste
- [ ] Make a config thing
- [ ] Add go back to previous directory
- [ ] Add details about the file next to it
- [x] Add opening files
- [x] Add terminal command capability

## How YOU can help
- If you know Python, look at the issues or the planned features above and try to get them to work!
- If you don't know how to code, click on the "emojis.json" file and you can add different emojis for file types
- Request a feature on the "Issues page"
- Or, you can just use it! It would make me very happy and you can find bugs and report them here. :]

## Building
On Linux:
```
pyinstaller --onefile --add-data "emojis.json:." zxp.py
```
On Windows (not tested):
```
pyinstaller --onefile --add-data "emojis.json;." zxp.py
```
(yes there is a difference in the ":" vs ";")
