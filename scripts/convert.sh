python templates_to_clusters.py
python label.py --raw=./data/test/$1.npy
python clusters_to_js.py ./data/test/$1.npy ./data/labelled/labels.npy --out=./viewer/js/
