import boto3
import logging

# Setup simple the logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Define the resource
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
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

    #
    # Filtering the instances according with the filters
    #
    # Filtering the instance objects is running
    running_instances = [i for i in ec2.instances.filter(Filters=filter_running)]
    # Filtering instances that has the specified tag
    tagged_instances = [i for i in ec2.instances.filter(Filters=filter_tag)]
    # Filtering instances that are running and hasn't the tagged defined
    instances_to_stop = [to_stop for to_stop in running_instances if to_stop.id not in [f.id for f in tagged_instances]]

    #
    print("[Enviroment Status]")
    print("\tFounded #",len(running_instances)," instance(s) running.")
    # Print the instances that are running
    for instance in running_instances:
        print("\t\t",instance,": Running")

    # Check if there's something in the list, and if find a instance execute the follow actions
    print("[Action to be done]")
    if len(instances_to_stop) > 0:
        print("\tFounded #",len(instances_to_stop)," instance(s) to be stoped.")
        for instance in instances_to_stop:
            # Stop the instance
            instance.stop()
            #Logging the execution
            print("\t\t",instance,": Stoped")
    else:
        print("\tFound Zero instances to Stop. So, there's nothing to do.\n")