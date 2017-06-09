"""Compare each sample with a point cloud, and label it accordingly.

Usage:
    label.py [options]
    label.py raw_dir <dir> [options]

Options:
    --template=<path>   Path to templates [default: ./data/templates/*.npy]
    --raw=<path>        Path to unclassified data [default: ./data/raw/*.npy]
    --out=<out>         Directory for final results [default: ./out]
"""

import docopt
import glob
import numpy as np
import os
import os.path
from thirdparty.icp import icp


def load_data(path_glob: str) -> np.array:
    """Load all point clouds. Expects points to be n x k"""
    return [np.load(path)[:, :3] for path in sorted(glob.iglob(path_glob))]


def label(templates: np.array, samples: np.array) -> np.array:
    """Use ICP to classify all samples."""
    labels = None
    for sample in samples:
        results = [icp(sample, template, max_iterations=1) for template in templates]
        distances = [np.sum(distance) for _, _, distance in results]

        i = int(np.argmin(distances))
        T, t, _ = results[i]  # T (4x4) and t (3x1)
        label = np.hstack((i, distances[i], np.ravel(T), np.ravel(t))).reshape((1, -1))
        labels = label if labels is None else np.vstack((labels, label))
    if labels is None:
        raise UserWarning('No samples found.')
    labels[:, 1] = 1 - (labels[:, 1] / np.max(labels[:, 1]))
    return labels


def write_dir_labels(template_path: str, raw_dir: str, out_dir: str):
    """Write labels for all clusters in specified directory.

    Hardcoded to use the directory structure in cloud_to_clusters.

    raw_dir/<drive>/<cloud>/*.npy
    """
    for directory in os.listdir(raw_dir):
        drive_dir = os.path.join(raw_dir, directory)
        for subdirectory in os.listdir(drive_dir):
            raw_path = os.path.join(drive_dir, subdirectory, '*.npy')
            out_path = os.path.join(out_dir, directory, subdirectory, 'labels.npy')
            write_labels(template_path, raw_path, out_path)


def write_labels(template_path: str, raw_path: str, out_path: str):
    """Label all files specified by raw_path."""
    templates = load_data(template_path)
    samples = load_data(raw_path)

    labels = label(templates, samples)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    np.save(out_path, labels)

    print(' * [INFO] Finished processing timestep. (saved to ', out_path, ')')


def main():
    arguments = docopt.docopt(__doc__)

    template_path = arguments['--template']
    raw_path = arguments['--raw']
    out_dir = arguments['--out']

    if arguments['raw_dir']:
        write_dir_labels(template_path, arguments['<dir>'], out_dir)
    else:
        out_path = os.path.join(out_dir, 'labels.npy')
        write_labels(template_path, raw_path, out_path)


if __name__ == '__main__':
    main()
