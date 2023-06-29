import boto3
from boto3 import session
from botocore.client import Config
from boto3.s3.transfer import S3Transfer

#Use the API Keys you generated at Digital Ocean
ACCESS_ID = 'UUH7GLM5ZV6SHQMP5R6K'
SECRET_KEY = '7qnpyCteMYe3O+hW7wDQATlWD072bRRauHZacGhfBjw'

#enter filename to be uploaded
source_file_name = 'txns_4x_3GB_blocks.tar'
target_file_name = 'txns_4x_3GB_blocks.tar' #change if file name on space is to be different

#source_folder = '/mnt/volume_lon1_49/txn_test_data'

space_name = 'nft-testdata02'
folder_name = 'TN/txns'

# Initiate session
session = session.Session()
client = session.client('s3',
                                region_name='fra1', #enter your own region_name
                                endpoint_url='https://nft-testdata02.fra1.digitaloceanspaces.com', #enter your own endpoint url

                                aws_access_key_id=ACCESS_ID,
                                aws_secret_access_key=SECRET_KEY)

transfer = S3Transfer(client)

# Uploads a file called 'name-of-file' to your Space called 'name-of-space'
# Creates a new-folder and the file's final name is defined as 'name-of-file'

# format of command is:
# transfer.upload_file('name-of-file', 'name-of-space', 'new-folder'+"/"+'new-name-of-file')

transfer.upload_file(source_file_name, space_name, folder_name + "/"+ target_file_name)


#This makes the file you are have specifically uploaded public by default.

# format is:
# response = client.put_object_acl(ACL='public-read', Bucket='name-of-space', Key="%s/%s" % ('new-folder', 'new-name-of-file'))

response = client.put_object_acl(ACL='public-read', Bucket=space_name, Key="%s/%s" % (folder_name, target_file_name))

