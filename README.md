# myVisualPing (Version 1)
## Description
This is a simple script that will take a screenshot of a website and compare it to the previous screenshot. If there is a difference, it will send an email to the user with the screenshot attached. This is useful for monitoring websites for changes.
Currently, I used it to monitor the difference on the status of paper submission

## Running
To run this script, you will need to install the following dependencies:
* selenium
* loguru

You will also need to install a webdriver for your browser of choice. I have tested this script with Chrome and Firefox. You can find the Chrome webdriver [here](https://chromedriver.chromium.org/downloads) and the Firefox webdriver [here](https://github.com/mozilla/geckodriver/releases)

Once you have installed the dependencies and the webdriver, you can run the script with the following command:
```
python3 main.py
```

## Configuration
The script is configured using the config.json file. The following is an example of the config file:
```json
{
    "websiteCredentials": [
        {
            "username": "xxx@outlook.com",
            "password": "xxxxxxxxxxx",
            "url": "https://www.baidu.com"
        }
    ],
    "emailCredentials": [
        {
          "mail_host": "smtp.outlook.com",
          "mail_user": "xxx@outlook.com",
          "mail_auth": "XXXXXXXXXXXXXXXX"
        }
    ]
}
```
## Logging
The script uses the loguru library to log information. The log file is located in the logs folder. The log file is rotated every day and the old log files are deleted after 7 days.
The log file is stored in `log` folder. 

