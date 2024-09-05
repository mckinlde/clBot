# for running a headless webdriver
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# for waiting for pages to render:
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# for writing to dynamoDB
import boto3
from boto3.dynamodb.conditions import Key
# for sending emails
import smtplib
from email.mime.text import MIMEText
# for parsing
from bs4 import BeautifulSoup
# general use
from time import sleep
import json
import datetime

# SETUP
# -----------------------------------------------------------------------------
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up ChromeDriver
service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Initialize a session using Amazon DynamoDB
session = boto3.Session(region_name='us-west-2')  # Replace with your region
dynamodb = session.resource('dynamodb')

# Select your DynamoDB table
table = dynamodb.Table('cars')  # Replace with your table name
# -----------------------------------------------------------------------------


# HELPER FUNCTIONS
# -----------------------------------------------------------------------------
def get_soup_from_url(driver, url, timeout=10):
    try:
        # Navigate to the specified URL
        driver.get(url)

        # Explicitly wait for an element to be present (you can adjust the condition based on your needs)
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

        sleep(3)
        # Get the HTML content after waiting
        page_html = driver.page_source
        # Create BeautifulSoup soup object
        soup = BeautifulSoup(page_html, 'html.parser')
        return soup
    except Exception as e:
        # Return the error if any
        return f"Error: {str(e)}"


def write_soup_to_file(soup, file_name):
    with open('html_captures/' + file_name, "w") as f:
        f.write(soup.prettify())


def extract_frontpage_links(bs4_object):
    links = []
    for link in bs4_object.find_all('a', class_='posting-title'):
        href = link.get('href')
        if href:
            links.append(href)
    return links


def send_mail(to, from_addr, subject, text):
    if not isinstance(text, str):
        # Convert the text to a string if it's not already
        text = str(text)
    msg = MIMEText(text)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to
    s = smtplib.SMTP_SSL("smtp.gmail.com")
    s.login('johnnygooddeals@gmail.com', 'vdzsukbhxjcqelej')
    # for Python 3
    s.send_message(msg)
    # OR
    # for Python 2 (or 3, will still work)
    # s.sendmail(from_addr, [to], msg.as_string())
    s.quit()

# -----------------------------------------------------------------------------

# LOOP
# -----------------------------------------------------------------------------

# Example of querying items
response = table.query(
    KeyConditionExpression=Key('url').eq('example')  # Replace with your key condition
)

items = response['Items']

for item in items:
    print(item)

frontpage_soup = get_soup_from_url(driver, 'https://seattle.craigslist.org/search/cta?purveyor=owner#search=1~gallery~0~0')
links = extract_frontpage_links(frontpage_soup)

i = 0
for link in links:
    sleep(1+random.randint(0,2))
    i=i+1
    print('link: ', link)
    print(i, ' out of ', len(links))
    table.put_item(
    Item={
        'url': link,  # primary key (partition key)
        'area': 'seattle', # Sort key
        'added': datetime.datetime.now().isoformat(),  # Convert to ISO 8601 string
        'status': 'active',
        'updated': datetime.datetime.now().isoformat(),  # Convert to ISO 8601 string
        'listing_html': driver.get(link)
    }
)

driver.quit()

send_mail('douglasemckinley@gmail.com', 'johnnygooddeals@gmail.com',
          'ec2 finished',
          'links checked: {length: .2f}'.format(length = len(links)))

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
