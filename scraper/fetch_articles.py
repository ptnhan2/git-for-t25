import requests
from requests.auth import HTTPBasicAuth

#url = "https://support.zendesk.com/api/v2/help_center/en-us/articles?sort_by=updated_at&sort_order=asc&start_time=1404345231"
url = "https://support.zendesk.com/api/v2/help_center/articles/4408883393818"

headers = {
	"Content-Type": "application/json",
}
email_address = 'your_email_address'
api_token = 'your_api_token'
# Use basic authentication
auth = HTTPBasicAuth(f'{email_address}/token', api_token)

response = requests.request(
	"GET",
	url,
	auth=auth,
	headers=headers
)

print(response.text)