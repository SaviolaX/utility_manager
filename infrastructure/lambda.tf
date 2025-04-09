# archive function in zip file
data "archive_file" "archive_utility_manager_lambda_function" {
  type        = "zip"
  source_dir  = "../backend/app"
  output_path = "../backend/utility_manager_lambda_function.zip"
}

# Create an AWS Lambda function in Terraform
resource "aws_lambda_function" "utility_manager_lambda_function" {
  filename         = data.archive_file.archive_utility_manager_lambda_function.output_path
  function_name    = "utility_manager_lambda_function"
  role             = aws_iam_role.utility_manager_lambda_role.arn
  handler          = "main.lambda_handler"
  runtime          = "python3.9"
  source_code_hash = data.archive_file.archive_utility_manager_lambda_function.output_base64sha256
  timeout          = 60
  memory_size      = 128

  environment {
    variables = {
      DYNAMO_DB_TABLE = aws_dynamodb_table.utility_manager_dynamodb_table.arn
    }
  }
}

resource "aws_iam_role" "utility_manager_lambda_role" {
  name = "utility_manager_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy" "utility_manager_lambda_basic_execution" {
  name        = "utility_manager_lambda_basic_execution"
  description = "Allow Lambda to execute basic actions"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })

}

resource "aws_iam_role_policy_attachment" "utility_manager_lambda_role_policy" {
  role       = aws_iam_role.utility_manager_lambda_role.name
  policy_arn = aws_iam_policy.utility_manager_lambda_basic_execution.arn
}
