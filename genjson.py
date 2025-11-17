import os
import json

def generate_image_manifest(root_dir="images"):
    """
    Recursively scans the root_dir (e.g., 'images/') and collects all image file paths
    relative to that root, simulating the structure of the front-end data.
    
    IMPORTANT: This script MUST be run from the same directory that contains 
    your 'images' folder (e.g., the root of your project).
    """
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
    manifest = []

    if not os.path.exists(root_dir):
        print(f"Error: Directory '{root_dir}' not found. Please create it and add your image folders (e.g., Arches, Canyonlands) inside.")
        return []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        relative_path = os.path.relpath(dirpath, root_dir)
        
        if relative_path == '.':
            relative_path = ''

        for filename in filenames:
            if filename.lower().endswith(image_extensions):
                # Ensure correct path separator for web URLs
                full_path_relative_to_images = os.path.join(relative_path, filename).replace('\\', '/')
                
                # We only want paths that represent a folder structure, e.g., 'Arches/image.jpg'
                if '/' in full_path_relative_to_images:
                    manifest.append(full_path_relative_to_images)
                    
    return manifest

def write_manifest_to_json(manifest, output_file="data.json"):
    """Writes the manifest array to a JSON file."""
    try:
        with open(output_file, 'w') as f:
            json.dump(manifest, f, indent=4)
        print(f"Successfully generated {len(manifest)} entries in {output_file}.")
        print("Place 'data.json' in the root directory alongside your 'index.html'.")
    except Exception as e:
        print(f"An error occurred while writing the JSON file: {e}")


if __name__ == "__main__":
    print("Starting image manifest generation...")
    image_manifest = generate_image_manifest()
    
    if image_manifest:
        write_manifest_to_json(image_manifest)
    else:
        print("Manifest is empty. Did you run the script from the correct location, and are there images in subfolders of 'images/'?")