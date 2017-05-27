"""Compare each sample with a point cloud, and label it accordingly.

Usage:
    label.py icp
    label.py opnorm
"""

import docopt
import glob
import numpy as np
import os
from thirdparty.icp import icp

from math import atan
from sklearn import linear_model
from scipy.sparse.linalg import svds
from scipy.ndimage.interpolation import rotate
from sklearn.decomposition import PCA


def load_data(path_glob: str) -> np.array:
    """Load all point clouds."""
    P = []
    for path in sorted(glob.iglob(path_glob)):
        p = np.load(path)
        if len(p.shape) == 3:
            p = p[0,:,:3]
        P.append(p)
    return P


def standardize(sample: np.array) -> np.array:
    """Standardize orientation, scale, and position."""

    # Project into R2
    pca = PCA(n_components=2)
    P = pca.fit_transform(sample)
    X, Y = np.split(P, 2, axis=1)

    # Compute orientation and rotation
    model_ransac = linear_model.RANSACRegressor(linear_model.LinearRegression())
    model_ransac.fit(X, Y)
    x = np.min(X)
    y = model_ransac.predict(x)
    theta = atan(y/x)

    # Rotate
    P = rotate(P, -theta, axes=(0, 1))

    # Center
    P -= np.mean(P, axis=0)

    # Rescale
    P /= np.max(np.linalg.norm(P, axis=1))

    return P


def label_opnorm(P_templates: np.array, P: np.array) -> np.array:
    """Use operator norm as a gauge of distance."""
    templates, labels = [], []

    for template in P_templates:
        templates.append(standardize(template))

    labels = None
    for sample in map(standardize, P):
        distances = [np.linalg.norm(template, sample, ord='op')
                     for template in templates]
        label = np.array([np.argmin(distances), min(distances)])
        labels = label if labels is None else np.vstack((labels, label))
    labels[:,1] = 1 - (labels[:,1] / np.max(labels[:,1]))
    return labels


def label_icp(templates: np.array, samples: np.array) -> np.array:
    """Use ICP to classify all samples."""
    labels = None
    for sample in samples:
        distances = [icp(sample, template)[1] for template in templates]
        label = np.array([np.argmin(distances), np.min(distances)])
        labels = label if labels is None else np.vstack((labels, label))
    labels[:,1] = 1 - (labels[:,1] / np.max(labels[:,1]))
    return labels


def main():

    arguments = docopt.docopt(__doc__)
    use_icp = arguments['icp']
    use_opnorm = arguments['opnorm']

    P_templates = load_data('./data/templates/*.npy')
    P = load_data('./data/data/*.npy')

    if use_icp:
        labels = label_icp(P_templates, P)
    elif use_opnorm:
        labels = label_opnorm(P_templates, P)

    os.makedirs('./out', exist_ok=True)
    np.save('./out/labels.npy', labels)

if __name__ == '__main__':
    main()
