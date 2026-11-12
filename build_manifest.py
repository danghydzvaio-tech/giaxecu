"""Record hashes for the complete trained-model package."""
import hashlib
import json
from pathlib import Path


def write_manifest(folder):
    folder = Path(folder)
    names = ['ann_bundle.joblib', 'evaluation.json', 'reference.csv', 'training_history.csv',
             'holdout_predictions.csv', 'split_indices.npz']
    manifest = {'schema_version': 1, 'sha256': {
        name: hashlib.sha256((folder / name).read_bytes()).hexdigest() for name in names}}
    (folder / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    return manifest


if __name__ == '__main__':
    write_manifest(Path(__file__).resolve().parent / 'artifacts')
