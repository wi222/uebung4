import pytest
from pulumi import automation as auto

@pytest.fixture(scope="module")
def pulumi_stack():
    project_name = "pulumi-hello-world"
    stack_name = "dev"

    try:
        stack = auto.select_stack(
            stack_name=stack_name,
            project_name=project_name,
            program=lambda: None,
        )
    except auto.errors.StackNotFoundError:
        stack = auto.create_stack(
            stack_name=stack_name,
            project_name=project_name,
            program=lambda: None,
        )
        stack.up(on_output=print)  # Initial deployment

    return stack
def test_storage_account_configuration(pulumi_stack):
    # Auslesen der Outputs des Pulumi-Stacks
    outputs = pulumi_stack.outputs()
    storage_account_name = outputs["storage_account_name"].value  
    storage_account_sku = outputs["storage_account_sku"].value  
    storage_account_kind = outputs["storage_account_kind"].value  
    
    # Überprüfen, ob der Storage-Account korrekt erstellt wurde
    assert storage_account_name is not None, "Storage Account Name ist None"
    assert storage_account_sku == "Standard_LRS", \
        f"Erwartete SKU: 'Standard_LRS', aber gefunden: {storage_account_sku}"
    assert storage_account_kind == "StorageV2", \
        f"Erwartete Art: 'StorageV2', aber gefunden: {storage_account_kind}"

def test_blob_container_configuration(pulumi_stack):
    outputs = pulumi_stack.outputs()
    blob_container_name = outputs["blob_container_name"].value  # Name des Blob-Containers
    
    # Überprüfen, ob der Blob-Container korrekt erstellt wurde
    assert blob_container_name is not None, "Blob Container Name ist None"

def test_app_service_plan_configuration(pulumi_stack):
    outputs = pulumi_stack.outputs()
    app_service_plan_name = outputs["app_service_plan_name"].value  
    app_service_plan_sku_tier = outputs["app_service_plan_sku_tier"].value  
    app_service_plan_kind = outputs["app_service_plan_kind"].value 
    
    # Überprüfen, ob der App Service Plan korrekt konfiguriert wurde
    assert app_service_plan_name is not None, "App Service Plan Name ist None"
    assert app_service_plan_sku_tier == "Free", \
        f"Erwartete Tier: 'Free', aber gefunden: {app_service_plan_sku_tier}"
    assert app_service_plan_kind == "linux", \
        f"Erwartete Art: 'linux', aber gefunden: {app_service_plan_kind}"

def test_web_app_configuration(pulumi_stack):
    outputs = pulumi_stack.outputs()
    web_app_name = outputs["web_app_name"].value  
    web_app_linux_fx_version = outputs["web_app_linux_fx_version"].value  
    
    # Überprüfen, ob die Web-App korrekt konfiguriert wurde
    assert web_app_name is not None, "Web App Name ist None"
    assert web_app_linux_fx_version == "PYTHON|3.11", \
        f"Erwartete Laufzeitversion: 'PYTHON|3.11', aber gefunden: {web_app_linux_fx_version}"
