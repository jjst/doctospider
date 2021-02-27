from spider import fetch_appointments


def lambda_handler(event, context):
    fetch_appointments()
