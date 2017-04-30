#!/usr/bin/python
# marek kuczynski
# @marekq
# www.marek.rocks

import boto3, datetime, os, time

# add your boto3 profile name and EC2 region, see ~/.aws/config and ~/.aws/credentials
profile 	= 'default'				
region 		= 'eu-west-1'


### DO NOT EDIT ANYTHING BELOW THIS LINE ### 


vtags		= []
resu		= []

cpath       = os.getcwd()
cfile		= cpath+'/ec2.csv'
rpath		= cpath+'/logs/'

# current time ts
now     	= datetime.datetime.now()
timest  	= now.strftime("%Y-%m-%d_%H-%M")
unixti      = int(time.time())


def get_ec2(prof, reg):
	# use the temporary credentials to retrieve EC2 data from the API
	session 	= boto3.session.Session(profile_name = prof)
	sts_client	= session.client('ec2', region_name = reg) 

	# tags to print in csv
	tags1		= ['PrivateIpAddress','PublicIpAddress','Platform','InstanceId','VpcId','InstanceType','PublicDnsName','Hypervisor','LaunchTime','KernelId','Platform','Architecture','VirtualizationType','InstanceLifecycle','PrivateDnsName','PublicDnsName','ImageId','SubnetId']
	tags2		= {'Placement' : 'AvailabilityZone', 'State' : 'Name', 'StateReason' : 'Message', 'Monitoring' : 'State'}

	# run describe_instances against EC2 API
	try:
		x		= sts_client.describe_instances()
		found	= True

	except:
		found	= False

	# get ec2 information
	if found:
		for res in x['Reservations']:
			for a in res['Instances']:
				z1 = []
				z2 = []
				z3 = []
				z4 = []
				z5 = []

				# iterate top level tags
				for tag in tags1:
					try:
						if tag == 'LaunchTime':
							dat = a[tag]
							y	= dat.strftime("%d-%m-%Y_%H-%M")
						
						else:
							y 	= a[tag]

						z1.append(str(y))

					except:
						z1.append('')

				# iterate the known, default tags of the instance
				for k, v in tags2.items():
					try:
						z 		= a[k][v]
						z2.append(str(z))

					except:
						z2.append('')

				# iterate the variable tags defined by the user of the instance
				for k in a['Tags']:
					
					ke	= k['Key'] 
					va 	= k['Value']
						
					if ke not in vtags:
						vtags.append(ke)

					z3.append(va)

				# iterate the security groups of the instance
				try:
					y			= a['SecurityGroups']

					for item in y:
						z		= item['GroupId']
						z4.append(str(z)+' ')

				except:
					pass

				# print the ARN of the lookup, the unix time of the scan and the date time of the scan
				z5		= get_ts()
				zz 		= "'"+"','".join(z1 + z2 + z3 + z4 + z5)+"'"

				resu.append(zz)
				print zz


	# create the headerline of the csv file and store it in a global variable
	global tagline

	# construct EC2 instance details
	t1			= tags1

	# construct instance placement headers
	t2			= []
	for k, v in tags2.items():
	    t2.append(k)

	# construct EC2 user defined tags
	t3			= vtags

	# construct EC2 security groups and timestamps
	t4			= ['SecurityGroups','unix-time','date-time']
	
	t5			= t1+t2+t3+t4
	tagline 		= "'"+"','".join([unicode(i) for i in t5])+"'"


def get_ts():
	return [str(unixti), str(timest)]


def write_log(filen, srcobj, tagl, newl, mode):
        f       = open(filen, mode)
        if tagl != '':
                f.write(tagl+'\n')

        for x in srcobj:
                if len(x) > 5:
                        if newl == 'Y':
							f.write(str(x)+'\n')

                        else:
                            f.write(str(x))
        f.close()


def write_res():
	cfname	= str(rpath)+'ec2-'+str(timest)+'.csv'
	write_log(cfname, resu, tagline, 'Y', 'w')
	write_log(cfile, resu, tagline, 'Y', 'w')
	print '\ndone with EC2 at '+str(timest)+', results written to '+str(cfname)+' and '+str(cfile)+'\n'


# # # # # #
# run the functions and exit

get_ec2(profile, region)
write_res()
