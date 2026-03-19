#!/usr/bin/env python3
"""
Upload model weights and (optionally) NHANES validation data to the Hugging Face Hub.

Prerequisites:
  - pip install huggingface_hub
  - huggingface-cli login   (or set HF_TOKEN)

Usage:
  python scripts/upload_to_huggingface.py              # upload weights only
  python scripts/upload_to_huggingface.py --dataset    # upload weights + nhanes_data_dump
"""

import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WEIGHTS_DIR = REPO_ROOT / "healome_clock" / "models" / "weights"
NHANES_DIR = REPO_ROOT / "nhanes_data_dump"
WEIGHTS_REPO = "Healome/healome-clock-weights"
DATASET_REPO = "Healome/nhanes-validation-data"


def upload_weights():
    from huggingface_hub import HfApi
    api = HfApi()
    for name in ["standard_21feat.joblib", "extended_35feat.joblib"]:
        path = WEIGHTS_DIR / name
        if not path.exists():
            print(f"  Skip {name} (not found at {path})")
            continue
        print(f"  Uploading {name}...")
        api.upload_file(
            path_or_fileobj=str(path),
            path_in_repo=name,
            repo_id=WEIGHTS_REPO,
            repo_type="model",
        )
    print("  Weights uploaded to https://huggingface.co/" + WEIGHTS_REPO)


def upload_dataset():
    from huggingface_hub import HfApi
    api = HfApi()
    if not NHANES_DIR.exists():
        print(f"  Skip dataset: {NHANES_DIR} not found")
        return
    print("  Uploading nhanes_data_dump/...")
    api.upload_folder(
        folder_path=str(NHANES_DIR),
        repo_id=DATASET_REPO,
        repo_type="dataset",
    )
    print("  Dataset uploaded to https://huggingface.co/datasets/" + DATASET_REPO)


def main():
    ap = argparse.ArgumentParser(description="Upload models and/or dataset to Hugging Face Hub")
    ap.add_argument("--dataset", action="store_true", help="Also upload nhanes_data_dump to Hub")
    args = ap.parse_args()
    print("Uploading model weights...")
    upload_weights()
    if args.dataset:
        print("Uploading NHANES validation dataset...")
        upload_dataset()
    print("Done.")


if __name__ == "__main__":
    main()
