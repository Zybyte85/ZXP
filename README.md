# ZXP
Z-Explorer. The quickest file explorer you will use.
## Usage
After you install it, just run `zxp` and it will open up. After that, you just type in the directories that you want to go to.

### Commands
- `:quit, :q`  quits out of the program
- `:back, :b`  goes back a directory

## Installation
You can download the binary from the releases and put it in a PATH folder (such as ~/.local/bin/) or you can run this command to automatically do that for you
```
wget https://github.com/Zybyte85/ZXP/releases/latest/download/zxp -P ~/.local/bin && chmod +x ~/.local/bin/zxp
```
## Planned Features
- [ ] Add copy/cut/paste
- [ ] Make a config thing
- [ ] Add go back to previous directory
- [ ] Add details about the file next to it

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
