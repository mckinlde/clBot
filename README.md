# clBot

# 1. Background
How to know a good deal when you see one? Look at a lot of them.

You can read about why this is a bad idea [here](https://singlepaynews.com/feed/1431) 

But apparently I just can't help myself.

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

Ideally these ec2s have different IPs as well, so CL doesn't get upset.

Here's what I think I should do:
1. create a new ec2 with the console
2. follow this repo's setup notes (README.md, setup_git.sh, setup_selenium.sh) to prep for a scraper
3. run a duplicate seattle_cars.py from the new ec2 instance (dividing the area = [] list between them)

Intuitively 1 more instance means 2x as much scraping, or 21 hours to get the full country

I want to assume they operate from different IPs, but I'm not sure

So while I go take a break, the thing to google is "IP of different ec2 instances in the same VPC"

# // ------------------------------------------------------------------------------------------

First, I set up a VPC endpoint bc I assume I need that.

https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/vpc-endpoints-dynamodb.html#vpc-endpoints-dynamodb-tutorial.configure-ec2-instance

But honestly idk that I do--so now I'm Googling 'insert to dynamoDB from EC2'.

https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/getting-started-step-2.html


// -------------------------------------------------------------------------------

//  I set up a VPC endpoint bc I assume I need that

// -------------------------------------------------------------------------------

https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/vpc-endpoints-dynamodb.html#vpc-endpoints-dynamodb-tutorial.configure-ec2-instance

cd /Users/douglasmckinley/Downloads/

chmod 400 "Jenkins.pem"

ssh -i "Jenkins.pem" ec2-user@ec2-54-149-50-230.us-west-2.compute.amazonaws.com

AWS Access Key ID [None]: -
AWS Secret Access Key [None]: -
Default region name [None]: us-west-2
Default output format [None]: 

{
    "Vpcs": [
        {
            "CidrBlock": "172.31.0.0/16",
            "DhcpOptionsId": "dopt-0b791ddfb87131b3a",
            "State": "available",
            "VpcId": "vpc-07012e5dc59bf9c6b",
            "OwnerId": "300293106161",
            "InstanceTenancy": "default",
            "CidrBlockAssociationSet": [
                {
                    "AssociationId": "vpc-cidr-assoc-04a455e6cdb0cbaa2",
                    "CidrBlock": "172.31.0.0/16",
                    "CidrBlockState": {
                        "State": "associated"
                    }
                }
            ],
            "IsDefault": true
        }
    ]
}

// --------------------------------------------------------------------------
//  Looking stuff up
// --------------------------------------------------------------------------

[ec2-user@ip-172-31-19-249 ~]$ aws ec2 describe-vpcs
{
    "Vpcs": [
        {
            "CidrBlock": "172.31.0.0/16",
            "DhcpOptionsId": "dopt-0b791ddfb87131b3a",
            "State": "available",
            "VpcId": "vpc-07012e5dc59bf9c6b",
            "OwnerId": "300293106161",
            "InstanceTenancy": "default",
            "CidrBlockAssociationSet": [
                {
                    "AssociationId": "vpc-cidr-assoc-04a455e6cdb0cbaa2",
                    "CidrBlock": "172.31.0.0/16",
                    "CidrBlockState": {
                        "State": "associated"
                    }
                }
            ],
            "IsDefault": true
        }
    ]
}


[ec2-user@ip-172-31-19-249 ~]$ aws ec2 describe-vpc-endpoint-services
        {
            "ServiceName": "com.amazonaws.us-west-2.dynamodb",
            "ServiceId": "vpce-svc-082c36eceb23cc4e9",
            "ServiceType": [
                {
                    "ServiceType": "Interface"
                }
            ],
            "AvailabilityZones": [
                "us-west-2a",
                "us-west-2b",
                "us-west-2c",
                "us-west-2d"
            ],
            "Owner": "amazon",
            "BaseEndpointDnsNames": [
                "dynamodb.us-west-2.vpce.amazonaws.com"
            ],
            "VpcEndpointPolicySupported": true,
            "AcceptanceRequired": false,
            "ManagesVpcEndpoints": false,
            "Tags": [],
            "SupportedIpAddressTypes": [
                "ipv4"
            ]
        },
        {
            "ServiceName": "com.amazonaws.us-west-2.dynamodb",
            "ServiceId": "vpce-svc-06e332dbde3b83af2",
            "ServiceType": [
                {
                    "ServiceType": "Gateway"
                }
            ],
            "AvailabilityZones": [
                "us-west-2a",
                "us-west-2b",
                "us-west-2c",
                "us-west-2d"
            ],
            "Owner": "amazon",
            "BaseEndpointDnsNames": [
                "dynamodb.us-west-2.amazonaws.com"
            ],
            "VpcEndpointPolicySupported": true,
            "AcceptanceRequired": false,
            "ManagesVpcEndpoints": false,
            "Tags": [],
            "SupportedIpAddressTypes": [
                "ipv4"
            ]
        },



[ec2-user@ip-172-31-19-249 ~]$ aws ec2 describe-route-tables
{
    "RouteTables": [
        {
            "Associations": [
                {
                    "Main": true,
                    "RouteTableAssociationId": "rtbassoc-0275dee2c0f172954",
                    "RouteTableId": "rtb-0fd40fc791b04b612",
                    "AssociationState": {
                        "State": "associated"
                    }
                }
            ],
            "PropagatingVgws": [],
            "RouteTableId": "rtb-0fd40fc791b04b612",
            "Routes": [
                {
                    "DestinationCidrBlock": "172.31.0.0/16",
                    "GatewayId": "local",
                    "Origin": "CreateRouteTable",
                    "State": "active"
                },
                {
                    "DestinationCidrBlock": "0.0.0.0/0",
                    "GatewayId": "igw-06ea5d8f86b334527",
                    "Origin": "CreateRoute",
                    "State": "active"
                }
            ],
            "Tags": [],
            "VpcId": "vpc-07012e5dc59bf9c6b",
            "OwnerId": "300293106161"
        }
    ]
// --------------------------------------------------------------------------
//  End of "Looking stuff up"
// --------------------------------------------------------------------------




aws ec2 create-vpc-endpoint --vpc-id vpc-07012e5dc59bf9c6b --service-name com.amazonaws.us-west-2.dynamodb --route-table-ids rtb-0fd40fc791b04b612

rtb-0fd40fc791b04b612
vpc-07012e5dc59bf9c6b

[ec2-user@ip-172-31-19-249 ~]$ aws ec2 create-vpc-endpoint --vpc-id vpc-07012e5dc59bf9c6b --service-name com.amazonaws.us-west-2.dynamodb --route-table-ids rtb-0fd40fc791b04b612
{
    "VpcEndpoint": {
        "VpcEndpointId": "vpce-0f6ae454a8f27593b",
        "VpcEndpointType": "Gateway",
        "VpcId": "vpc-07012e5dc59bf9c6b",
        "ServiceName": "com.amazonaws.us-west-2.dynamodb",
        "State": "available",
        "PolicyDocument": "{\"Version\":\"2008-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":\"*\",\"Action\":\"*\",\"Resource\":\"*\"}]}",
        "RouteTableIds": [
            "rtb-0fd40fc791b04b612"
        ],
        "SubnetIds": [],
        "Groups": [],
        "PrivateDnsEnabled": false,
        "RequesterManaged": false,
        "NetworkInterfaceIds": [],
        "DnsEntries": [],
        "CreationTimestamp": "2024-09-04T16:53:04+00:00",
        "OwnerId": "300293106161"
    }
}
[ec2-user@ip-172-31-19-249 ~]$ aws dynamodb list-tables
{
    "TableNames": [
        "cl-cars"
    ]
}
// -------------------------------------------------------------------------------
//  End of "I set up a VPC endpoint bc I assume I need that"
// -------------------------------------------------------------------------------
