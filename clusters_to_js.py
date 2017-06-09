"""Convert from .npy to .js dictionaries.

Usage:
    convert.py <input_path> [options]
    convert.py <input_path> <label_path> [options]

Options:
    --out=<out>     Path for output [default: ./viewer/js/data/output.js]
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
label_path = arguments['<label_path>']

os.makedirs('./out', exist_ok=True)

data = {}
pcs, paths, i = load_data(template_path), glob.iglob(template_path), 0
labels = np.load(label_path) if label_path is not None else paths

for path, pc, label in zip(paths, pcs, labels):
    obj_name = os.path.basename(path).replace('.npy', '').replace('.stl', '')
    import pdb
    pdb.set_trace()
    data[obj_name] = {'vertices': [{'x': x, 'y': y, 'z': z} for x, y, z in pc]}
    if label_path is not None:
        data[obj_name]['label'] = label


with open(out_path, 'w') as f:
    f.write('var %s = %s' % (variable, str(data)))
