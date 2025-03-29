resource "aws_cognito_user_pool" "utility_manager_user_pool" {
  name = "utility_manager_user_pool"
  password_policy {
    minimum_length    = 6
    require_lowercase = false
    require_numbers   = false
    require_symbols   = false
    require_uppercase = false
  }
  auto_verified_attributes = ["email"]
  username_attributes      = ["email"]
}

resource "aws_cognito_user_pool_client" "utility_manager_user_pool_client" {
  name = "utility_manager_user_pool_client"

  user_pool_id        = aws_cognito_user_pool.utility_manager_user_pool.id
  generate_secret     = false
  explicit_auth_flows = ["ALLOW_USER_SRP_AUTH", "ALLOW_USER_PASSWORD_AUTH", "ALLOW_REFRESH_TOKEN_AUTH"]
}
