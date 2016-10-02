list_ec2
========

List and print all EC2 instances in an AWS account using AWS API keys. 


Description
------------

The list_ec2 tool can be used to create timestamped CSV reports about EC2 instances in an AWS account. This is helpful if you are the maintainer of multiple EC2 subscriptions and want to ensure the EC2 instances are properly secured. Using the reports it becomes easy to review which instances are running on which external IP's for example without having to visit the AWS console. 

Example output is shown below;


![alt tag](https://raw.githubusercontent.com/marekq/list-ec2/master/docs/s1.png)


Usage
-----

The tool has been tested on Debian and MacOS, but should work on other platforms too. Besides Python, install the following package using 'python-pip';

    $ pip install boto3 

Next, ensure your ~/.aws/ directory contains valid AWS credentials, which you can create using the AWS CLI tool. Set the profile name and region within the script to ensure your resources can be printed. 

Results of the scan are shown on screen, stored in "ec2.csv" in the current directory and a timestamped copy of the results file is stored in folder 'logs'. You could use i.e. Splunk to monitor the logs directory over time and create security use cases in case i.e. an EC2 instance is launched without the proper security group applied. 

        
Contact
-------

For any questions or fixes, please reach out to @marekq! 