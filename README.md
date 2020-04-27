# Script to downlaod the file from http server
This script check for latest file uploaded in http server and then download it if the latest file is not 
present in directory where the downlaoded file is placed. This script also has intelligence to manage its
storage space by removing the oldest file on local storage media before start downloading.

Right now the script is written in very straign way using traditional function method.

I have plan to write using classes in furture, once i do it, i will upload the same here.

The script can be used for 
- Downloading the file which is has build number embedded into file name, without any modification, except http uri
- With little modification on file selection section, it can traverse inside the directory to pick the file to download


