# clBot

# 1. Background
How to know a good deal when you see one? Look at a lot of them.

You can read about why this is a bad idea [here](https://singlepaynews.com/feed/1431) 

But apparently I just can't help myself. ((Note from the future: skip to step 7 if you're using this as a boilerplate; we setup with firefox/geckdriver now and have shell scripts for everything from installing stuff to creating cronjobs))

# 2. Launching an ec2 from the aws web console
First, I launch an ec2 instance.  I use:
- a new .pem file that is saved to my local machine's downloads folder
- default security group for the VPC
- and add the security group that allows me to ssh from home.

Yes I have to set these, 'default' behavior is to create a new security group without VPC or ssh access.

Then I connect to it from my local terminal:

tbh, it's easier to do this via [ec2 web console](https://us-west-2.console.aws.amazon.com/ec2/home). 


```cd /Users/douglasmckinley/Downloads/```

```chmod 400 "MyRobot.pem"```

> ssh -i "MyRobot.pem" {Public IPv4 DNS}

```ssh -i "MyRobot.pem" ec2-user@ec2-52-32-86-217.us-west-2.compute.amazonaws.com```


I can also use scp to transfer files

```scp -i "MyRobot.pem" filename-to-transfer-from-local ec2-user@ec2-52-32-86-217.us-west-2.compute.amazonaws.com```

Okay but finally I am ssh'd in to the ec2 instance.

# 3. Configuring the EC2 with git (from a ssh'd terminal window)

Now we're ready to pull our git repo and start making things repeatable with shell scripts.

I've kinda moved past this step, but [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account?platform=linux&tool=webui) are the [links](https://github.com/settings/keys) for configuring GitHub ssh keys

```
#!/bin/bash

# Update the package list and install Git
sudo yum update -y
sudo yum install git -y

# Verify Git installation
git --version

# Configure Git
git config --global user.name "mckinlde"
git config --global user.email "douglas.e.mckinley@gmail.com"

# Generate SSH key for GitHub
ssh-keygen -t ed25519 -C "douglas.e.mckinley@gmail.com" -f ~/.ssh/id_ed25519 -N ""

# Add the generated SSH key to the authorized keys
cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys

# Display the SSH key so you can add it to GitHub
echo "Your new SSH key (copy this to GitHub):"
cat ~/.ssh/id_ed25519.pub

# Clone the GitHub repository
git clone git@github.com:mckinlde/clBot.git
```

And finally it's time to use the setup_selenium.sh script 

```
# Navigate to the directory containing the script
cd ~/clBot

# make it executable
chmod +x setup_selenium.sh

# run the script
./setup_selenium.sh
```

That script will create a file 'selenium_test.py', and we can run it to check that everything worked correctly:

```python3 selenium_test.py```

The expected output is:

> Google


Sick.  Measurable progress.  Now I can run headless chrome/selenium from an ec2, and I just need a script that gets what I want from the web and saves it to dynamo.

The script I have now running locally uses a sql table and runs with a browser window, so it's not completely useless but needs to change a lot.

I think chatGPT can make the existing script run headlessly; so I'm going to focus on getting this ec2 to write to a dynamoDB table so that I have it ready to go.


# 4. Creating a DymanoDB table

I use the [DynamoDB console](https://us-west-2.console.aws.amazon.com/dynamodbv2/home?region=us-west-2#create-table) to create a table named 'cars' with Partition Key 'url' and Sort Key 'area'

I may have my keys backwards but who cares I'll make a new one.

I try to use a .py file, and then a command line, and neither work.  Apparently I first need to configure credentials, so in aws command line:

```aws configure```

And then input to prompts:

```
AWS Access Key ID [None]: -snip-
AWS Secret Access Key [None]: -snip-
Default region name [None]: us-west-2
Default output format [None]: 
```

Finally, this command-line putItem works:

```
aws dynamodb put-item \
    --table-name cars  \
    --item \
        '{"url": {"S": "No One You Know"}, "area": {"S": "Call Me Today"}, "AlbumTitle": {"S": "Somewhat Famous"}, "Awards": {"N": "1"}}'
```

ChatGPT says I need to do these things to get setup:

1. Install Boto3

```pip3 install boto3```

2. Configure AWS Credentials

I should be using IAM roles, but I've already setup with aws config.  I'll copy the IAM instructions here for future reference:
```
If your EC2 instance has an IAM role with the necessary permissions to access DynamoDB, you don’t need to manually configure credentials. Ensure that your IAM role has policies like AmazonDynamoDBFullAccess or more specific permissions if required.

Attach an IAM Role to your EC2 instance:
Go to the AWS Management Console.
Navigate to EC2.
Select your instance.
Click on "Actions" -> "Security" -> "Modify IAM role".
Attach a role that has DynamoDB access.
```

3. use a python script

Sick, it worked.  All I was missing was boto3, and I added that to setup_selenium.sh for redundancy

Now I'm ready to make da scraper.

# 5. Scraping the web

seattle_cars.py should be renamed, because it currently check all areas of craigslist, following this logic:

1. get all the listings from this area that are still active
    2. check to see if they should be updated, update if so
3. get all the listings from this area's frontpage
    4. check to see if they should be updated (should always pass, unless something is already a scam or whatever)
    5. add them to dynamo

There are 420 areas of CL, and at most 120 links from each frontpage, and I sleep 3 seconds for each driver.get()

420(areas) * 120(links) * 3(sec) / 3600(sec/hour) = 42 hours to read the country

Which brings us to

# 6. Scaling

I got this error from the script running on ec2:
```
raise error_class(parsed_response, operation_name)
botocore.errorfactory.ProvisionedThroughputExceededException: An error occurred (ProvisionedThroughputExceededException) when calling the PutItem operation (reached max retries: 9): The level of configured provisioned throughput for the table was exceeded. Consider increasing your provisioning level with the UpdateTable API.
```

I thought I was gonna do stuff to set up autoscaling, but turns out it's out-of-the-box with dynamoDB since 2017, so I just used console to set a higher maximum

The remaining meaningful way to scale is to have more EC2s that check CL.  That way I can check fewer areas, and have a faster than 42 hours turnaround.

Turns out that's also pretty simple, just create new ec2's and repeat the steps so far.  I've since added to the seattle_cars.py script to split the list of areas up and make them selectable.  After trying that out for a day I've moved on to running them automatically with chron, and you can check [running automagically with chronjobs.md](https://github.com/mckinlde/clBot/blob/main/running%20automagically%20with%20chronjobs.md) for instructions on setting that up as well.

From here I think I'm basically done with the scraping side, and this repo as of now is a pretty great boilerplate for setting up ec2s that talk to a dynamoDB and do things automatically with chron; which is not a useless thing.

Future work will be:
1. getting data from dynamoDB into a structured RDBMS so that I can surface a fancy dashboard (probably in a new repo)
2. training a classifier to predict which new listings are good deals that sell fast (probably also in a new repo, but maybe the same as #1)
3. setting up an email alert for those listings (probably back in this repo by editing seattle_cars.py)
4. setting up a website where you can pay to sign up for email alerts in your area (though everyone seems to ask about specific car models, so maybe I sell that instead)
5. selling access to the dashboard / the raw data itself to KBB?  who knows

# 7. Maintenance

Everything has broken.  Chrome will no longer launch, and I have switched to geckodriver.  I still want this repo to be boilerplate, so here is the usage:

To ensure that both `update_cronjob.sh` and `run_seattle_cars.sh` work seamlessly together, a few adjustments are necessary. Here’s a breakdown of the necessary changes and the reasoning behind them:

### Usage of Repo from fresh ec2:

- First, run setup_git.sh, then pull this repo.

- Then, run setup_selenium.sh and setup_firefox_and_geckodriver.sh; these should just be installing stuff

- Now, run update_cronjob.sh to make a cronjob that will use run_seattle_cars.sh to run seattle_cars.py with a given area selected.  

### Key Changes:
- The *update_cronjob.sh* script now takes three arguments:
  - `AREA_SET`: The area set number (e.g., `1`, `2`, etc.).
  - `HOUR`: The hour (in 24-hour format) when you want the cron job to run (e.g., `0` for midnight, `12` for noon).
  - `MINUTE`: The minute when you want the cron job to run (e.g., `7`, `12`, etc.).

### Example Usage of update_cronjob.sh after installing dependencies:

To set the cron job to run at **12:07 AM** every day for area set `1`, you would run:

```bash
./update_cronjob.sh 1 0 7
```

This would schedule the job to run at 00:07 every day with area set `1`.

For **12:12 PM** and area set `3`, you would run:

```bash
./update_cronjob.sh 3 12 12
```

This flexibility allows you to run the cron jobs at specific times with minimal effort.


# // ----------------------------------------------------------------------

# Copypasta for updating old ec2s that already have a :

```
cd clBot/
git pull origin main
cd ../
chmod +x ~/clBot/setup_firefox_and_geckodriver.sh
./clBot/setup_firefox_and_geckodriver.sh
chmod +x ~/clBot/update_cronjob.sh
./clBot/update_cronjob.sh
```
