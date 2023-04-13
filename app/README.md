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
