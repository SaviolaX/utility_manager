# Utility manager: Frontend

## Requirements

Configure access credentials to AWS account in AWC CLI

```text
aws_access_key_id = ...
aws_secret_access_key = ...
```

1. Terraform ~1.10.5
2. AWC CLI ~2.25
3. Task ~3.42

## The order steps to deploy on AWS S3

### Build app

```sh
npm run build
```

It generates files needed for deployment, and store them in `dist/` folder that placed in the project directory.

### Deploy to S3

To check witch resources will be created on AWS

- Go to `infrastructure` dir

```sh
cd infrastructure
```

- Initialize terraform

```sh
terraform init
```

- To check all resources will be changed or created

```sh
task plan
```

- To start create resources and upload project(`dist/`) on S3

```sh
task apply
```

- To delete everything was created

```sh
task destroy
```
