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
