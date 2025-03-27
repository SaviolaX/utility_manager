resource "aws_cognito_user_pool" "utility_manager_user_pool" {
  name = "utility_manager_user_pool"
  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
  }
  auto_verified_attributes = ["email"]
}

resource "aws_cognito_user_pool_client" "utility_manager_user_pool_client" {
  name = "utility_manager_user_pool_client"

  user_pool_id        = aws_cognito_user_pool.utility_manager_user_pool.id
  generate_secret     = false
  explicit_auth_flows = ["ALLOW_USER_PASSWORD_AUTH", "ALLOW_REFRESH_TOKEN_AUTH"]
}
