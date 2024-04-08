# To see the available subscription accounts of azure in cmd:
`az account list`

My current ones: 
1. "name": "Free Trial"
2. "name": "Microsoft Azure Sponsorship"

# To change subsription currently being used:
`az account set --subscription <name or id>`

Example: `az account set --subscription "Free Trial"`

# To check the current account being used:
`az account show`

# To deploy the webapp directly:
`az webapp up --name textext --runtime PYTHON:3.11 --sku B1 --logs`

# Build and Run Web App as a Local Docker Image:
1. To build a docker container:
`docker build --tag base-textext-docker-2 .`
2. To run the docker image locally:
`docker run -d -p 8000:8000 base-textext-docker-2`
3. To stop docker container:
`docker stop <container-name>`
(here container-name is the return value that gets printed when we start the container)

# To create a PostgreSQL Database on Cloud
1. Create a Azure database for PostgreSQL flexible server with server name and password 
2. Create a database / use the existing database
3. Initialize database by creating tables using `init_db.py`
4. Store the predefined data in tables
5. Test the database connectivity and results using `test_db.py`
6. Set the database details in `.env` file

# To Build and deploy Web App as a container on Azure
1. create Resource group:
`az group create --name textext-testing-rg --location eastus`

2. Create an Azure Container Registry:
`az acr create --resource-group textext-testing-rg --name testtextextregistry --sku Basic --admin-enabled true`

3. Save the password to a variable:
``for /f "usebackq tokens=*" %i in (`az acr credential show --resource-group textext-testing-rg --name testtextextregistry --query "passwords[?name == 'password'].value" --output tsv`) do set ACR_PASSWORD=%i``

4. To print / view password:
`echo %ACR_PASSWORD%`

5. Build the image in Azure Container Registry:
`az acr build --resource-group textext-testing-rg --registry testtextextregistry --image webappsimple:latest .`