# for running a headless webdriver
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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
from time import sleep
import json
import datetime

# SETUP
# -----------------------------------------------------------------------------
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--no-sandbox")  # Required for running as root in many cases
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional)
chrome_options.add_argument("--remote-debugging-port=9222")  # Enable debugging

# Set up ChromeDriver
service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

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


def get_html_from_url(driver, url, timeout=10):
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
        return page_html
    except Exception as e:
        # Return the error if any
        return f"Error: {str(e)}"


def write_soup_to_file(soup, file_name):
    with open('html_captures/' + file_name, "w") as f:
        f.write(soup.prettify())


def write_html_to_file(html, file_name):
    with open('html_captures/' + file_name, "w") as f:
        f.write(html)


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


def check_listing_activity(soup):
    # Check if the listing is as expected
    if soup.find("span", attrs={"class": "postingtitletext"}) is not None:
        return {'is_expected': True, 'activity': 'listing as expected'}

    # Check if the listing has been removed by the author
    if 'this posting has been deleted by its author' in soup.get_text().lower():
        return {'is_expected': False, 'activity': 'removed by author'}

    # Check if the listing has been flagged
    elif 'this posting has been flagged for removal' in soup.get_text().lower():
        return {'is_expected': False, 'activity': 'listing flagged'}

    # Check if the listing has 404'd
    elif '404 error' in soup.get_text().lower():
        return {'is_expected': False, 'activity': 'listing 404'}

    # Check if the listing has expired
    if 'this posting has expired' in soup.get_text().lower():
        return {'is_expected': False, 'activity': 'expired'}

    # If none of the above cases match
    return {'is_expected': False, 'activity': 'unknown'}


def soup_from_html(page_html):
    # Create BeautifulSoup soup object
    soup = BeautifulSoup(page_html, 'html.parser')
    return soup


def query_dynamodb(area_value):
    # Query the DynamoDB table for items with a specific area and filter by activity
    response = table.query(
        KeyConditionExpression=Key('area').eq(area_value),
        FilterExpression=Attr('activity').eq('active')
    )

    items = response.get('Items', [])

    # Process the results
    result_dict = {}
    for item in items:
        url = item.get('url')
        if url:  # Ensure that 'url' is present in the item
            result_dict[url] = {
                'activity': item.get('activity'),
                'listing_html': item.get('listing_html'),
                'updated': item.get('updated')
            }

    return result_dict


def process_frontpage(area, driver, get_soup_from_url, extract_frontpage_links, get_html_from_url, soup_from_html, check_listing_activity):
    # Fetch the front page soup from the URL
    frontpage_soup = get_soup_from_url(
        driver,
        f'https://{area}.craigslist.org/search/cta?purveyor=owner#search=1~gallery~0~0'
    )

    # Why do you break on dothan?
    print(f'https://{area}.craigslist.org/search/cta?purveyor=owner#search=1~gallery~0~0')

    # Extract links from the front page
    links = extract_frontpage_links(frontpage_soup)

    new_listings_count = 0

    for i, link in enumerate(links, start=1):
        print('Processing frontpage: ', area)
        print('link: ', link)
        print(i, ' of ', len(links))
        # Get HTML content from the link
        link_html = get_html_from_url(driver, link)

        # Check listing activity
        listing_activity = check_listing_activity(soup_from_html(link_html))

        if listing_activity['is_expected']:
            # Insert new item into DynamoDB
            table.put_item(
                Item={
                    'area': area,  # primary key (partition key)
                    'url': link,  # Sort key
                    'added': datetime.datetime.now().isoformat(),  # Convert to ISO 8601 string
                    'activity': 'active',
                    'updated': datetime.datetime.now().isoformat(),  # Convert to ISO 8601 string
                    'listing_html': link_html
                }
            )
            new_listings_count += 1

    return {'new_listings_added': new_listings_count}


def update_existing_listings(existing_listings, area, driver, get_html_from_url, soup_from_html, check_listing_activity):
    listings_updated_count = 0
    listings_checked_count = 0

    for i, link in enumerate(existing_listings, start=1):
        print('Updating Existing: ', area)
        print('link: ', link)
        print(i, ' of ', len(existing_listings))
        # Get HTML content from the link
        link_html = get_html_from_url(driver, link)

        # Check listing activity
        listing_activity = check_listing_activity(soup_from_html(link_html))

        listings_checked_count += 1

        if not listing_activity['is_expected']:
            # Update existing item in DynamoDB
            table.update_item(
                Key={"area": area, "url": link},
                UpdateExpression="set activity=:s, updated=:u",
                ExpressionAttributeValues={
                    ":s": listing_activity['activity'],
                    ":u": datetime.datetime.now().isoformat()
                },
                ReturnValues="UPDATED_NEW"
            )
            listings_updated_count += 1

    return {
        'listings_updated': listings_updated_count,
        'listings_checked': listings_checked_count
    }


# -----------------------------------------------------------------------------
# LOOP
# -----------------------------------------------------------------------------
# Prompt user for area set selection
# I think this is causeing bugs in 'expect' script print("Area sets 1-5 avaliable")

choice = input("Select an area set:")

if choice == '1':
    areas = areas1
elif choice == '2':
    areas = areas2
elif choice == '3':
    areas = areas3
elif choice == '4':
    areas = areas4
elif choice == '5':
    areas = areas5
else:
    print("Invalid choice. Defaulting to Set 1.")
    areas = areas1

startTime_of_country = datetime.datetime.now()

for area in areas:

    startTime_of_area = datetime.datetime.now()

    # Query the table
    existing_listings = query_dynamodb(area)

    # 1. Check existing listings
    updated = update_existing_listings(
        existing_listings,
        area,
        driver,
        get_html_from_url,
        soup_from_html,
        check_listing_activity
    )
    # 2. add anything from frontpage
    processed = process_frontpage(
        area,
        driver,
        get_soup_from_url,
        extract_frontpage_links,
        get_html_from_url,
        soup_from_html,
        check_listing_activity
    )

    endTime_of_area = datetime.datetime.now()

    # Calculate the time delta
    areaDeltaT = endTime_of_area - startTime_of_area

    # Send mail with formatted string
    send_mail(
        'douglasemckinley@gmail.com',
        'johnnygooddeals@gmail.com',
        'ec2 {area} finished, updated: {updated}, processed: {processed}, timeDelta: {areaDeltaT}'.format(
            area=area,
            updated=updated,
            processed=processed,
            areaDeltaT=areaDeltaT
        ),
        'ec2 {area} finished, updated: {updated}, processed: {processed}, timeDelta: {areaDeltaT}'.format(
            area=area,
            updated=updated,
            processed=processed,
            areaDeltaT=areaDeltaT
        )
    )

endTime_of_country = datetime.datetime.now()

driver.quit()

# Calculate the time delta
countryDeltaT = startTime_of_country - endTime_of_country

# Send mail with formatted string
send_mail(
    'douglasemckinley@gmail.com',
    'johnnygooddeals@gmail.com',
    'all areas finished, timeDelta: {countryDeltaT}'.format(
        countryDeltaT=countryDeltaT
    ),
    'all areas finished, timeDelta: {countryDeltaT}'.format(
        countryDeltaT=countryDeltaT
    )
)

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
