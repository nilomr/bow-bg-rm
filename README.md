# Bird background removal pipeline

This project provides a Python pipeline to download bird illustrations from Birds of the World (https://birdsoftheworld.org/bow/home), remove their backgrounds using a semantic segmentation model, and save them as compressed PNG files with transparent backgrounds.

## Setup

1. Install Python 3.9+.
2. Clone the repository.
3. Create a virtual environment: `python -m venv .venv`
4. Activate it: `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)
5. Install dependencies: `pip install -r requirements.txt`

## Usage

1. Place your bird data CSV in the `data/` directory (not included due to copyright).
2. Edit `species_to_process` in `process_birds.py` to select species.
3. Run: `python process_birds.py`

Processed images will be in `processed/`.

## Data privacy

The CSV data contains copyrighted illustrations and is not included in this repository.

## Dependencies

- pandas, requests, rembg (using u2net), pillow, onnxruntime