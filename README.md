# Point Cloud Matching

Uses iterative closest point (ICP) to match sample point clouds to templates. Includes utilities to convert existing .stl, .obj, .xaml, .pkl etc. objects into point cloud, numpy arrays. To visualize the results in an interactive viewer, see [`viewer/`](http://github.com/alvinwan/pcmatch/tree/master/viewer).

![screen shot 2017-06-20 at 12 05 20 am](https://user-images.githubusercontent.com/2068077/27471822-f273a15a-57ad-11e7-916a-c79a4d404d49.png)

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

![templates](https://user-images.githubusercontent.com/2068077/27471876-24453f86-57ae-11e7-9fdd-074dd0c4e6dc.gif)
