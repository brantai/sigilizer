# Planetary Sigilizer

Converts any string into a sigil based on corresponding [planetary magic squares](https://en.wikipedia.org/wiki/Magic_square#Europe_after_15th_century).

```
sigilize.py <string to be sigilized> <planet name> <filename>
```

## Install Dependencies

```
pip install "drawsvg~=2.0"
```

## Example:

```
sigilize.py -m "Hello World" -p mercury -f helloworld.svg
```

## Result:

![Result](helloworld.svg)
