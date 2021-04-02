import boto3
import sys
from pprint import pprint
# Define the resource
eks = boto3.client('eks')
ctags = {'autodelete': 'no'}

# Define region scope
#regions = ['us-east-1','us-east-2','us-west-1','us-west-2','sa-east-1','ca-central-1','eu-central-1','eu-north-1','ap-south-1','eu-west-1','eu-west-2','eu-west-3','ap-northeast-1','ap-northeast-2','ap-southeast-1','ap-southeast-2']
regions = ['us-east-2']
def lambda_handler(event, context):
    for x in range(0, len(regions)):
        print("\n[",regions[x],"]")
        eks_obj = boto3.client('eks', region_name=regions[x])
        response = eks_obj.list_clusters()
        lcluster = response['clusters']
        if len(response)>0:
            for i in lcluster:
                print("\tCluster Name:",i)
                dcluster=eks_obj.describe_cluster(name=i)
                list = dcluster.get('cluster')
                tags = (list.get('tags'))
                if ctags != tags:
                    print("\t\tCluster",i,"will be deleted.")
                    lngroup=eks_obj.list_nodegroups(clusterName=i)
                    ngroup=lngroup['nodegroups']
                    print("\t\tFounded ",len(ngroup),"NodeGroups.")
                    if len(ngroup)>0:
                        for f in ngroup:
                            dngresult = delete_nodegroup(eks_obj,i, f)
                            if dngresult == True:
                                print("\t\tDeleting NodeGroup",f)
                            else:
                                print("\t\tError: Wasn't possible to delete the NodeGroup",f)
                    else: 
                        dcresult = delete_cluster(eks_obj, i)
                        if dcresult == True:
                            print("\t\tDeleting Cluster",i)
                        else:
                            print("\t\tError: Wasn't possible to delete the Cluster",i)
                else: 
                    print("\t\tThis cluster isn't in my the list to be killed!\n")
        else:
            print("Founded NO clusters in this region.")

def delete_cluster(eks_obj, i):
    try:
        eks_obj.delete_cluster(name=i)
        return True
    except:
        return False

def delete_nodegroup(eks_obj, i, f):
    try:
        eks_obj.delete_nodegroup(clusterName=i,nodegroupName=f)
        return True
    except:
        return False