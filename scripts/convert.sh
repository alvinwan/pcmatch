#python src/templates_to_clusters.py
python src/mesh_to_cloud.py
python src/label.py --raw=./data/data/*.npy
python src/clusters_to_js.py "./data/data/*.npy" ./data/labelled/labels.npy --out=./viewer/js/
#python src/clusters_to_js.py "./data/templates/*.npy" --out=./viewer/js/templates.js --variable=templates
