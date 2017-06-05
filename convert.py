"""Convert from .npy to .js dictionaries.

Usage:
    convert.py <input_path> [options]

Options:
    --out=<out>     Path for output [default: ./js/output.js]
    --variable=<v>  Name of variable to assign all data [default: data]
"""

import docopt
import glob
import os
import os.path
import numpy as np

from label import load_data

arguments = docopt.docopt(__doc__)
template_path = arguments['<input_path>']
out_path = arguments['--out']
variable = arguments['--variable']

os.makedirs('./out', exist_ok=True)

data = {}
pcs, paths = load_data(template_path), glob.iglob(template_path)
for path, pc in zip(paths, pcs):
    obj_name = os.path.basename(path).replace('.stl.npy', '')
    data[obj_name] = [{'x': x, 'y': y, 'z': z} for x, y, z in pc]

with open(out_path, 'w') as f:
    f.write('var %s = %s' % (variable, str(data)))
