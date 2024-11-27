import pulumi
import os
from pulumi_azure_native import resources, storage, web, insights
from pulumi import FileAsset

# Erstellen einer Ressourcengruppe
resource_group = resources.ResourceGroup("uebung4-resourcegroup", location="switzerlandnorth")

# Erstellen eines Storage-Accounts
storage_account = storage.StorageAccount("storageaccount",
    resource_group_name=resource_group.name,
    location=resource_group.location,
    sku=storage.SkuArgs(name="Standard_LRS"),
    kind="StorageV2",
    allow_blob_public_access=True
)

# Erstellen eines Blob-Containers
blob_container = storage.BlobContainer("blobcontainer",
    account_name=storage_account.name,
    resource_group_name=resource_group.name,
    public_access="Blob"
)

# ZIP-Datei der Anwendung erstellen
os.system('cd app && zip -r ../webapp.zip .')

# Hochladen einer Datei in den Blob-Container
app_blob = storage.Blob("webappzip",
    resource_group_name=resource_group.name,
    account_name=storage_account.name,
    container_name=blob_container.name,
    source=FileAsset("./webapp.zip")
)

# Generieren der Blob-URL
blob_url = pulumi.Output.concat("https://", storage_account.name, ".blob.core.windows.net/", blob_container.name, "/", app_blob.name)

# Erstellen eines App Service Plans
app_service_plan = web.AppServicePlan("serviceplan",
    resource_group_name=resource_group.name,
    location=resource_group.location,
    kind="Linux",
    reserved=True,
    sku=web.SkuDescriptionArgs(
        tier="Free",
        name="F1"
    )
)

# Application Insights erstellen
app_insights = insights.Component("appinsights",
    resource_group_name=resource_group.name,
    location=resource_group.location,
    application_type="web",
    kind="web",
    ingestion_mode="ApplicationInsights"
)

# Erstellen einer Web-App
web_app = web.WebApp("webapp",
    resource_group_name=resource_group.name,
    location=resource_group.location,
    server_farm_id=app_service_plan.id,
    site_config=web.SiteConfigArgs(
        app_settings=[
            web.NameValuePairArgs(name="WEBSITE_RUN_FROM_PACKAGE", value=blob_url),
            web.NameValuePairArgs(name="APPINSIGHTS_INSTRUMENTATIONKEY", value=app_insights.instrumentation_key),
        ],
        linux_fx_version="PYTHON|3.11",
    )
)
# Outputs exportieren
pulumi.export("web_app_url", web_app.default_host_name)
pulumi.export("blob_container_name", blob_container.name)
pulumi.export("web_app_name", web_app.name)
pulumi.export("storage_account_sku", storage_account.sku.name)
pulumi.export("storage_account_name", storage_account.name)
pulumi.export("storage_account_kind", storage_account.kind)
pulumi.export("app_service_plan_name", app_service_plan.name)
pulumi.export("app_service_plan_sku_tier", app_service_plan.sku.tier)
pulumi.export("app_service_plan_kind", app_service_plan.kind)
pulumi.export("web_app_linux_fx_version", web_app.site_config.linux_fx_version)
