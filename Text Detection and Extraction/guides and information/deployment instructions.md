## To see the available subscription accounts of azure in cmd:
    az account list    

My current ones: 
1. "name": "Free Trial"
2. "name": "Microsoft Azure Sponsorship"

---

## To change subsription currently being used:
    az account set --subscription <name or id>    

Example:     

    az account set --subscription "Free Trial"    

---

## To check the current account being used:
    az account show    

---

## Choosing unique names for resources:
1 Resource group name:

    set RESOURCE_GROUP_NAME=textext-testing-rg    

2 Container registry name:

    set CONTAINER_REGISTRY_NAME=testtextextregistry    

3 Local Docker Image Name:

    set LOCAL_DOCKER_IMAGE=base-textext-docker-2    

4 Web App service plan:

    set APP_SERVICE_PLAN_NAME=webplan    

5 Web App Name:

    set WEB_APP_NAME=textextwebapptest    

---

## To deploy the webapp directly without docker container:
    az webapp up --name "%WEB_APP_NAME%" --runtime PYTHON:3.11 --sku B1 --logs    

---

## Build and Run Web App as a Local Docker Image:
1 To build a docker container:

    docker build --tag "%LOCAL_DOCKER_IMAGE%" .    

2 To run the docker image locally:

    docker run -d -p 8000:8000 "%LOCAL_DOCKER_IMAGE%"    

3 To stop docker container:

    docker stop <container-name>    

*(here container-name is the return value that gets printed when we start the container)*

---

## To create a PostgreSQL Database on Cloud

1. Create a Azure database for PostgreSQL flexible server with server name and password 

2. Create a database / use the existing database

3. Initialize database by creating tables using `init_db.py`

4. Store the predefined data in tables

5. Test the database connectivity and results using `test_db.py`

6. Set the database details in `.env` file

---

## To Build and Store web app as a docker container image on Azure

1 create Resource group: 

    az group create --name "%RESOURCE_GROUP_NAME%" --location eastus    

2 Create an Azure Container Registry:

    az acr create --resource-group "%RESOURCE_GROUP_NAME%" --name "%CONTAINER_REGISTRY_NAME%" --sku Basic --admin-enabled true    

3 Save the password to a variable:

    for /f "usebackq tokens=*" %i in (`az acr credential show --resource-group "%RESOURCE_GROUP_NAME%" --name "%CONTAINER_REGISTRY_NAME%" --query "passwords[?name == 'password'].value" --output tsv`) do set ACR_PASSWORD=%i    


4 To print / view password:

    echo %ACR_PASSWORD%    

5 Login to the ACR registry with registry name choosen in step 2 and the password from step 3 and username same as registry name most of the time 
*(we can get all of this from the Access Keys of Container Registry)*

    az acr login --name "%CONTAINER_REGISTRY_NAME%"    

or 

    az acr login --name "%CONTAINER_REGISTRY_NAME%" --password "%ACR_PASSWORD%" --username "%CONTAINER_REGISTRY_NAME%"    

6 Connect the local docker image to the container registry on cloud using tag:

    docker tag "%LOCAL_DOCKER_IMAGE%":latest "%CONTAINER_REGISTRY_NAME%".azurecr.io/"%LOCAL_DOCKER_IMAGE%":latest    

7 Push the image to the container registry:

    docker push "%CONTAINER_REGISTRY_NAME%".azurecr.io/"%LOCAL_DOCKER_IMAGE%":latest    

**NOTE: Instead of using steps 5 to 7 we can also do this:**
Build the image in Azure Container Registry:

    az acr build --resource-group "%RESOURCE_GROUP_NAME%" --registry "%CONTAINER_REGISTRY_NAME%" --image "%LOCAL_DOCKER_IMAGE%":latest .    

---

## Deploy the web app from the docker container image on Azure

1 Create an App Service plan:

    az appservice plan create --name "%APP_SERVICE_PLAN_NAME%" --resource-group "%RESOURCE_GROUP_NAME%" --sku B1 --is-linux    

2 Create the web app

    az webapp create --resource-group "%RESOURCE_GROUP_NAME%" --plan "%APP_SERVICE_PLAN_NAME%" --name "%WEB_APP_NAME%" --docker-registry-server-password "%ACR_PASSWORD%" --docker-registry-server-user "%CONTAINER_REGISTRY_NAME%" --role acrpull --deployment-container-image-name "%CONTAINER_REGISTRY_NAME%".azurecr.io/"%LOCAL_DOCKER_IMAGE%":latest    

3 The web app is visible at the site: `https://<WEB_APP_NAME>.azurewebsites.net`

4 To Deploy update - push the docker image to container registry as in step 7 of building container image.