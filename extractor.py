# Import necessary libraries

import sys
import os
from PIL import Image
from PIL.ExifTags import TAGS
from docx import Document
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from tabulate import tabulate
from termcolor import colored

# Define a list of sensitive properties for metadata filtering

sensitive_properties = [
    "Author", "Creator", "Producer", "UserComment", "Software",
    "Make", "Model", "Artist", "Copyright", "CameraOwnerName",
    "GPSInfo", "GPSLatitude", "GPSLongitude", "GPSAltitude", "GPSTimeStamp",
    "GPSDateStamp", "GPSLatitudeRef", "GPSLongitudeRef", "GPSAltitudeRef",
    "GPSProcessingMethod", "GPSSpeed", "GPSSpeedRef",
    "GPSImgDirection", "GPSImgDirectionRef",
    "GPSMapDatum", "GPSDestLatitude", "GPSDestLongitude",
    "GPSDestBearing", "GPSDestDistance", "GPSDestLatitudeRef",
    "GPSDestLongitudeRef", "GPSDestBearingRef", "GPSDestDistanceRef",
    "GPSDifferential", "GPSAreaInformation", "GPSDate", "GPSDOP",
    "GPSMeasureMode", "GPSPitch", "GPSRoll", "GPSSatellites",
    "GPSStatus", "GPSTrack", "GPSTrackRef", "GPSVersionID"
]

# Print metadata in a formatted table with sensitive properties highlighted in red

def print_metadata(file_path, metadata_type, metadata):
    formatted_metadata = []
    max_value_length = 250
    for key, value in metadata.items():
        str_value = str(value)
        if len(str_value) > max_value_length:
            str_value = str_value[:max_value_length] + '...'
        if key in sensitive_properties:
            formatted_key = colored(key, "red")
            formatted_value = colored(str_value, "red")
        else:
            formatted_key = key
            formatted_value = str_value
        formatted_metadata.append((formatted_key, formatted_value))

    formatted_file_path = colored(file_path, "green")
    print(f"\n{formatted_file_path}: {metadata_type}")
    print(tabulate(formatted_metadata, headers=["Property", "Value"]))

# Extract image metadata using the Python Imaging Library (PIL) and print it

def extract_image_metadata(file_path):
    try:
        with Image.open(file_path) as img:
            metadata_raw = img._getexif()
            if metadata_raw is None:
                print(f"\n{file_path}: No Exif metadata found")
                return

            metadata = {}
            for tag, value in metadata_raw.items():
                metadata[TAGS.get(tag, tag)] = value

            print_metadata(file_path, "Image metadata", metadata)
    except Exception as e:
        print(f"{file_path}: Error: {e}")

# Extract Word document metadata using python-docx and print it

def extract_docx_metadata(file_path):
    try:
        doc = Document(file_path)
        metadata = doc.core_properties.__dict__
        print_metadata(file_path, "Word document metadata", metadata)
    except Exception as e:
        print(f"{file_path}: Error: {e}")

# Extract PDF metadata using pdfminer and print it

def extract_pdf_metadata(file_path):
    try:
        with open(file_path, 'rb') as file:
            parser = PDFParser(file)
            doc = PDFDocument(parser)

            if not doc.is_extractable:
                raise PDFTextExtractionNotAllowed

            metadata = doc.info
            print_metadata(file_path, "PDF metadata", metadata)
    except (PDFNoOutlines, PDFTextExtractionNotAllowed) as e:
        print(f"{file_path}: Error: {e}")

# Process a directory, extracting metadata from supported file types

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            _, file_extension = os.path.splitext(file_path)
            if file_extension.lower() in [".jpg", ".jpeg", ".png"]:
                extract_image_metadata(file_path)
            elif file_extension.lower() == ".docx":
                extract_docx_metadata(file_path)
            elif file_extension.lower() == ".pdf":
                extract_pdf_metadata(file_path)


# Main function, checks for valid input and processes the specified directory

if __name__ == "__main__":
    # Check if the correct number of command line arguments is provided (2 in this case: script name and directory)
    if len(sys.argv) != 2:
        print("Usage: python extractor.py <directory>")
        sys.exit(1)
    # Get the directory path from the command line argument
    directory = sys.argv[1]
    # Check if the provided path is a valid directory, exit the script if it's not
    if not os.path.isdir(directory):
        print("Directory not found")
        sys.exit(1)
 # If the input is valid and the directory exists, process the directory to extract metadata from supported files
    process_directory(directory)
