# Purpose: This file is used to create the API Gateway for the Utility Manager application.

# Create a REST API
resource "aws_api_gateway_rest_api" "utility_manager_api_gateway" {
  name        = "utility_manager_api_gateway"
  description = "Utility Manager API Gateway"
}

# Create a "count" resource
resource "aws_api_gateway_resource" "utility_manager_api_gateway_resource__count" {
  rest_api_id = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  parent_id   = aws_api_gateway_rest_api.utility_manager_api_gateway.root_resource_id
  path_part   = "count"

  depends_on = [aws_api_gateway_rest_api.utility_manager_api_gateway]
}

###################### GET method ##############################
# Create a GET method for the "count" resource
resource "aws_api_gateway_method" "utility_manager_api_gateway_get_method" {
  rest_api_id      = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  resource_id      = aws_api_gateway_resource.utility_manager_api_gateway_resource__count.id
  http_method      = "GET"
  authorization    = "COGNITO_USER_POOLS"
  api_key_required = false
  authorizer_id    = aws_api_gateway_authorizer.utility_manager_api_gateway_authorizer.id

  depends_on = [aws_api_gateway_resource.utility_manager_api_gateway_resource__count]
}

# Create a method response for the "count" resource
resource "aws_api_gateway_method_response" "utility_manager_api_gateway_get_method_response" {
  rest_api_id = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  resource_id = aws_api_gateway_resource.utility_manager_api_gateway_resource__count.id
  http_method = aws_api_gateway_method.utility_manager_api_gateway_get_method.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = true
  }
}

# Create a lambda integration for the "count" resource
resource "aws_api_gateway_integration" "utility_manager_api_gateway_get_integration" {
  rest_api_id             = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  resource_id             = aws_api_gateway_resource.utility_manager_api_gateway_resource__count.id
  http_method             = aws_api_gateway_method.utility_manager_api_gateway_get_method.http_method
  integration_http_method = "POST"
  type                    = "AWS"
  uri                     = aws_lambda_function.utility_manager_lambda_function.invoke_arn

  depends_on = [
    aws_api_gateway_method.utility_manager_api_gateway_get_method,
    aws_api_gateway_resource.utility_manager_api_gateway_resource__count
  ]
}

# Create an integration response for the "count" resource
resource "aws_api_gateway_integration_response" "utility_manager_api_gateway_get_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  resource_id = aws_api_gateway_resource.utility_manager_api_gateway_resource__count.id
  http_method = aws_api_gateway_method.utility_manager_api_gateway_get_method.http_method
  status_code = aws_api_gateway_method_response.utility_manager_api_gateway_get_method_response.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = "'*'"
  }

  depends_on = [aws_api_gateway_integration.utility_manager_api_gateway_get_integration]
}
###################### end GET method ##############################


###################### POST method ##############################

#Create a POST method for the "count" resource
resource "aws_api_gateway_method" "utility_manager_api_gateway_post_method" {
  rest_api_id      = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  resource_id      = aws_api_gateway_resource.utility_manager_api_gateway_resource__count.id
  http_method      = "POST"
  authorization    = "COGNITO_USER_POOLS"
  api_key_required = false
  authorizer_id    = aws_api_gateway_authorizer.utility_manager_api_gateway_authorizer.id

  depends_on = [aws_api_gateway_resource.utility_manager_api_gateway_resource__count]
}

# Create a method response for the "count" resource
resource "aws_api_gateway_method_response" "utility_manager_api_gateway_post_method_response" {
  rest_api_id = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  resource_id = aws_api_gateway_resource.utility_manager_api_gateway_resource__count.id
  http_method = aws_api_gateway_method.utility_manager_api_gateway_post_method.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = true
  }
}

# Create a lambda integration for the "count" resource
resource "aws_api_gateway_integration" "utility_manager_api_gateway_post_integration" {
  rest_api_id             = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  resource_id             = aws_api_gateway_resource.utility_manager_api_gateway_resource__count.id
  http_method             = aws_api_gateway_method.utility_manager_api_gateway_post_method.http_method
  integration_http_method = "POST"
  type                    = "AWS"
  uri                     = aws_lambda_function.utility_manager_lambda_function.invoke_arn

  depends_on = [
    aws_api_gateway_method.utility_manager_api_gateway_get_method,
    aws_api_gateway_resource.utility_manager_api_gateway_resource__count
  ]
}

# Create an integration response for the "count" resource
resource "aws_api_gateway_integration_response" "utility_manager_api_gateway_post_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  resource_id = aws_api_gateway_resource.utility_manager_api_gateway_resource__count.id
  http_method = aws_api_gateway_method.utility_manager_api_gateway_post_method.http_method
  status_code = aws_api_gateway_method_response.utility_manager_api_gateway_post_method_response.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = "'*'"
  }

  depends_on = [aws_api_gateway_integration.utility_manager_api_gateway_post_integration]
}

###################### end POST method ##############################

###################### OPTIONS method ##############################
# Create OPTIONS method for the "count" resource
resource "aws_api_gateway_method" "utility_manager_api_gateway_post_method_options" {
  rest_api_id   = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  resource_id   = aws_api_gateway_resource.utility_manager_api_gateway_resource__count.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

# Create integration for the OPTIONS method
resource "aws_api_gateway_integration" "utility_manager_api_gateway_post_method_integration_options" {
  rest_api_id = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  resource_id = aws_api_gateway_resource.utility_manager_api_gateway_resource__count.id
  http_method = aws_api_gateway_method.utility_manager_api_gateway_post_method_options.http_method
  type        = "MOCK"
  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

# Create a method response for the OPTIONS method
resource "aws_api_gateway_method_response" "utility_manager_api_gateway_post_method_response_options" {
  rest_api_id = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  resource_id = aws_api_gateway_resource.utility_manager_api_gateway_resource__count.id
  http_method = aws_api_gateway_method.utility_manager_api_gateway_post_method_options.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"  = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
    "method.response.header.Access-Control-Allow-Headers" = true
  }
}

# Create an integration response for the OPTIONS method
resource "aws_api_gateway_integration_response" "utility_manager_api_gateway_integration_post_response_options" {
  rest_api_id = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  resource_id = aws_api_gateway_resource.utility_manager_api_gateway_resource__count.id
  http_method = aws_api_gateway_method.utility_manager_api_gateway_post_method_options.http_method
  status_code = aws_api_gateway_method_response.utility_manager_api_gateway_post_method_response_options.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"  = "'*'",
    "method.response.header.Access-Control-Allow-Methods" = "'GET,POST,OPTIONS'",
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
  }

  depends_on = [aws_api_gateway_integration.utility_manager_api_gateway_post_method_integration_options]

}

###################### end OPTIONS method ##############################


# Create a deployment for the API Gateway
resource "aws_api_gateway_deployment" "utility_manager_api_gateway_deployment" {
  rest_api_id = aws_api_gateway_rest_api.utility_manager_api_gateway.id
  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.utility_manager_api_gateway_resource__count.id,
      aws_api_gateway_method.utility_manager_api_gateway_get_method.id,
      aws_api_gateway_integration.utility_manager_api_gateway_get_integration.id,
      aws_api_gateway_method.utility_manager_api_gateway_post_method.id,
      aws_api_gateway_integration.utility_manager_api_gateway_post_integration.id,
      aws_api_gateway_method.utility_manager_api_gateway_post_method_options.id,
      aws_api_gateway_integration.utility_manager_api_gateway_post_method_integration_options.id,
    ]))
  }
  lifecycle {
    create_before_destroy = true
  }

  depends_on = [
    aws_api_gateway_integration.utility_manager_api_gateway_get_integration,
    aws_api_gateway_integration.utility_manager_api_gateway_post_integration,
    aws_api_gateway_integration.utility_manager_api_gateway_post_method_integration_options,
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

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway_logs.arn
    format          = "$context.requestId $context.httpMethod $context.path"
  }

  depends_on = [aws_api_gateway_deployment.utility_manager_api_gateway_deployment]
}

resource "aws_cloudwatch_log_group" "api_gateway_logs" {
  name              = "/aws/apigateway/utility-manager-logs"
  retention_in_days = 7
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

