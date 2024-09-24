import os
from dotenv import load_dotenv
import boto3
from datetime import datetime, timedelta
import subprocess
import requests

load_dotenv()

# Load environment variables
AWS_REGION = os.getenv('AWS_REGION')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
LOG_GROUP_NAME = os.getenv('LOG_GROUP_NAME')
LOG_STREAM_NAME = os.getenv('LOG_STREAM_NAME')
NOTIFICATION_TITLE = os.getenv('NOTIFICATION_TITLE', 'New CloudWatch Log')
GOOGLE_APPS_SCRIPT_WEBHOOK = os.getenv('GOOGLE_APPS_SCRIPT_WEBHOOK')
NOTIFICATION_EMAIL = os.getenv('NOTIFICATION_EMAIL')

# Create CloudWatch client
cloudwatch = boto3.client('logs',
                         region_name=AWS_REGION,
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def get_latest_log_events():
    # Get the latest log events from the last 5 minutes
    start_time = int((datetime.now() - timedelta(minutes=5)).timestamp() * 1000)
    end_time = int(datetime.now().timestamp() * 1000)
    response = cloudwatch.get_log_events(
        logGroupName=LOG_GROUP_NAME,
        logStreamName=LOG_STREAM_NAME,
        startTime=start_time,
        endTime=end_time,
        limit=10
    )

    return [event for event in response['events'] if any(level in event['message'] for level in ['CRITICAL', 'ERROR', 'WARNING'])]

def send_notification(title, message):
    # Send a notification using the Linux notification system
    subprocess.run(['notify-send', title, message])

    # Send a notification via email using the Google Apps Script Webhook
    if GOOGLE_APPS_SCRIPT_WEBHOOK:
        print(f"sending notification via Google Apps Script Webhook: {NOTIFICATION_EMAIL}")
        try:
            data = {
                'recipient': NOTIFICATION_EMAIL,
                'subject': title,
                'message': message
            }
            requests.post(GOOGLE_APPS_SCRIPT_WEBHOOK, json=data)
        except requests.exceptions.RequestException as e:
            print(f"Error sending notification via Google Apps Script Webhook: {e}")

def main():
    if LOG_GROUP_NAME is None or LOG_STREAM_NAME is None or GOOGLE_APPS_SCRIPT_WEBHOOK is None:
        print("Error: LOG_GROUP_NAME, LOG_STREAM_NAME, or GOOGLE_APPS_SCRIPT_WEBHOOK environment variable is not set.")
        return
    latest_logs = get_latest_log_events()
    if latest_logs:
        for log_event in latest_logs:
            send_notification(NOTIFICATION_TITLE, log_event['message'])
        print('Notifications sent!')
    else:
        print('No new logs found.')

if __name__ == '__main__':
    main()