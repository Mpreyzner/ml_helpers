from google_images_download import google_images_download
import sys

# first install https://github.com/hardikvasa/google-images-download
# usage python get_my_images.py "bear, smelly cat" 200
response = google_images_download.googleimagesdownload()
keywords = (sys.argv[1:2])
limit = sys.argv[2:] or 100
arguments = {"keywords": keywords, "limit": limit, "print_urls": True}
response.download(arguments)
