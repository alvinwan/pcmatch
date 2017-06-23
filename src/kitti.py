"""Invokes the label script on segmented KITTI point clouds.

Usage:
    kitti.py [options]

Options:
    --templates=<path>      Path to templates [default: ./data/templates/*.npy]
    --kitti=<path>          Path to KITTI data [default: /rscratch/bichen/data/KITTI_raw]
"""

import docopt
import os
import os.path
from label import load_data
from label import label
import numpy as np


def main():
    arguments = docopt.docopt(__doc__)
    template_path = arguments['--templates']
    path_kitti = arguments['--kitti']

    drives = []
    for date in os.listdir(path_kitti):
       if date.startswith('2011'):
          path_date = os.path.join(path_kitti, date)
          for drive in os.listdir(path_date):
             if drive.startswith('2011'):
                drive_path = os.path.join(path_date, drive, 'seg', 'data')
                if not os.path.exists(drive_path):
                   print(' * Skipping (path does not exist)', drive_path)
                   continue
                print(' * Labeling', drive_path)
                samples_path = os.path.join(drive_path, '*.npy')
                templates = load_data(template_path)
                samples = load_data(samples_path)
                labels = label(templates, samples)
                out_path = os.path.join('./out', date, drive, 'labels.npy')
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                np.save(out_path, labels)


if __name__ == '__main__':
    main()
