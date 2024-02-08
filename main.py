#create directories / paths
from pathlib import Path
import os

mypath = 'data'
csvpath = 'data/csv'
metadatapath = 'data/metadata'
impimgpath = 'data/imprintedimage'
modified_metadatapath = "data/modifiedmetadata"

print(os.path.isdir(mypath))
Path(csvpath).mkdir(parents=True, exist_ok=True)
Path(metadatapath).mkdir(parents=True, exist_ok=True)
Path(impimgpath).mkdir(parents=True, exist_ok=True)
Path(modified_metadatapath).mkdir(parents=True, exist_ok=True)
print(os.path.isdir(mypath))

#call a command line application from python - get results (stdout) from sync proc.
res = subprocess.check_output(['aws','s3','ls','ia628'])

#get all images from s3:
cmd = ['aws', 's3', 'sync', 's3://ia628/class/images', metadatapath]
res = subprocess.check_output(cmd)

print(res.decode()) #decode the bytes into string

#get files in directory
import os
import exifread

allowed_exts = ['jpg']
path = metadatapath
fl = [] # file list
f_name = []
if os.path.isdir(path): #is the path a valid directory?
    for file in os.listdir(path):
        ext = file.split(".")[-1]
        #print(ext)
        if ext.lower() in allowed_exts:
            fl.append(os.path.join(path, file))
            f_name.append(file)
print(f_name)

#get exif data
import exifread
#sudo python3 -m pip install exifread
image_description = {}
for index, file in enumerate(fl):
    f = open(file, 'rb')
    # Return Exif tags
    from IPython.display import Image
    display(Image(filename=file))
    
    tags = exifread.process_file(f)
    f.close()
    print(tags.keys())
    try:
        image_description[f'img{index}'] = tags['Image ImageDescription']
    except Exception:
        image_description[f'img{index}'] = "NO DESCRIPTION"


    
     
    #print(tags['Image ImageDescription'])

#append to csv
import csv
outputcsv = 'data/csv/metadata.csv'
fields = ['file','image_description']
c = open(outputcsv, 'w')
writer = csv.DictWriter(c, fieldnames = fields,lineterminator='\n')  
writer.writeheader()
for file, (key, value) in zip(f_name, image_description.items()):
    rows = []
    row= {'file':f_name,'image_description': value}
    rows.append(row)
    writer.writerows(rows)      
c.close()

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from IPython.display import Image as displayimage

imprinted_img = []
for file, (key, value) in zip(fl, image_description.items()):
    img = Image.open(file)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 100)
    draw.text((0, 0),f"{value}",(255,0,0),font=font)
    img.save(f"data/imprintedimage/{key}-imprint.jpg")
    imprinted_img.append(f"data/imprintedimage/{key}-imprint.jpg")

for filename in imprinted_img:
    display(displayimage(filename=filename))

import boto3
from pathlib import Path

def create_bucket(s3_client, bucket_name):
    """Create an S3 bucket if it does not exist."""
    if bucket_name not in [bucket['Name'] for bucket in s3_client.list_buckets()['Buckets']]:
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created.")
    else:
        print(f"Bucket '{bucket_name}' already exists.")

def upload_folder(s3_client, bucket_name, local_folder, s3_folder):
    """Upload a local folder to an S3 folder."""
    local_folder_path = Path(local_folder)
    
    for file in local_folder_path.rglob('*'):
        if file.is_file():
            s3_client.upload_file(
                Filename=str(file),
                Bucket=bucket_name,
                Key=f"{s3_folder}/{file.relative_to(local_folder_path)}"
            )

# Initialize the S3 client
s3_client = boto3.client('s3')

# Specify the S3 bucket name and the local and S3 folders
bucket_name = 'ia628'  # Replace with your S3 bucket name
main_folder_s3 = 'maddirt'
subfolders_local = ['data/csv', 'data/metadata', 'data/imprintedimage']  # Replace with your local subfolder paths

# Create the S3 bucket (if it does not exist)
create_bucket(s3_client, bucket_name)

# Upload each local subfolder to the main folder in S3
for subfolder_local in subfolders_local:
    upload_folder(s3_client, bucket_name, subfolder_local, f"{main_folder_s3}/{Path(subfolder_local).name}")

print("Upload completed.")


#fetching new metadata

import subprocess
#call a command line application from python - get results (stdout) from sync proc.
res = subprocess.check_output(['aws','s3','ls','ia628'])

#get all images from s3:
cmd = ['aws', 's3', 'sync', 's3://ia628/maddirt/imprintedimage', modified_metadatapath]
res = subprocess.check_output(cmd)

print(res.decode())