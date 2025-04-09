resource "aws_dynamodb_table" "utility_manager_dynamodb_table" {
  name           = "utility_manager_db"
  billing_mode   = "PROVISIONED"
  read_capacity  = 10
  write_capacity = 10
  hash_key       = "UserId"
  range_key      = "Date"

  attribute {
    name = "UserId"
    type = "S"
  }

  attribute {
    name = "Date"
    type = "S"
  }

}

resource "aws_iam_role_policy" "utility_manager_dynamodb_policy" {
  name = "utility_manager_lambda_dynamodb_policy"
  role = aws_iam_role.utility_manager_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:Scan"
        ]
        Resource = "arn:aws:dynamodb:*:*:table/${aws_dynamodb_table.utility_manager_dynamodb_table.name}"
      }
    ]
  })
  depends_on = [aws_dynamodb_table.utility_manager_dynamodb_table]
}

