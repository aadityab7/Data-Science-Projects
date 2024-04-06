# To see the available subscription accounts of azure in cmd:
`az account list`

My current ones: 
- "name": "Free Trial"
- "name": "Microsoft Azure Sponsorship"

# To change subsription currently being used:
`az account set --subscription <name or id>`

Example: `az account set --subscription "Free Trial"`

# To check the current account being used:
`az account show`

# To deploy the webapp:
`az webapp up --name textext --runtime PYTHON:3.11 --sku B1 --logs`