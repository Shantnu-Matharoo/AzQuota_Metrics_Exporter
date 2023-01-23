# metrics-exporter-for-az-quotas

## Metrics and Labels

The exporter exposes 2 metrics to Prometheus.

```text
az_resource_quota_limit
az_resource_quota_usage
```

Labels are used to filter the desired values to monitor. The following labels are set for both metrics:

```text
subscription_id
subscription_name
resource_type
resource_category
```

### Example 

If you want to find all Azure Network resource usages for a certain subscription you could use this query in Prometheus:

```text
az_resource_quota_usage{resource_category="Network", subscription_name="Example Subscription"}
```
---
## Configuration

### Exporter

The exporter need to be configured using environment variables. Create an [Azure Service Principal](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal) and grant it role "Contributor" permissions over a subscription you want to get the resource quotas from.

All the following variables need to be set. There are no defaults!

- __CLIENT_ID__ (The ID of your Service Principal)
- __SECRET__ (The secret of the Service Principal)
- __TENANT__ (Your Azure tenant ID)
- __LISTEN_PORT__ (The port you want the metrics server to be exposed to)
- __LOCATION__ (Location of your resources i.e. 'westeurope')

### Prometheus Config

Set the following job in your Prometheus config file:

```yaml
scrape_configs:
  - job_name: 'metrics-exporter-for-az-quotas'
    scrape_interval: 60s
    static_configs:
      - targets: ['<SVC Name>:<port>'] 
```

---

## Running the exporter

The exporter is designed to be run inside a Docker Container but could also be run outside of one (not recommended). 

Use the following command (substitute the placeholder values) to run the azure-quota-exporter:

```text
docker run -d -p "8000:8000" \
--env CLIENT_ID=yourid \
--env SECRET=yoursecret \
--env TENANT=tenantid \
--env LISTEN_PORT=8000 \
--env LOCATION=westeurope \
metrics-exporter-for-az-quotas
```

The project is licensed under the GPLv2.
