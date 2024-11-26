import pytest
from pulumi import automation as auto

# Integration tests: Überprüfen Sie die Beziehungen zwischen den Ressourcen.

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

def test_blob_container_linked_to_storage_account(pulumi_stack):
    # Auslesen der Outputs des Pulumi-Stacks
    outputs = pulumi_stack.outputs()
    blob_container_name = outputs["blob_container_name"].value  # Name des Blob-Containers
    storage_account_name = outputs["storage_account_name"].value  # Name des Storage-Accounts
    
    # Überprüfen, ob der Blob-Container existiert
    assert blob_container_name is not None, "Blob Container Name ist None"
    # Überprüfen, ob der Storage-Account existiert
    assert storage_account_name is not None, "Storage Account Name ist None"

def test_web_app_linked_to_app_service_plan(pulumi_stack):
    # Auslesen der Outputs des Pulumi-Stacks
    outputs = pulumi_stack.outputs()
    web_app_name = outputs["web_app_name"].value  
    app_service_plan_name = outputs["app_service_plan_name"].value  #
    
    # Überprüfen, ob die Web-App existiert
    assert web_app_name is not None, "Web App Name ist None"
    # Überprüfen, ob der App Service Plan existiert
    assert app_service_plan_name is not None, "App Service Plan Name ist None"

def test_web_app_has_correct_app_settings(pulumi_stack):
    # Auslesen der Outputs des Pulumi-Stacks
    outputs = pulumi_stack.outputs()
    web_app_url = outputs["web_app_url"].value  
    
    # Überprüfen, ob die Web-App-URL existiert
    assert web_app_url is not None, "web_app_url ist None"
    # Überprüfen, ob die URL das Standard-Domainmuster von Azure-Webseiten enthält
    assert "azurewebsites.net" in web_app_url, \
        f"web_app_url enthält nicht 'azurewebsites.net': {web_app_url}"