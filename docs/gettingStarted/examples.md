---
layout: default
title: Examples
parent: Getting Started
nav_order: 5
---

## Example of Transformer Class
This example demonstrates the use of the Transformer class.

`LOAD DEPENDENCIES`
```python import pprint, sys, os 

# Add path (if necessary)
dir_path = os.path.dirname(os.path.realpath(__file__))
par_dir = os.path.dirname(dir_path)
sys.path.insert(0, par_dir)

from mz.Transformer import Transformer #import Transformer class
from mz.utils_ import gen_randomData #import random data generator
```