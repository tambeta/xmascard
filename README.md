# xmascard

A Python script for procedurally generating abstract "christmas cards" by
randomly partitioning a 2D plane and filling the resulting rectangles using a
preset palette.

Since it's intended as a one-off script, there is no command-line interface
and control of the script is via hardcoded constants. Feel free to fork and
improve the interface, though.

The sole external dependency is [PIL /
Pillow](https://pillow.readthedocs.io/en/stable/).

Simply execute the script and `out.png` is output into the working directory.

Example output:

![Example](https://i.imgur.com/ey5e1Ky.png)

