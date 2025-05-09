import os
import json
import glob
from pathlib import Path
import fiftyone as fo
from PIL import Image 

# Paths to your dataset
DATASET_ROOT = "ScreenSpot-v2"
ANNOTATIONS_DIR = DATASET_ROOT
IMAGES_DIR = os.path.join(DATASET_ROOT, "screenspotv2_image")

def convert_bbox_to_relative(bbox, img_size):
    """
    Convert absolute bounding box coordinates to relative coordinates.
    
    Args:
        bbox (list): Absolute bounding box in format [x, y, width, height]
        img_size (list): Image dimensions in format [width, height]
    
    Returns:
        list: Relative bounding box in format [x, y, width, height] in range [0, 1]
    """
    img_width, img_height = img_size
    x, y, width, height = bbox
    
    # Convert to relative coordinates (normalized between 0 and 1)
    rel_x = x / img_width
    rel_y = y / img_height
    rel_width = width / img_width  # Width is already width, not x2-x1
    rel_height = height / img_height  # Height is already height, not y2-y1
    
    return [rel_x, rel_y, rel_width, rel_height]



def parse_annotation_files():
    """
    Parse all annotation files and create FiftyOne samples.
    
    Reads all JSON annotation files from the annotations directory,
    processes each entry, and creates a list of FiftyOne samples
    with the required fields.
    
    Returns:
        list: List of FiftyOne Sample objects
    """
    samples = []
    
    # Get all JSON annotation files
    annotation_files = glob.glob(os.path.join(ANNOTATIONS_DIR, "*.json"))
    
    for annotation_file in annotation_files:
        print(f"Processing {os.path.basename(annotation_file)}...")
        
        # Load annotation file
        with open(annotation_file, 'r', encoding='utf-8') as f:
            annotations = json.load(f)
        
        # Process each annotation entry in the JSON file
        for annotation in annotations:
            # Construct full image path
            image_path = os.path.join(IMAGES_DIR, annotation["img_filename"])
            
            # Skip if image doesn't exist
            if not os.path.exists(image_path):
                print(f"Warning: Image not found: {image_path}")
                continue
            
            # Get image dimensions by opening the image
            try:
                with Image.open(image_path) as img:
                    img_width, img_height = img.size
            except Exception as e:
                print(f"Warning: Could not open image {image_path}: {e}")
                continue
            
            # Convert bounding box to relative coordinates (FiftyOne format)
            bbox_relative = convert_bbox_to_relative(annotation["bbox"], [img_width, img_height])
            
            # Create detection object for the UI element
            # Label will be the ui_type value (e.g., "icon" or "text")
            detection = fo.Detection(
                label=annotation["data_type"],
                bounding_box=bbox_relative
            )
            
            # Create base sample with filepath
            sample = fo.Sample(filepath=image_path)
            
            # Add fields to sample explicitly
            sample["ui_id"] = annotation.get("id")  # Use .get() in case id is missing
            sample["instruction"] = annotation["instruction"]
            sample["data_source"] = fo.Classification(label=annotation["data_source"])
            sample["action_detection"] = detection
            
            samples.append(sample)
    
    print(f"Processed {len(samples)} samples total")
    return samples

def main():
    """
    Main function to create and populate the FiftyOne dataset.
    
    Creates a new dataset named "ScreenSpot_Pro", parses all annotation files,
    adds samples to the dataset, computes metadata, and adds dynamic sample fields.
    
    Returns:
        fo.Dataset: The created FiftyOne dataset
    """
    # Create dataset (overwrite if exists)
    dataset = fo.Dataset("ScreenSpot_v2", overwrite=True)

    samples = parse_annotation_files()

    dataset.add_samples(samples)
    
    dataset.compute_metadata()
    
    dataset.add_dynamic_sample_fields()
    
    dataset.save()
    return dataset