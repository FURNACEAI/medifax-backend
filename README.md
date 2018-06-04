# Medifax Backend AWS Lambda Functions

These functions are the business logic for the Medifax MVP.

# Customers Endpoints

Service Information
service: medifax-backend-customers
stage: prod
region: us-east-1
stack: medifax-backend-customers-prod
endpoints:
  POST - https://u3tad4wx2c.execute-api.us-east-1.amazonaws.com/prod/customers/create
  GET - https://u3tad4wx2c.execute-api.us-east-1.amazonaws.com/prod/customers/list
  GET - https://u3tad4wx2c.execute-api.us-east-1.amazonaws.com/prod/customers/{id}
  POST - https://u3tad4wx2c.execute-api.us-east-1.amazonaws.com/prod/customers/share/{id}
  POST - https://u3tad4wx2c.execute-api.us-east-1.amazonaws.com/prod/customers/onetimes3url
  POST - https://u3tad4wx2c.execute-api.us-east-1.amazonaws.com/prod/customers/update/{id}
  DELETE - https://u3tad4wx2c.execute-api.us-east-1.amazonaws.com/prod/customers/{id}
  POST - https://u3tad4wx2c.execute-api.us-east-1.amazonaws.com/prod/customers/auth
functions:
  create: medifax-backend-customers-prod-create
  list: medifax-backend-customers-prod-list
  get: medifax-backend-customers-prod-get
  share: medifax-backend-customers-prod-share
  onetimes3url: medifax-backend-customers-prod-onetimes3url
  update: medifax-backend-customers-prod-update
  delete: medifax-backend-customers-prod-delete
  auth: medifax-backend-customers-prod-auth

# Employee Endpoints

service: medifax-backend-employees
stage: prod
region: us-east-1
stack: medifax-backend-employees-prod
endpoints:
  POST - https://5y96pktw7j.execute-api.us-east-1.amazonaws.com/prod/employee/create
  GET - https://5y96pktw7j.execute-api.us-east-1.amazonaws.com/prod/employee/list
  GET - https://5y96pktw7j.execute-api.us-east-1.amazonaws.com/prod/employee/{id}
  POST - https://5y96pktw7j.execute-api.us-east-1.amazonaws.com/prod/employee/update/{id}
  DELETE - https://5y96pktw7j.execute-api.us-east-1.amazonaws.com/prod/employee/{id}
  POST - https://5y96pktw7j.execute-api.us-east-1.amazonaws.com/prod/employee/auth
functions:
  create: medifax-backend-employees-prod-create
  list: medifax-backend-employees-prod-list
  get: medifax-backend-employees-prod-get
  update: medifax-backend-employees-prod-update
  delete: medifax-backend-employees-prod-delete
  auth: medifax-backend-employees-prod-auth
