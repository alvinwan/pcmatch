"""Converts a mesh into point cloud.

This file, as a script, will convert a mesh binary into .npy. It is written for
python3, but if the output directory exists, then remove L28 to use python2.


Usage:
    mesh_to_cloud.py [options]

Options:
    --data=<data>       Path to data [default: ./data/mesh/*.*]
    --n=<n>             Number of points to sample [default: 3000]
    --out=<out>         Root of output directory [default: ./data/templates]
    --scale=<scale>     Scale all sizes by [default: 0.2]
"""

import docopt
import trimesh
import os
import numpy as np
import glob
import os.path

from trimesh.sample import sample_surface


array_hooks = {}
mesh_hooks = {}
VAN_LENGTH = 206
SPORTS_LENGTH = 176
TRUCK_LENGTH = 550
SEDAN_LENGTH = 211
PICKUP_LENGTH = 228
SMALL_LENGTH = 106
BUS_LENGTH = 500
JEEP_LENGTH = 132
SUV_LENGTH = 240
PEDESTRIAN_HEIGHT = 69
CYCLIST_LENGTH = 68


def array(name):
    """Use @array(<vehicle name>) to setup a conversion hook.

    When processing an array with named <vehicle name>, the annotated function
    will then be called, with the array provided.

    :param name: Name of the vehicle in question. Must be the name of the file.
    """
    def decorator(f):
        def function(*args, **kwargs):
            print(' * [INFO] Array hook for %s run.' % name)
            return f(*args, **kwargs)
        if name not in array_hooks:
            array_hooks[name] = []
        array_hooks[name].append(function)
        return f
    return decorator


def mesh(name, **kwargs):
    """Use @mesh(<vehicle name>) to setup a conversion hook.

    When processing a mesh file named <vehicle name>, the annotated function
    will then be called, with the mesh object provided.

    :param name: Name of the vehicle in question. Must be the name of the file.
    :param kwargs: Passed into the conversion function.
    """
    def decorator(f):
        def function(*args, **kwargs_inner):
            print(' * [INFO] Mesh hook for %s run.' % name)
            kwargs_inner.update(kwargs)
            return f(*args, **kwargs_inner)
        mesh_hooks[name] = function
        return f
    return decorator


def main():
    """Passes command line arguments into utility function."""
    arguments = docopt.docopt(__doc__)
    input_path = arguments['--data']
    output_dir = arguments['--out']
    n = int(arguments['--n'])
    scale = float(arguments['--scale'])
    os.makedirs(output_dir, exist_ok=True)

    paths = list(glob.iglob(input_path))
    if not paths:
        raise UserWarning('No files found at %s' % input_path)

    for path in paths:
        mesh = trimesh.load(path)
        name = os.path.basename(path).split('.')[0]
        if name in mesh_hooks:
            mesh = mesh_hooks[name](mesh)
        points = sample_surface(mesh, n) * scale
        points -= points.mean(axis=0)
        if name in array_hooks:
            for function in array_hooks[name]:
                points = function(points)
        output_path = os.path.join(output_dir, name)
        np.save(output_path, points)


@mesh('van', total=VAN_LENGTH)
@mesh('sports', total=SPORTS_LENGTH)
@mesh('truck', total=TRUCK_LENGTH)
@mesh('sedan', total=SEDAN_LENGTH)
@mesh('pickup', total=PICKUP_LENGTH)
@mesh('small', total=SMALL_LENGTH)
@mesh('bus', total=BUS_LENGTH)
@mesh('jeep', total=JEEP_LENGTH)
@mesh('suv', total=SUV_LENGTH)
@mesh('pedestrian', total=PEDESTRIAN_HEIGHT)
@mesh('cyclist', total=CYCLIST_LENGTH)
def rescale(mesh: trimesh.Trimesh, total: float) -> trimesh.Trimesh:
    mesh.apply_scale(total / mesh.scale)
    return mesh


@array('pickup')
@array('van')
@array('suv')
def swap_x_z(points: np.array) -> np.array:
    points[:, 2], points[:, 0] = points[:, 0].copy(), points[:, 2].copy()
    return points


@array('pickup')
@array('pedestrian')
@array('suv')
@array('van')
@array('jeep')
@array('sports')
@array('truck')
def swap_y_z(points: np.array) -> np.array:
    points[:, 1], points[:, 2] = points[:, 2].copy(), points[:, 1].copy()
    return points


if __name__ == '__main__':
    main()
