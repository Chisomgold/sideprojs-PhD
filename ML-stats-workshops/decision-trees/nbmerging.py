import nbformat
from nbmerge import main

merged = main([
    'Decision_trees.ipynb',
    '02_decision_tree_classification.ipynb',
    '03_random_forest_classification.ipynb',
    '04_xgboost_classification.ipynb',
    '05_random_forest_regression.ipynb',
    '06_xgboost_regression.ipynb'
])

with open('merged.ipynb', 'w', encoding='utf-8') as f:
    nbformat.write(merged, f)
