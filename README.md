# s3-stats
## Overview  
Will create some basic statistics for an s3 account  
## Installation
Download this repo. Then run
`python setup.py install` 
## Prerequisites  
Please have AWS access keys stored as environment variables or in your ~/.aws folder, as  
described here https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
## To Use
`python src/s3_stats.py`
To convert bytes to another format:
"Gi" for Gb, "Mi" for Mb and "ki" for kb. Pass as optional arg, i.e.:
`python src/s3_stats.py -c Mi`
## Tests
Please make sure you have Docker and docker-compose installed on your computer. A test fixture
will be generated that utilizes docker to install a local version of S3
(Minio). Then, simply run
`pytest`
## Troubleshooting
If the script errors, please set your PYTHONPATH:
`export PYTHONPATH=<repo-path>`
