import boto3
import logging

# Setup simple the logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Define the resource
ec2 = boto3.resource('ec2')

# Get a list of all instances
all_instances = [i for i in ec2.instances.all()]

def lambda_handler(event, context):
    # Use the filter() method of the instances collection to retrieve all running EC2 instances with this filter.
    filters = [{
            'Name': 'tag:autostop', 
            'Values': ['no']
        },
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]
    
    # Filtering the instances according with the filters
    instances = [i for i in ec2.instances.filter(Filters=filters)]

    # Geting only the instances that doesnt have hove what we filtered.
    instances_to_stop = [to_stop for to_stop in all_instances if to_stop.id not in [i.id for i in instances]]
    
    # Check if there's something in the list, and if find a instance execute the follow actions
    if len(instances_to_stop) > 0:
        print("Founded #",len(instances_to_stop)," instance(s) to be stoped.")
        for instance in instances_to_stop:
            # Stop the instance
            instance.stop()
            # Logging the execution
            print("\t",instance,": Stoped")
    else:
        print("There's no instances to stop.")