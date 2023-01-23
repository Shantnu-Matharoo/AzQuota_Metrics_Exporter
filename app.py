#!/usr/bin/env python3

from prometheus_client import start_http_server, Gauge
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.subscription import SubscriptionClient
import time
import os

'''
Define Prometheus metrics
'''
RESOURCE_QUOTA_LIMIT = Gauge('az_resource_quota_limit', 'Resource limit for an Azure resource', ['subscription_id', 'resource_type', 'resource_category', 'resource_location'])
RESOURCE_QUOTA_USAGE = Gauge('az_resource_quota_usage', 'Resource usage for an Azure resource', ['subscription_id', 'resource_type', 'resource_category', 'resource_location'])

client_id = os.getenv("CLIENT_ID")
secret = os.getenv("SECRET")
tenant = os.getenv("TENANT")
listen_port = os.getenv("LISTEN_PORT")
resource_location = os.getenv("LOCATION")
subscriptionId = os.getenv("SUBSCRIPTIONID")

'''
Set credentials using the env vars.
'''
credentials = ServicePrincipalCredentials(
    client_id=client_id,
    secret=secret,
    tenant=tenant
)

'''
Validating Subscription. 
'''
def get_subscription():
    sub_client = SubscriptionClient(credentials)
    subs = sub_client.subscriptions.list()
    for sub in subs:
        if sub.state == "Enabled" and subscriptionId in sub.subscription_id:
            return True
        else:
            raise Exception("Subscription not found/enabled")

'''
Gets all limits and quotas for Compute Resources
'''
def process_azure_compute():
    client = ComputeManagementClient(credentials, subscriptionId)
    try:
        usages_client = client.usage.list(resource_location)
        for use in usages_client:
            print(use.current_value)
            RESOURCE_QUOTA_USAGE.labels(subscriptionId, use.name.value, "Compute", resource_location).set(use.current_value)
            RESOURCE_QUOTA_LIMIT.labels(subscriptionId, use.name.value, "Compute", resource_location).set(use.limit)
    except:
        pass

'''
Gets all limits and quotas for Network Resources
'''
def process_azure_network():
    client = NetworkManagementClient(credentials, subscriptionId)
    try:
        usages_network = client.usages.list(resource_location)
        for use in usages_network:
            RESOURCE_QUOTA_USAGE.labels(subscriptionId, use.name.value, "Network", resource_location).set(use.current_value)
            RESOURCE_QUOTA_LIMIT.labels(subsubscriptionId, use.name.value, "Network", resource_location).set(use.limit)
    except:
        pass

'''
Gets all limits and quotas for Storage Resources
'''
def process_azure_storage():
    client = StorageManagementClient(credentials, subscriptionId)
    try:
        usages_storage = client.usage.list_by_location(resource_location)
        for use in usages_storage:
            RESOURCE_QUOTA_USAGE.labels(subscriptionId, use.name.value, "Storage", resource_location).set(use.current_value)
            RESOURCE_QUOTA_LIMIT.labels(subscriptionId, use.name.value, "Storage", resource_location).set(use.limit)
    except:
        pass

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    print("Starting up server...")
    try:
        int(listen_port)
    except:
        print(f'Value for variable LISTEN_PORT is {listen_port} and could not be converted to an integer. Please fix this issue and restart the application.')
        print('Stopping server.')
        exit
    get_subscription()
    start_http_server(int(listen_port))
    print(f'Server sucessfully started. Listening on port {listen_port}')
    while True:
        process_azure_compute()
        process_azure_network()
        process_azure_storage()
        time.sleep(3600)