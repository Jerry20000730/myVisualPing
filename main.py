import json
import os
import smtplib
from email.mime.text import MIMEText

from selenium import webdriver
from selenium.webdriver.common.by import By
from loguru import logger
import datetime

logger.add("log/{}.log".format(datetime.datetime.now()), backtrace=True, diagnose=True)
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
        logger.log('INFO', 'config.json loaded.')
except FileNotFoundError:
    logger.exception('The file does not exist.')

def sendmail(to, mail_host, mail_auth, mail_user, send_name, title, content):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = send_name
    msg['To'] = to
    msg['Subject'] = title
    server = smtplib.SMTP(mail_host, 25)
    server.login(mail_user, mail_auth)
    server.sendmail(mail_user, to, msg.as_string())
    server.quit()


def emailReminder(desc_email, title, content) -> bool:
    try:
        sendmail(desc_email, config['emailCredentials'][0]['mail_host'], config['emailCredentials'][0]['mail_auth'], config['emailCredentials'][0]['mail_user'], config['emailCredentials'][0]['mail_user'], title, content)
    except Exception as e:
        logger.exception(e)
        return False
    return True


def updateStatus() -> str:
    try:
        driver = webdriver.Chrome()
        driver.get(config['websiteCredentials'][0]['url'])
        driver.maximize_window()
        driver.implicitly_wait(5)

        driver.switch_to.frame('content')
        driver.find_element(By.ID, 'username').send_keys(config['websiteCredentials'][0]['username'])
        driver.find_element(By.ID, 'passwordTextbox').send_keys(config['websiteCredentials'][0]['password'])
        driver.find_element(By.NAME, 'authorLogin').click()

        driver.switch_to.frame('content')
        driver.find_element(By.LINK_TEXT, 'Submissions Being Processed').click()

        td = driver.find_element(By.XPATH, '//*[@id="row1"]/td[7]')
        status = td.accessible_name
        logger.log('INFO', 'current status: {}'.format(status))
        if os.path.exists('status.txt'):
            logger.log('INFO', "The file \'status.txt\' already exists.")
        else:
            try:
                with open('status.txt', 'w') as file:
                    logger.log('INFO', "The file \'status.txt\' has been created.")
            except IOError as e:
                logger.exception('The file creation failed.')
        return status
    except Exception as e:
        logger.exception(e)
        emailReminder('tragicmaster@outlook.com', 'Error Detected', 'Dear Fangcheng,\n\nError Detected. Please check the log file \n\nBest Regards,\nMyVisualPing')
        return 'Error'


def getPreviousStatus() -> str:
    try:
        with open('status.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        logger.exception('The file does not exist.')


def compare(status, previousStatus):
    if status != previousStatus:
        r = emailReminder('tragicmaster@outlook.com', 'Status Changed',
                          'Dear Fangcheng,\n\n    Status on paper website has changed from \'{}\' to \'{}\'. \n\nBest Regards,\nMyVisualPing'.format(
                              previousStatus, status))
        if r:
            try:
                with open('status.txt', 'w') as f:
                    f.write(status)
            except FileNotFoundError:
                logger.exception('The file does not exist.')
        else:
            logger.log('INFO', 'Email send failed.')


if __name__ == '__main__':
    current_status = updateStatus()
    if current_status != 'Error':
        compare(current_status, getPreviousStatus())
