output "bucket_name" {
  value       = aws_s3_bucket.frontend_bucket.bucket
  description = "The name of the S3 bucket"
}

output "bucket_id" {
  value       = aws_s3_bucket.frontend_bucket.id
  description = "The ID of the S3 bucket"
}

output "bucket_arn" {
  value       = aws_s3_bucket.frontend_bucket.arn
  description = "The ARN of the S3 bucket"
}

output "website_endpoint" {
  value       = aws_s3_bucket_website_configuration.frontend_bucket_website_configuration.website_endpoint
  description = "The URL of the deployed application"
}

output "cognito_user_pool_id" {
  value       = aws_cognito_user_pool.utility_manager_user_pool.id
  description = "The Cognito UserPool ID"
}

output "cognito_user_pool_client_id" {
  value       = aws_cognito_user_pool_client.utility_manager_user_pool_client.id
  description = "The Cognito UserPool client ID"
}
