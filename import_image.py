import cloudinary
# Import the cloudinary.api for managing assets
import cloudinary.api
# Import the cloudinary.uploader for uploading assets
import cloudinary.uploader

import string

cloudinary.config(
    cloud_name="devwy53sh",
    api_key="244389599412372",
    api_secret="da--HG37wTXmNog65BnEWtPa3Vc",
    secure=True,
)

def uploadImage(name):
  name1 = name.replace(".","")
  cloudinary.uploader.upload(name, public_id=name1, unique_filename=True, overwrite=True)
  return cloudinary.CloudinaryImage(name1).build_url()