# File Metadata Extractor

The File Metadata Extractor is a Python script that extracts metadata from various file types, including images (JPEG, PNG), PDFs, and Word documents. Potentially sensitive metadata gets flagged in red. 

## Installation

To install the required dependencies, navigate to the directory containing the `requirements.txt` file and run the following command:
`pip install -r requirements.txt`

This will install the required packages listed in the `requirements.txt` file.

## Usage

To run the File Metadata Extractor, navigate to the directory containing the `extractor.py` file and run the following command:

`python extractor.py [path_to_directory]`

Replace `[path_to_directory]` with the path to the directory containing the files you want to extract metadata from. The script will automatically detect the file type and extract the appropriate metadata.

## Output

The script will print the metadata for each file in a table format. Sensitive metadata properties will be highlighted in red to make them easy to identify.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

The File Metadata Extractor is provided as-is, without warranty of any kind, express or implied. The authors of this project are not responsible for any damage or loss caused by the use or misuse of this script. This tool should only be used for ethical and legal purposes, such as extracting metadata from your own files or with the explicit permission of the owner of the files. It is the user's responsibility to comply with all applicable laws and regulations.