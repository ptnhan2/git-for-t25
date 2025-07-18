import os
from requests.auth import HTTPBasicAuth
# BASE_URL = "https://support.zendesk.com/api/v2/help_center/"
BASE_URL = "https://support.optisigns.com/api/v2/help_center/"
HEADERS = {
	"Content-Type": "application/json",
}
EMAIL_ADDRESS = ''
API_TOKEN = ''
AUTH = HTTPBasicAuth(f'{EMAIL_ADDRESS}/token', API_TOKEN)
