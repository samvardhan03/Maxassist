from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Authenticate with Google API credentials
creds = Credentials.from_authorized_user_info(info=...)
service = build('groupssettings', 'v1', credentials=creds)

# Retrieve group data
group = service.groups().get(groupUniqueId='your_group_id').execute()



