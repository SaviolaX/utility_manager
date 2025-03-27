# Purpose: This file is used to create the API Gateway for the Utility Manager application.

# Create a REST API
resource "aws_api_gateway_rest_api" "utility_manager_api_gateway" {
  name        = "utility_manager_api_gateway"
  description = "Utility Manager API Gateway"
}

# Create a "hello" resource
resource "aws_api_gateway_resource" "utility_manager_api_gateway_resource" {
  rest_api_id = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  parent_id   = aws_api_gateway_rest_api.utility_manager_api_gateway.root_resource_id
  path_part   = "hello"

  depends_on = [aws_api_gateway_rest_api.utility_manager_api_gateway]
}

###################### GET method ##############################
# Create a GET method for the "hello" resource
resource "aws_api_gateway_method" "utility_manager_api_gateway_method" {
  rest_api_id      = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  resource_id      = aws_api_gateway_resource.utility_manager_api_gateway_resource.id
  http_method      = "GET"
  authorization    = "COGNITO_USER_POOLS"
  api_key_required = false
  authorizer_id    = aws_api_gateway_authorizer.utility_manager_api_gateway_authorizer.id

  depends_on = [aws_api_gateway_resource.utility_manager_api_gateway_resource]
}

# Create a method response for the "hello" resource
resource "aws_api_gateway_method_response" "utility_manager_api_gateway_method_response" {
  rest_api_id = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  resource_id = aws_api_gateway_resource.utility_manager_api_gateway_resource.id
  http_method = aws_api_gateway_method.utility_manager_api_gateway_method.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = true
  }
}

# Create a lambda integration for the "hello" resource
resource "aws_api_gateway_integration" "utility_manager_api_gateway_integration" {
  rest_api_id             = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  resource_id             = aws_api_gateway_resource.utility_manager_api_gateway_resource.id
  http_method             = aws_api_gateway_method.utility_manager_api_gateway_method.http_method
  integration_http_method = "POST"
  type                    = "AWS"
  uri                     = aws_lambda_function.utility_manager_lambda_function.invoke_arn

  depends_on = [
    aws_api_gateway_method.utility_manager_api_gateway_method,
    aws_api_gateway_resource.utility_manager_api_gateway_resource
  ]
}

# Create an integration response for the "hello" resource
resource "aws_api_gateway_integration_response" "utility_manager_api_gateway_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  resource_id = aws_api_gateway_resource.utility_manager_api_gateway_resource.id
  http_method = aws_api_gateway_method.utility_manager_api_gateway_method.http_method
  status_code = aws_api_gateway_method_response.utility_manager_api_gateway_method_response.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = "'*'"
  }

  depends_on = [aws_api_gateway_integration.utility_manager_api_gateway_integration]
}
###################### end GET method ##############################


###################### OPTIONS method ##############################
# Create OPTIONS method for the "hello" resource
resource "aws_api_gateway_method" "utility_manager_api_gateway_method_options" {
  rest_api_id   = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  resource_id   = aws_api_gateway_resource.utility_manager_api_gateway_resource.id
  http_method   = "OPTIONS"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.utility_manager_api_gateway_authorizer.id
}

# Create integration for the OPTIONS method
resource "aws_api_gateway_integration" "utility_manager_api_gateway_integration_options" {
  rest_api_id             = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  resource_id             = aws_api_gateway_resource.utility_manager_api_gateway_resource.id
  http_method             = aws_api_gateway_method.utility_manager_api_gateway_method_options.http_method
  type                    = "AWS"
  integration_http_method = "POST"
  uri                     = aws_lambda_function.utility_manager_lambda_function.invoke_arn

}

# Create a method response for the OPTIONS method
resource "aws_api_gateway_method_response" "utility_manager_api_gateway_method_response_options" {
  rest_api_id = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  resource_id = aws_api_gateway_resource.utility_manager_api_gateway_resource.id
  http_method = aws_api_gateway_method.utility_manager_api_gateway_method_options.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"  = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
    "method.response.header.Access-Control-Allow-Headers" = true
  }
}

# Create an integration response for the OPTIONS method
resource "aws_api_gateway_integration_response" "utility_manager_api_gateway_integration_response_options" {
  rest_api_id = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  resource_id = aws_api_gateway_resource.utility_manager_api_gateway_resource.id
  http_method = aws_api_gateway_method.utility_manager_api_gateway_method_options.http_method
  status_code = aws_api_gateway_method_response.utility_manager_api_gateway_method_response_options.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"  = "'*'",
    "method.response.header.Access-Control-Allow-Methods" = "'GET,OPTIONS'",
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
  }

  depends_on = [aws_api_gateway_integration.utility_manager_api_gateway_integration_options]

}

###################### end OPTIONS method ##############################

# Create a deployment for the API Gateway
resource "aws_api_gateway_deployment" "utility_manager_api_gateway_deployment" {
  rest_api_id = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.utility_manager_api_gateway_resource.id,
      aws_api_gateway_method.utility_manager_api_gateway_method.id,
      aws_api_gateway_integration.utility_manager_api_gateway_integration.id,
      aws_api_gateway_method.utility_manager_api_gateway_method_options.id,
      aws_api_gateway_integration.utility_manager_api_gateway_integration_options.id,
    ]))
  }
  lifecycle {
    create_before_destroy = true
  }

  depends_on = [
    aws_api_gateway_integration.utility_manager_api_gateway_integration,
    aws_api_gateway_integration.utility_manager_api_gateway_integration_options
  ]
}

resource "aws_api_gateway_authorizer" "utility_manager_api_gateway_authorizer" {
  name            = "utility_manager_authorizer"
  rest_api_id     = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  type            = "COGNITO_USER_POOLS"
  provider_arns   = [aws_cognito_user_pool.utility_manager_user_pool.arn]
  identity_source = "method.request.header.Authorization"
}

# Create a stage for the API Gateway
resource "aws_api_gateway_stage" "utility_manager_api_gateway_stage" {
  rest_api_id   = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  stage_name    = "dev"
  deployment_id = aws_api_gateway_deployment.utility_manager_api_gateway_deployment.id

  depends_on = [aws_api_gateway_deployment.utility_manager_api_gateway_deployment]
}

# Create a permission for API Gateway to invoke the Lambda function
resource "aws_lambda_permission" "utility_manager_lambda_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.utility_manager_lambda_function.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.utility_manager_api_gateway.execution_arn}/*/*"

  depends_on = [aws_api_gateway_rest_api.utility_manager_api_gateway]
}

