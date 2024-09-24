# AWS CloudWatch Log Reader with Linux and Email Notifications

This Python script monitors AWS CloudWatch logs and sends notifications for CRITICAL, ERROR, and WARNING level log events. The notifications are sent using both the Linux notification system and a Google Apps Script Webhook (which can be configured to send email notifications).

## Features
- Retrieves the latest log events from a specified CloudWatch log group and stream
- Filters the log events to only include CRITICAL, ERROR, and WARNING level messages
- Sends notifications using the Linux notification system
- Sends notifications via email using a Google Apps Script Webhook
- Runs continuously in the background using a cron job

## Prerequisites
- Python 3.7 or later
- Access to an AWS account with CloudWatch logging enabled
- A Google Apps Script Webhook URL (optional, for email notifications)

## Installation
1. Clone the repository or download the `cloudwatch_log_reader.py` script.
2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project directory and add the following environment variables:
   ```
   AWS_REGION=your_aws_region
   AWS_ACCESS_KEY_ID=your_aws_access_key_id
   AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
   LOG_GROUP_NAME=your_cloudwatch_log_group_name
   LOG_STREAM_NAME=your_cloudwatch_log_stream_name
   NOTIFICATION_TITLE=New CloudWatch Log
   GOOGLE_APPS_SCRIPT_WEBHOOK=your_google_apps_script_webhook_url
   ```
   Replace the values with your actual AWS credentials, CloudWatch log group and stream names, and the Google Apps Script Webhook URL (if you want to enable email notifications).

## Usage
### Run the script manually
```
python cloudwatch_log_reader.py
```
The script will check the latest log events from the specified CloudWatch log group and stream, and send notifications for any CRITICAL, ERROR, or WARNING level logs.

### Run the script using a cron job
To run the script continuously in the background, you can use a cron job:
1. Open your system's crontab editor:
   ```
   crontab -e
   ```
2. Add the following line to the crontab file to run the script every 5 minutes:
   ```
   */5 * * * * /path/to/your/python /path/to/cloudwatch_log_reader.py
   ```
   Replace `/path/to/your/python` with the actual path to your Python interpreter, and `/path/to/cloudwatch_log_reader.py` with the actual path to the script file.
3. Save and exit the crontab editor.

Now, the `cloudwatch_log_reader.py` script will run every 5 minutes in the background, checking for new CRITICAL, ERROR, and WARNING level logs in CloudWatch and sending notifications using both the Linux notification system and the Google Apps Script Webhook (for email).

## Customization
- You can change the frequency of the cron job by updating the schedule expression in the crontab file.
- The `NOTIFICATION_TITLE` environment variable can be used to customize the title of the notifications.
- If you don't want to use the Google Apps Script Webhook for email notifications, simply leave the `GOOGLE_APPS_SCRIPT_WEBHOOK` environment variable unset.

## Dependencies
- `boto3`: AWS SDK for Python
- `python-dotenv`: Loads environment variables from a `.env` file
- `requests`: Used to send notifications via the Google Apps Script Webhook

## License
This project is licensed under the [MIT License](LICENSE).
