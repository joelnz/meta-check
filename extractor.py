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

sensitive_properties = [
    "Author", "Creator", "Producer", "UserComment", "Software",
    "Make", "Model", "Artist", "Copyright", "CameraOwnerName",
    "GPSLatitude", "GPSLongitude", "GPSAltitude", "GPSTimeStamp",
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

def print_metadata(file_path, metadata_type, metadata):
    formatted_metadata = []
    for key, value in metadata.items():
        if key in sensitive_properties:
            formatted_key = colored(key, "red")
            formatted_value = colored(str(value), "red")
        else:
            formatted_key = key
            formatted_value = str(value)
        formatted_metadata.append((formatted_key, formatted_value))

    formatted_file_path = colored(file_path, "green")
    print(f"\n{formatted_file_path}: {metadata_type}")
    print(tabulate(formatted_metadata, headers=["Property", "Value"]))

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
        
def extract_docx_metadata(file_path):
    try:
        doc = Document(file_path)
        metadata = doc.core_properties.__dict__
        print_metadata(file_path, "Word document metadata", metadata)
    except Exception as e:
        print(f"{file_path}: Error: {e}")

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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extractor.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]

    if not os.path.isdir(directory):
        print("Directory not found")
        sys.exit(1)

    process_directory(directory)