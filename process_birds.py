import pandas as pd
import requests
from rembg import remove
from PIL import Image
import io
import os
import time
from tqdm import tqdm
import concurrent.futures


def process_bird(row):
    asset_id = row["asset_id"]
    species_code = row["species_code"]
    url = f"https://cdn.download.ams.birds.cornell.edu/api/v1/asset/{asset_id}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        image_data = response.content

        # Remove background
        output_data = remove(image_data)

        # Open with PIL
        image = Image.open(io.BytesIO(output_data))

        # Save as compressed PNG with transparent background
        output_path = f"processed/{species_code}_{asset_id}.png"
        image.save(output_path, "PNG", optimize=True)

        return f"Processed and saved: {output_path}"

    except Exception as e:
        return f"Failed to process {asset_id}: {e}"


# Read the CSV
df = pd.read_csv("data/bow-data.csv", encoding="latin1")

# Select 20 random birds
filtered_df = df.sample(40)

# Create processed directory if not exists
os.makedirs("processed", exist_ok=True)

start_time = time.time()

with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
    futures = [
        executor.submit(process_bird, row) for index, row in filtered_df.iterrows()
    ]

    for future in tqdm(
        concurrent.futures.as_completed(futures),
        total=len(futures),
        desc="Processing birds",
    ):
        result = future.result()
        tqdm.write(result)

end_time = time.time()
print(f"Total processing time: {end_time - start_time:.2f} seconds")
