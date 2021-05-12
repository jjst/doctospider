# doctospider

Extracts vaccination availability from doctolib.fr. Sends an SMS with Twilio if appointments are available.

Feel free to use this if you find it useful, sorry for the lack of docs, this was thrown together in a few hours.

Run the script via:
```
python3 spider.py
```

I deploy it on AWS Lambda and trigger a run every 5 minutes via AWS EventBridge, but it can be deployed differently too. 
