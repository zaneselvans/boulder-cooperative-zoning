# Install Notes

pip install cython pandas xlrd lxml openpyxl

If you get an error when writing the file that says:
```
 UserWarning: The installed version of lxml is too old to be used with openpyxl
```

Then you'll have to run `pip install lxml --upgrade`

If *that* gives you an error:
```
Could not find function xmlCheckVersion in library libxml2. Is libxml2
installed?

Perhaps try: xcode-select --install
```

You'll have to run:
```
brew install libxml2
brew install libxslt
brew link libxml2 --force
brew link libxslt --force
```

Then run `pip install lxml --upgrade` again. Then you should be abl
