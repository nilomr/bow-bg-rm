import pandas as pd
import requests
from rembg import remove
from PIL import Image
import io
import os

# Read the CSV
df = pd.read_csv("data/bow-data.csv", encoding="latin1")

# Filter for specific species to test
species_to_process = ["Brown-headed Nuthatch", "Bahama Nuthatch"]
filtered_df = df[df["primary_com_name"].isin(species_to_process)]

# Create processed directory if not exists
os.makedirs("processed", exist_ok=True)

for index, row in filtered_df.iterrows():
    asset_id = row["asset_id"]
    primary_name = row["primary_com_name"].replace(" ", "_")
    url = f"https://cdn.download.ams.birds.cornell.edu/api/v1/asset/{asset_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        image_data = response.content

        # Remove background
        output_data = remove(image_data)

        # Open with PIL
        image = Image.open(io.BytesIO(output_data))

        # Save as compressed PNG with transparent background
        output_path = f"processed/{primary_name}_{asset_id}.png"
        image.save(output_path, "PNG", optimize=True)

        print(f"Processed and saved: {output_path}")

    except Exception as e:
        print(f"Failed to process {asset_id}: {e}")
