"""Convert clouds to clusters.

Usage:
    cloud_to_clusters.py <path> [options]

Options:
    --out=<out>     Directory containing output [default: ./out]
"""

from collections import defaultdict

import docopt
import glob
import numpy as np
import os.path


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
    return clusters


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
        np.save(out_path, np.vstack(vertices))


def main():
    arguments = docopt.docopt(__doc__)
    write_clouds_to_clusters(arguments['<path>'], arguments['--out'])


if __name__ == '__main__':
    main()
