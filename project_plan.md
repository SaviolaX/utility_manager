# Utility manager

Utility manager is an app that helps you to count your mounthly utilities prices.

## Authentication

- Recieve user's manual input
- Check user in db
- Create user
- Return response about user creation

## Workflow

- Receive user's manual inputs via client interface
- Receive user's data for previous month
- Counts difference
- Return to user results
- Store current data in db

## Backend

### Dependencies

- boto3
- pytest

### Deployment backend

Would like to use [AWS](https://eu-central-1.console.aws.amazon.com/console/home?region=eu-central-1)

- Cognito
- Lambda
- DynamoDB
- S3 Bucker (optionaly)
- API Gataway

### Infrastructure

- [Terraform](https://www.terraform.io/)

### Package manager

- [UV](https://github.com/astral-sh/uv)

## Frontend

- [Vue js](https://vuejs.org/)

### Dependencies frontend

- Maybe [Chart JS](https://www.chartjs.org/)

### Deployment frontend

At this moment i think about:

- [AWS Amplify](https://aws.amazon.com/amplify/)
- [S3 Bucket static hosting](https://docs.aws.amazon.com/AmazonS3/latest/userguide/HostingWebsiteOnS3Setup.html)
