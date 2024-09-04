# clBot
How to know a good deal when you see one? Look at a lot of them.

You can read about why this is a bad idea here: https://singlepaynews.com/feed/1431

But apparently I just can't help myself.

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
