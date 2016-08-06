Adds a few extra features to [pytoutv](https://github.com/bvanheu/pytoutv):

- fetch
  - Retry on timeout
  - Fetch episodes in order
  - Only fetch undownloaded episodes
  - Less verbose file naming

- list
  - Retry on timeout
  - Only show new emissions
  - Show more information (URL, genre, country)

**Installation**

```
 git clone https://github.com/bvanheu/pytoutv.git
 cd pytoutv
 sudo python3 setup.py install
 cd ..
 git clone https://github.com/bmaupin/junkpile.git
 cd junkpile/python/video-tools/pytoutv-plus/
 sudo python3 setup.py install
```
