# Define the variables for the AWS provider
variable "region" {
  description = "The region in which the resources will be created"
  default     = "eu-central-1"
}

# Define the variables for the S3 bucket
variable "bucket_name" {
  description = "The name of the S3 bucket to create"
  default     = "frontend-utility-manager-web-app"
}

variable "force_destroy" {
  description = "A boolean flag to enable/disable forceful deletion of the bucket"
  default     = true
}

variable "tag_environment" {
  description = "The environment in which the resources will be created"
  default     = "Dev"
}

variable "tag_name" {
  description = "The name of the S3 bucket"
  default     = "Utility Manage Web App Bucket"
}

variable "index_document" {
  description = "The index document for the S3 bucket"
  default     = "index.html"
}

variable "bucket_block_public_acls" {
  description = "A boolean flag to enable/disable public ACLs"
  default     = false
}

variable "bucket_block_public_policy" {
  description = "A boolean flag to enable/disable public bucket policies"
  default     = false
}
variable "bucket_ignore_public_acls" {
  description = "A boolean flag to enable/disable ignoring public ACLs"
  default     = false
}
variable "bucket_restrict_public_buckets" {
  description = "A boolean flag to enable/disable restricting public buckets"
  default     = false
}

