"""Convert clouds to clusters.

Usage:
    cloud_to_clusters.py path <path> [options]
    cloud_to_clusters.py dir <dir> [options]

Options:
    --out=<out>     Directory containing output [default: ./data/clusters]
"""

from collections import defaultdict

import docopt
import glob
import numpy as np
import os.path


def write_clouds_dir_to_clusters(clouds_dir: str, out_dir: str):
    """Write all clouds contained in subdirectories from cloud_dir/.

    Hardcoded to use the directory structure in KITTI_raw at Aspire.

    cloud_dir/<drive>/seg/data/*.npy
    """
    for directory in sorted(os.listdir(clouds_dir)):
        clouds_path = os.path.join(clouds_dir, directory, 'seg', 'data', '*.npy')
        new_out_dir = os.path.join(out_dir, directory)
        write_clouds_to_clusters(clouds_path, new_out_dir)


def write_clouds_to_clusters(clouds_path: str, out_dir: str):
    """Write all clouds to cluster numpy files.

    This function assumes that all clouds are formatted as (64, 1024, 13),
    where the last dimension is the number of channels, and 64/1024 are various
    sets of points.
    """
    for cloud_path in glob.iglob(clouds_path):
        cloud = np.load(cloud_path).reshape(-1, 13)
        clusters = cloud_to_clusters(cloud)
        cluster_dir = get_cluster_dir(cloud_path, out_dir)
        write_clusters(clusters, cluster_dir)
        print(' * [INFO] Finished processing cloud',
              os.path.basename(cloud_path).replace('.npy', ''),
              '(saved to ', cluster_dir, ')')


def cloud_to_clusters(cloud: np.array) -> np.array:
    """Converts provided cloud into a set of clusters."""
    clusters = defaultdict(lambda: [])
    for vertex in cloud:
        center = tuple(vertex[6:9])
        if center != (0, 0, 0):
            clusters[center].append(vertex)

    print(' * [INFO]', len(list(clusters.keys())), 'clusters found')
    for key in clusters:
        clusters[key] = process_cluster(np.vstack(clusters[key]))
    return clusters


def process_cluster(cluster: np.array, scale: float=3.0) -> np.array:
    """Pre-process the cluster.

    We first demean and then scale up the object.
    """
    demeaned = cluster.copy()
    demeaned[:, :3] -= cluster[:, 6:9]
    demeaned[:, :3] *= scale
    return demeaned


def get_cluster_dir(cloud_path: str, out_dir: str) -> str:
    """Creates new path for cluster, using cloud path and output root dir."""
    cloud_name = os.path.basename(cloud_path).replace('.npy', '')
    cluster_dir = os.path.join(out_dir, cloud_name)
    os.makedirs(cluster_dir, exist_ok=True)
    return cluster_dir


def write_clusters(clusters: np.array, cluster_dir: str):
    """Writes all clusters to individual numpy files."""
    for center, vertices in clusters.items():
        out_path = os.path.join(cluster_dir, '%f_%f_%f' % center)
        out_data = np.vstack(vertices)
        assert out_data.shape[1] > 3
        np.save(out_path, out_data)


def main():
    arguments = docopt.docopt(__doc__)
    if arguments['path']:
        write_clouds_to_clusters(arguments['<path>'], arguments['--out'])
    else:
        write_clouds_dir_to_clusters(arguments['<dir>'], arguments['--out'])


if __name__ == '__main__':
    main()
