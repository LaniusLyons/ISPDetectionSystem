import json
import requests

# Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
webhook_url = 'https://requestb.in/vb7fvuvb'
slack_data = {'ts':'Testing Webhook'}


response = requests.post(
    webhook_url, data=slack_data,
    headers={'Content-Type': 'application/json'}
)
if response.status_code != 200:
    raise ValueError(
        'Request to slack returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )
else:
	print response.status_code
	print response.content
