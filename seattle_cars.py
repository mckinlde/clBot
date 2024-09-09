# for accepting command-line arguments
import sys
# for running a headless webdriver
import random

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# for waiting for pages to render:
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# for reading/writing to dynamoDB
import boto3
from boto3.dynamodb.conditions import Key, Attr
# for sending emails
import smtplib
from email.mime.text import MIMEText
# for parsing
from bs4 import BeautifulSoup
# general use
from time import sleep, time
import json
import datetime
import botocore

# SETUP
# -----------------------------------------------------------------------------
# Firefox setup for headless mode
firefox_options = Options()
firefox_options.add_argument("--headless")  # Run in headless mode
firefox_options.add_argument("--disable-gpu")  # Disable GPU acceleration
firefox_options.add_argument("--no-sandbox")  # Required for running as root
firefox_options.add_argument("--disable-software-rasterizer")

# Set up FirefoxDriver
print("Checking for geckodriver in /usr/local/bin")
service = Service("/usr/local/bin/geckodriver")  # Make sure geckodriver is installed and in this path
print("Initializing Firefox WebDriver...")
driver = webdriver.Firefox(service=service, options=firefox_options)
print("WebDriver initialized successfully!")


# After initializing the driver
print("Driver initialized...")

# Set a custom wait time
timeout = 30  # seconds

# Initialize a session using Amazon DynamoDB
session = boto3.Session(region_name='us-west-2')  # Replace with your region
dynamodb = session.resource('dynamodb')
# Select your DynamoDB table
table = dynamodb.Table('listings')  # Replace with your table name


# Set your CL area
areas1 = [
    "auburn", "bham", "dothan", "shoals", "gadsden", "huntsville", "mobile", "montgomery", "tuscaloosa",
    "anchorage", "fairbanks", "kenai", "juneau", "flagstaff", "mohave", "phoenix", "prescott", "showlow",
    "sierravista", "tucson", "yuma", "fayar", "fortsmith", "jonesboro", "littlerock", "texarkana",
    "bakersfield", "chico", "fresno", "goldcountry", "hanford", "humboldt", "imperial", "inlandempire",
    "losangeles", "mendocino", "merced", "modesto", "monterey", "orangecounty", "palmsprings", "redding",
    "sacramento", "sandiego", "sfbay", "slo", "santabarbara", "santamaria", "siskiyou", "stockton",
    "susanville", "ventura", "visalia", "yubasutter", "boulder", "cosprings", "denver", "eastco",
    "fortcollins", "rockies", "pueblo", "westslope", "newlondon", "hartford", "newhaven", "nwct",
    "delaware", "washingtondc", "miami", "daytona", "keys", "miami", "fortmyers", "gainesville", "cfl",
    "jacksonville", "lakeland", "miami", "lakecity", "ocala", "okaloosa", "orlando", "panamacity",
    "pensacola", "sarasota", "miami", "spacecoast", "staugustine", "tallahassee", "tampa", "treasure"
]
areas2 = [
    "miami", "albanyga", "athensga", "atlanta", "augusta", "brunswick", "columbusga", "macon", "nwga",
    "savannah", "statesboro", "valdosta", "honolulu", "boise", "eastidaho", "lewiston", "twinfalls",
    "bn", "chambana", "chicago", "decatur", "lasalle", "mattoon", "peoria", "rockford", "carbondale",
    "springfieldil", "quincy", "bloomington", "evansville", "fortwayne", "indianapolis", "kokomo",
    "tippecanoe", "muncie", "richmondin", "southbend", "terrehaute", "ames", "cedarrapids", "desmoines",
    "dubuque", "fortdodge", "iowacity", "masoncity", "quadcities", "siouxcity", "ottumwa", "waterloo",
    "lawrence", "ksu", "nwks", "salina", "seks", "swks", "topeka", "wichita", "bgky", "eastky",
    "lexington", "louisville", "owensboro", "westky", "batonrouge", "cenla", "houma", "lafayette",
    "lakecharles", "monroe", "neworleans", "shreveport", "maine", "annapolis", "baltimore", "easternshore",
    "frederick", "smd", "westmd", "boston", "capecod", "southcoast", "westernmass", "worcester",
    "annarbor", "battlecreek", "centralmich", "detroit", "flint", "grandrapids", "holland", "jxn"
]
areas3 = [
    "kalamazoo", "lansing", "monroemi", "muskegon", "nmi", "porthuron", "saginaw", "swmi", "thumb", "up",
    "bemidji", "brainerd", "duluth", "mankato", "minneapolis", "rmn", "marshall", "stcloud", "gulfport",
    "hattiesburg", "jackson", "meridian", "northmiss", "natchez", "columbiamo", "joplin", "kansascity",
    "kirksville", "loz", "semo", "springfield", "stjoseph", "stlouis", "billings", "bozeman", "butte",
    "greatfalls", "helena", "kalispell", "missoula", "montana", "grandisland", "lincoln", "northplatte",
    "omaha", "scottsbluff", "elko", "lasvegas", "reno", "nh", "cnj", "jerseyshore", "newjersey",
    "southjersey", "albuquerque", "clovis", "farmington", "lascruces", "roswell", "santafe", "albany",
    "binghamton", "buffalo", "catskills", "chautauqua", "elmira", "fingerlakes", "glensfalls",
    "hudsonvalley", "ithaca", "longisland", "newyork", "oneonta", "plattsburgh", "potsdam", "rochester",
    "syracuse", "twintiers", "utica", "watertown", "asheville", "boone", "charlotte", "eastnc"
]
areas4 = [
    "fayetteville", "greensboro", "hickory", "onslow", "outerbanks", "raleigh", "wilmington",
    "winstonsalem", "bismarck", "fargo", "grandforks", "nd", "akroncanton", "ashtabula", "athensohio",
    "chillicothe", "cincinnati", "cleveland", "columbus", "dayton", "limaohio", "mansfield", "sandusky",
    "toledo", "tuscarawas", "youngstown", "zanesville", "lawton", "enid", "oklahomacity", "stillwater",
    "tulsa", "bend", "corvallis", "eastoregon", "eugene", "klamath", "medford", "oregoncoast", "portland",
    "roseburg", "salem", "altoona", "chambersburg", "erie", "harrisburg", "lancaster", "allentown",
    "meadville", "philadelphia", "pittsburgh", "poconos", "reading", "scranton", "pennstate",
    "williamsport", "york", "providence", "charleston", "columbia", "florencesc", "greenville",
    "hiltonhead", "myrtlebeach", "nesd", "csd", "rapidcity", "siouxfalls", "sd", "chattanooga",
    "clarksville", "cookeville", "jacksontn", "knoxville", "memphis", "nashville", "tricities"
]
areas5 = [
    "abilene", "amarillo", "austin", "beaumont", "brownsville", "collegestation", "corpuschristi",
    "dallas", "nacogdoches", "delrio", "elpaso", "galveston", "houston", "killeen", "laredo",
    "lubbock", "mcallen", "odessa", "sanangelo", "sanantonio", "sanmarcos", "bigbend", "texoma",
    "easttexas", "victoriatx", "waco", "wichitafalls", "logan", "ogden", "provo", "saltlakecity",
    "stgeorge", "vermont", "charlottesville", "danville", "fredericksburg", "norfolk", "harrisonburg",
    "lynchburg", "blacksburg", "richmond", "roanoke", "swva", "winchester", "bellingham", "kpr",
    "moseslake", "olympic", "pullman", "seattle", "skagit", "spokane", "wenatchee", "yakima",
    "charlestonwv", "martinsburg", "huntington", "morgantown", "wheeling", "parkersburg", "swv", "wv",
    "appleton", "eauclaire", "greenbay", "janesville", "racine", "lacrosse", "madison", "milwaukee",
    "northernwi", "sheboygan", "wausau", "wyoming", "micronesia", "puertorico", "virgin"
]

# HELPER FUNCTIONS
# -----------------------------------------------------------------------------
def initialize_driver():
    """
    Initializes a new Firefox WebDriver instance.
    """
    print("Initializing Firefox WebDriver...")
    firefox_options = Options()
    firefox_options.add_argument("--headless")  # Run in headless mode
    firefox_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    firefox_options.add_argument("--no-sandbox")  # Required for running as root
    firefox_options.add_argument("--disable-software-rasterizer")

    service = Service("/usr/local/bin/geckodriver")  # Ensure geckodriver is installed in this path
    driver = webdriver.Firefox(service=service, options=firefox_options)
    print("WebDriver initialized successfully!")
    return driver

def exponential_backoff_retry(func, retries=5, delay=2, *args, **kwargs):
    """
    Implements exponential backoff for retrying a function call.
    """
    for attempt in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            if attempt < retries - 1:
                backoff = delay * (2 ** attempt) + random.uniform(0, 1)
                print(f"Retrying in {backoff:.2f} seconds...")
                sleep(backoff)
            else:
                print(f"Max retries reached. Skipping...")
                return None

def get_soup_from_url(driver, url, timeout=10):
    """
    Fetch the HTML from a given URL and return a BeautifulSoup object.
    """
    try:
        driver.get(url)
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        return BeautifulSoup(driver.page_source, 'html.parser')
    except Exception as e:
        return f"Error: {str(e)}"

def get_html_from_url(driver, url, timeout=10):
    """
    Fetch the raw HTML from a given URL.
    """
    try:
        driver.get(url)
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        sleep(3)
        return driver.page_source
    except Exception as e:
        return f"Error: {str(e)}"

def safe_put_item(item, retries=5, delay=2):
    """
    Perform a DynamoDB put_item operation with retry and exponential backoff.
    """
    for attempt in range(retries):
        try:
            table.put_item(Item=item)
            return True
        except botocore.exceptions.ProvisionedThroughputExceededException as e:
            print(f"Provisioned throughput exceeded on attempt {attempt + 1}: {e}")
            if attempt < retries - 1:
                backoff = delay * (2 ** attempt) + random.uniform(0, 1)
                print(f"Retrying after {backoff:.2f} seconds...")
                sleep(backoff)
            else:
                print("Max retries reached. Skipping this item.")
                send_mail('Provisioning Alert', f"Failed to put item: {item['url']}")
                return False

def extract_frontpage_links(bs4_object):
    """
    Extract listing links from a Craigslist page.
    """
    links = []
    try:
        for link in bs4_object.find_all('a', class_='posting-title'):
            href = link.get('href')
            if href:
                links.append(href)
    except AttributeError:
        print("Error: Invalid BeautifulSoup object.")
    return links

def send_mail(subject, text):
    """
    Sends an email notification when required.
    """
    to = 'douglasemckinley@gmail.com'
    from_addr = 'johnnygooddeals@gmail.com'
    msg = MIMEText(text)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to

    try:
        s = smtplib.SMTP_SSL("smtp.gmail.com")
        s.login('johnnygooddeals@gmail.com', 'vdzsukbhxjcqelej')
        s.send_message(msg)
        s.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_listing_activity(soup):
    """
    Determine the current status of a listing by examining its HTML content.
    """
    try:
        if soup.find("span", attrs={"class": "postingtitletext"}) is not None:
            return {'is_expected': True, 'activity': 'listing as expected'}

        if 'this posting has been deleted by its author' in soup.get_text().lower():
            return {'is_expected': False, 'activity': 'removed by author'}

        if 'this posting has been flagged for removal' in soup.get_text().lower():
            return {'is_expected': False, 'activity': 'listing flagged'}

        if '404 error' in soup.get_text().lower():
            return {'is_expected': False, 'activity': 'listing 404'}

        if 'this posting has expired' in soup.get_text().lower():
            return {'is_expected': False, 'activity': 'expired'}

    except Exception as e:
        print(f"Error checking listing activity: {e}")
        return {'is_expected': False, 'activity': 'unknown'}
    
    return {'is_expected': False, 'activity': 'unknown'}

def query_dynamodb(area_value):
    """
    Query the DynamoDB table for active listings in a specific area.
    """
    response = table.query(
        KeyConditionExpression=Key('area').eq(area_value),
        FilterExpression=Attr('activity').eq('active')
    )

    items = response.get('Items', [])
    result_dict = {}

    for item in items:
        url = item.get('url')
        if url:
            result_dict[url] = {
                'activity': item.get('activity'),
                'listing_html': item.get('listing_html'),
                'updated': item.get('updated')
            }

    return result_dict

def process_frontpage(area, driver):
    """
    Process the front page of Craigslist listings for a specific area.
    """
    print(f'Processing frontpage for {area}')
    frontpage_soup = exponential_backoff_retry(get_soup_from_url, driver=driver, url=f'https://{area}.craigslist.org/search/cta?purveyor=owner#search=1~gallery~0~0')

    if not frontpage_soup:
        print(f"Failed to load frontpage for {area}")
        return

    links = extract_frontpage_links(frontpage_soup)
    new_listings_count = 0

    for i, link in enumerate(links, start=1):
        print(f'Processing link {i}/{len(links)} for {area}: {link}')
        link_html = exponential_backoff_retry(get_html_from_url, driver=driver, url=link)
        if link_html:
            listing_activity = check_listing_activity(BeautifulSoup(link_html, 'html.parser'))

            if listing_activity['is_expected']:
                new_listings_count += safe_put_item({
                    'area': area,
                    'url': link,
                    'added': datetime.datetime.now().isoformat(),
                    'activity': 'active',
                    'updated': datetime.datetime.now().isoformat(),
                    'listing_html': link_html
                })

    return {'new_listings_added': new_listings_count}

def update_existing_listings(existing_listings, area, driver):
    """
    Update the listings from a specific Craigslist area.
    """
    listings_updated_count = 0
    listings_checked_count = 0

    for i, link in enumerate(existing_listings, start=1):
        print(f'Updating existing listing {i}/{len(existing_listings)} for {area}: {link}')
        link_html = exponential_backoff_retry(get_html_from_url, driver=driver, url=link)

        if link_html:
            listing_activity = check_listing_activity(BeautifulSoup(link_html, 'html.parser'))
            listings_checked_count += 1

            if not listing_activity['is_expected']:
                # Update existing item in DynamoDB
                safe_put_item({
                    'area': area,
                    'url': link,
                    'updated': datetime.datetime.now().isoformat(),
                    'activity': listing_activity['activity'],
                    'listing_html': link_html
                })
                listings_updated_count += 1

    return {
        'listings_updated': listings_updated_count,
        'listings_checked': listings_checked_count
    }


# MAIN EXECUTION
# -----------------------------------------------------------------------------
# Accept area set as a command-line argument
if len(sys.argv) > 1:
    choice = sys.argv[1]
else:
    choice = input("Select an area set:")

# Define the areas to process
areas = {
    '1': areas1,
    '2': areas2,
    '3': areas3,
    '4': areas4,
    '5': areas5
}.get(choice, areas1)
startTime_of_country = datetime.datetime.now()

for area in areas:
    startTime_of_area = datetime.datetime.now()

    # Initialize driver for each area
    driver = initialize_driver()

    # Query the table
    existing_listings = query_dynamodb(area)

    # 1. Check existing listings
    updated = update_existing_listings(existing_listings, area, driver)

    # 2. Process new listings from front page
    processed = process_frontpage(area, driver)

    # Quit driver and wait before proceeding to next area
    driver.quit()
    print(f"Driver quit. Waiting 30 seconds before processing the next area...")
    sleep(30)

    endTime_of_area = datetime.datetime.now()
    areaDeltaT = endTime_of_area - startTime_of_area

    send_mail(
        subject=f'EC2 {area} finished',
        text=f'EC2 {area} finished, updated: {updated}, processed: {processed}, timeDelta: {areaDeltaT}'
    )

# Final processing
endTime_of_country = datetime.datetime.now()
countryDeltaT = endTime_of_country - startTime_of_country

send_mail(
    subject='All areas finished',
    text=f'All areas finished, timeDelta: {countryDeltaT}'
)
