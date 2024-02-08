# AWS S3 Image Processing Script

This project contains a Python script that automates the process of downloading images from an AWS S3 bucket, extracting EXIF data from those images, imprinting the image description and datetime onto the images themselves, and then syncing the modified images back to the S3 bucket.

## Features

- Downloads images from a specified AWS S3 bucket.
- Extracts EXIF data for each image.
- Imprints the EXIF description and datetime onto the image.
- Syncs the modified images back to an S3 bucket.

## Prerequisites

Before you can run this script, you need to have the following installed:

- Python 3.x
- AWS CLI configured with access to the S3 bucket
- Required Python libraries: `pathlib`, `os`, `subprocess`, `exifread`, `csv`, `PIL`, `boto3`

## Setup

1. Clone this repository to your local machine.
2. Ensure the AWS CLI is configured with the necessary permissions to access your S3 bucket.
3. Install the required Python dependencies by running:

pip install exifread Pillow boto3


## Usage

To run the script, navigate to the project directory and execute the main script file:

```bash
python main.py


Directory Structure
The script automatically creates the following directory structure for processing and storing images and metadata:

data/: Root directory for data processing.
csv/: Stores metadata in CSV format.
metadata/: Temporary storage for downloaded images.
imprintedimage/: Stores images with imprinted EXIF data.
modifiedmetadata/: Contains images after processing and ready for upload.
AWS S3 Sync
The script uses the AWS CLI to sync images from and to the S3 bucket. Ensure your AWS credentials have the necessary permissions for s3:ListBucket and s3:PutObject.

Contributing
Contributions to this project are welcome! Please fork the repository and submit a pull request with your improvements.

License
This project is licensed under the MIT License - see the LICENSE file for details.