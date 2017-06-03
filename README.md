# Point Cloud Matching

Uses iterative closest point (ICP) to match sample point clouds to templates.
To visualize the results in an interactive viewer, see [`viewer/`](http://github.com/alvinwan/pcmatch/tree/master/viewer).

> To convert existing .stl, .obj, .xaml, .pkl etc. objects into numpy arrays,
see [this gist](https://gist.github.com/alvinwan/06c875531dc57fdd5dce6cf56ed8cbc3) I wrote. The script additionally centers and scales the point cloud.

# Install

The project is written in Python 3 and is not guaranteed to successfully backport to Python 2.

(Optional) We recommend setting up a virtual environment.

```
virtualenv pcm --python=python3
source activate pcm/bin/activate
```

Say `$PCM_ROOT` is the root of your repository. Navigate to your root repository.

```
cd $PCM_ROOT
```

We need to setup our Python dependencies.

```
pip install -r requirements.txt
```

# Run

By default, the script looks for sample point clouds in `./data/raw` and
template point clouds in `./data/templates`. All point cloud files are `.npy`
files containing `nx3` matrices of `x,y,z` respectively.

```
python label.py
```

Here are full usage instructions:

```
Usage:
    label.py [options]

Options:
    --template=<path>   Path to templates [default: ./data/templates/*.npy]
    --raw=<path>        Path to unclassified data [default: ./data/raw/*.npy]
    --out=<out>         Path for final results [default: ./out/labels.npy]
```
