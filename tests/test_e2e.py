import requests
import pytest
from pulumi import automation as auto

# End-to-end tests: Stellen Sie sicher, dass der gesamte Stack korrekt bereitgestellt wird.

@pytest.fixture(scope="module")
def pulumi_stack():
    project_name = "pulumi-hello-world"  
    stack_name = "dev" 

    stack = auto.select_stack(
        stack_name=stack_name,
        project_name=project_name,
        program=lambda: None,  
    )
    return stack

def test_web_app(pulumi_stack):
    # Auslesen der Outputs des Pulumi-Stacks
    outputs = pulumi_stack.outputs()
    web_app_url = outputs["web_app_url"].value  

    # Test 1: Überprüfung der Erreichbarkeit der Web-App über HTTP
    response = requests.get(f"http://{web_app_url}")
    assert response.status_code == 200, "Web App ist über HTTP nicht erreichbar"
    assert "Hello, World!" in response.text, "HTTP-Response enthält nicht 'Hello, World!'"

    # Test 2: Überprüfung der HTTP-Header
    assert "Content-Type" in response.headers, "HTTP-Header 'Content-Type' fehlt"
    assert response.headers["Content-Type"] == "text/html; charset=utf-8", \
        f"Unerwarteter Content-Type: {response.headers['Content-Type']}"

    # Test 3: Überprüfung der Erreichbarkeit der Web-App über HTTPS
    response_https = requests.get(f"https://{web_app_url}")
    assert response_https.status_code == 200, "Web App ist über HTTPS nicht erreichbar"
    assert "Hello, World!" in response_https.text, "HTTPS-Response enthält nicht 'Hello, World!'"

    # Test 4: Überprüfung der HTTPS-Header
    assert "Content-Type" in response_https.headers, "HTTPS-Header 'Content-Type' fehlt"
    assert response_https.headers["Content-Type"] == "text/html; charset=utf-8", \
        f"Unerwarteter HTTPS-Content-Type: {response_https.headers['Content-Type']}"

    # Test 5: Überprüfung der Ladezeit der Web-App über HTTPS
    assert response_https.elapsed.total_seconds() < 2, \
        f"HTTPS-Ladezeit zu hoch: {response_https.elapsed.total_seconds()} Sekunden"

    # Test 6: Überprüfung des Inhalts der Web-App
    assert "Hello, World!" in response.text, "Der Seiteninhalt ist nicht korrekt"
