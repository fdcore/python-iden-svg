Identicon for Python
=====================

<img src="https://github.com/fdcore/python-iden-svg/raw/master/demo.svg" width="200" />

This is a Python library which generates identicons based on a given string.

Inspired by <https://github.com/bitverseio/identicon>

How to use
-----------
```python
  from iden import Iden
  i = Iden('hello world') # (text, type_iden='pixel', size=None)
  i.setBackgroundColor('#EEEEEE') # default #FFFFFF

  print i.getIcon() # return svg code
  # or
  i.save('hello.svg') # save file
```

**type_iden** - default 'pixel', available ('pixel', 'circle')
**size** - default (pixel = 480, circle = 1000)
