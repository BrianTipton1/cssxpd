Quick script to expand css files into one huge css file

> Running with python
```python
python main.py -u https://myurl.com/something.css
```
> Help Menu
```bash
usage: cssxpd [-h] [-u URL] [-o OUT_FILE] [-s] [-nw]

Will search through a CSS file and recursively download additional CSS imports and write to one file

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL
  -o OUT_FILE, --out-file OUT_FILE
  -s, --stdout
  -nw, --no-write
```

> Running with Nix Flake
```bash
nix run github:BrianTipton1/cssxpd#cssxpd
```