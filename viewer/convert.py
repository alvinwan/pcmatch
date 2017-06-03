"""Convert from .npy to .js dictionaries.

Usage:
    convert.py <input_path> [options]

Options:
    --out=<out>     Path for output [default: ./out]
"""

import docopt
import glob
import os
import os.path
import numpy as np

arguments = docopt.docopt(__doc__)
template_path = arguments['<input_path>']
out_path = arguments['--out']

os.makedirs('./out', exist_ok=True)

data = {}
for path in glob.iglob(template_path):
    obj_name = os.path.basename(path).replace('.stl.npy', '')
    data[obj_name] = [{'x': x, 'y': y, 'z': z}
                      for x, y, z in np.load(path)]

out_path = os.path.join(out_path, 'templates.js')
with open(out_path, 'w') as f:
    f.write('var templates = %s' % str(data))
