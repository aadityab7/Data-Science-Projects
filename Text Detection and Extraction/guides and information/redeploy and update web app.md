# Redploy and update the web app using container

    az account list
    az account set --subscription "Free Trial"
    az account show
    set RESOURCE_GROUP_NAME=textextTestingResourceGroup
    set CONTAINER_REGISTRY_NAME=testtextextregistry
    set LOCAL_DOCKER_IMAGE=base-test-textext-docker
    set APP_SERVICE_PLAN_NAME=webplan
    set WEB_APP_NAME=textextTestWebAppTest
    cd C:\Program Files\Docker\Docker
    C:
    "Docker Desktop.exe"
    cd G:\"00 Data Science"\"Data-Science-Projects"\"Text Detection and Extraction"
    G:
    docker build --tag "%LOCAL_DOCKER_IMAGE%" .
    for /f "usebackq tokens=*" %i in (`docker run -d -p 8000:8000 "%LOCAL_DOCKER_IMAGE%"`) do set CONTAINER_NAME=%i
    ECHO %CONTAINER_NAME%
    docker stop "%CONTAINER_NAME%"
    for /f "usebackq tokens=*" %i in (`az acr credential show --resource-group "%RESOURCE_GROUP_NAME%" --name "%CONTAINER_REGISTRY_NAME%" --query "passwords[?name == 'password'].value" --output tsv`) do set ACR_PASSWORD=%i
    echo %ACR_PASSWORD%
    az acr login --name "%CONTAINER_REGISTRY_NAME%" --password "%ACR_PASSWORD%" --username "%CONTAINER_REGISTRY_NAME%"
    docker tag "%LOCAL_DOCKER_IMAGE%":latest "%CONTAINER_REGISTRY_NAME%".azurecr.io/"%LOCAL_DOCKER_IMAGE%":latest
    docker push "%CONTAINER_REGISTRY_NAME%".azurecr.io/"%LOCAL_DOCKER_IMAGE%":latest
