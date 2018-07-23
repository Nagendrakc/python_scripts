#!/usr/bin/python
#
#	This script download the latest file from the http repository
#	This script, if it is executed as part of cron job, then keep 
#	checking for the http repo for new file, if there is any new file
#	then download it
#	Also, it has space management, user can define allocated storage size
#	for the downloaded file. if it crosses the defined limit, then remove the 
#	oldest file to make space for new file.
#
import os
import urllib2
import requests
from lxml import html
from bs4 import BeautifulSoup
import wget
import os
import time
import re

total_allocated_storage = 25	# totoal reserved storage spce size in GB
storage_path = '/root/http/html/downloaded_file/'    # Path on where the downloaded file will be placed

# Define proxy dict, if there is any
proxy_data = {
		"https": "https://proxy101.com:8080",
		"http": "http://proxy101.com:8080"
	     }

# Fucntion to monitor the storage space reserved for downloaded files
# It removes the oldest downloaded file if it crosses more than "total_allocated_storage"	 
def monitor_storage():
	files = os.listdir(storage_path)
	print files
	total_size = sum( os.path.getsize(storage_path+f) for f in files)/1024/1024/1024
	print total_size,'GB'
	sorted_files = []
	for k in files:
		if 'HPEOneView' not in k:
			continue
		else:
			sorted_files.append(k)
	sorted_files.sort()
	if total_size >= total_allocated_storage:
		print 'Storage space reached limit'
		print 'removing file {0}'.format(sorted_files[0])
		os.remove(storage_path + sorted_files[0])

# Download the give file using wget
		
def downloadFile(file):
	wget.download(url+file, storage_path+file)

url = 'http://website-where-the-files-are-hosted.net/LatestVersions/rel/2.00/OVAfiles/'

file_list = []

d = requests.get(url, proxies=proxy_data)
soup = BeautifulSoup(d.content, 'html.parser')

for links in soup.find_all('a'):
	if ('.sig' in str(links)) or ('sha256' in str(links)) or ('FAILED' in str(links)) or ('stringinfile' not in str(links)):
		continue
	else:
		file_list.append(links.get('href'))
		print links.get('href')

file_list.sort()
available_ova_build_id =0 

# If the file contains build ID, then it can be used to find the latest build and form a file name to download

for i in file_list:
	bn = re.findall('\d{5,10}', i)
	if int(bn[0]) > available_ova_build_id:
		available_ova_build_id =int(bn[0])
		file_name = i

print available_ova_build_id
print file_name
to_download_file_path = url + file_name
print to_download_file_path

monitor_storage()

# Check if the file is already present in local storage, if not, then download

dir_list = os.listdir(storage_path)
if file_name not in dir_list:
	print 'downloading file {0}'.format(file_name)
	downloadFile(file_name)
