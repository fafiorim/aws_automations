import boto3
import logging
from datetime import datetime

# Setup simple the logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Define the resource
ec2 = boto3.resource('ec2')

# Define region scope
regions =['us-east-1','us-east-2','us-west-1','us-west-2','sa-east-1','ca-central-1','eu-central-1','eu-north-1','ap-south-1','eu-west-1','eu-west-2','eu-west-3','ap-northeast-1','ap-northeast-2','ap-southeast-1','ap-southeast-2']

def lambda_handler(event, context):
    start_time = datetime.now()
    # Use the filter() method of the instances collection to retrieve all running EC2 instances with this filter.
    filter_running = [
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]

    filter_tag = [
        {
            'Name': 'tag:autostop', 
            'Values': ['no']
        }
    ]
    # For each object in the list regions do all those actions
    for x in range(0, len(regions)):
        # Get all object ec2 objects in the region x
        ec2_obj = boto3.resource('ec2', region_name=regions[x])

        #print the region, just a format for the logs
        print("\n[",regions[x],"]")
 

        # Filtering the instances according with the filters
        # Filtering the instance objects is running
        running_instances = [i for i in ec2_obj.instances.filter(Filters=filter_running)]
        # Filtering instances that has the specified tag
        tagged_instances = [i for i in ec2_obj.instances.filter(Filters=filter_tag)]
        # Filtering instances that are running and hasn't the tagged defined
        instances_to_stop = [to_stop for to_stop in running_instances if to_stop.id not in [f.id for f in tagged_instances]]

        #
        print("\t[Enviroment Status]")
        print("\t\tFounded #",len(running_instances)," instance(s) running.")
        # Print the instances that are running
        for instance in running_instances:
            print("\t\t\t",instance,": Running")

        # Check if there's something in the list, and if find a instance execute the follow actions
        print("\t[Action to be done]")
        if len(instances_to_stop) > 0:
            print("\t\tFounded #",len(instances_to_stop)," instance(s) to be stoped.")
            for instance in instances_to_stop:
                # Stop the instance
                instance.stop()
                #Logging the execution
                print("\t\t\t",instance,": Stoped")
        else:
            print("\t\tFound Zero instances to Stop. So, there's nothing to do.")
    
    end_time = datetime.now()
    took_time = end_time - start_time
    print("\nTime spent for the total execution: ",str(took_time),"\n")