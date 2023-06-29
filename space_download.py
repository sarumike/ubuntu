import boto3
from boto3 import session
from botocore.client import Config
from boto3.s3.transfer import S3Transfer

#Use the API Keys you generated at Digital Ocean
ACCESS_ID = 'UUH7GLM5ZV6SHQMP5R6K'
SECRET_KEY = '7qnpyCteMYe3O+hW7wDQATlWD072bRRauHZacGhfBjw'

#enter filename to be uploaded
local_file_name = 'snapshot_1M_max_sigs_50.gz' #file name to save to locally
target_file_name = 'snapshot_1M_max_sigs_50.gz' #file name on Space share


space_name = 'nft-testdata01'
folder_name = 'snapshots'

# Initiate session
session = session.Session()

client = session.client('s3',
         region_name='fra1', #enter your own region_name
         endpoint_url='https://nft-testdata01.fra1.digitaloceanspaces.com', #enter your own endpoint url
         aws_access_key_id=ACCESS_ID,
         aws_secret_access_key=SECRET_KEY)

transfer = S3Transfer(client)

# Downloads a file from your Space called 'name-of-space'
# saves the file on local machine called local_file

# format of command is:
# transfer.download_file('name-of-space', 'folder_name'+"/"+'new-name-of-file', local file )

transfer.download_file(space_name, folder_name + "/"+ target_file_name, local_file_name )


