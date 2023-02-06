## Example to make profiling

```
python -m cProfile -o program.prof detection.py

```

### It can visualized with snakeviz

```
pip install snakeviz
snakeviz program.prof
```

### Another example with cProfile

```
python -m cProfile -o output.pstats detection.py
```

This can be visualized with:

```
sudo apt install dot2tex
gprof2dot --colour-nodes-by-selftime -f pstats output.pstats | dot -Tpng -o output.png
```

### Torch profiler

It is possible also to use the profiler provided by torch, the documentation can be
found in the next link:

https://pytorch.org/tutorials/recipes/recipes/profiler_recipe.html


### In case you have the following error:

```
QObject::moveToThread: Current thread (0x2db0dde0) is not the object's thread (0x2e64aec0).
Cannot move to target thread (0x2db0dde0)

qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "/home/pi/.local/lib/python3.9/site-packages/cv2/qt/plugins" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

Available platform plugins are: xcb, dxcb, xcb, eglfs, linuxfb, minimal, minimalegl, offscreen, vnc.
```

### Apply the workaround

```
sudo $HOME/.local/lib/python3.9/site-packages/cv2/qt/plugins/platforms/libqxcb.so
```
