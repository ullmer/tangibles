Within PyGame Zero, the alpha="opacity" features of Actors (including animation) 
depends upon version 1.3.  This is not present in pypi, and can be a bit curious to build.
The specific build sequence that's worked for me:

git clone
python3 setup.py build
python3 setup.py install (as root)
python3 -m pip install --editable .
# the latter, per https://pygame-zero.readthedocs.io/en/latest/contributing.html

