# Create an S3 bucket to store the web app files
resource "aws_s3_bucket" "frontend_bucket" {
  bucket        = var.bucket_name
  force_destroy = var.force_destroy # if the object is deleted, it will be permanently deleted

  tags = {
    Name        = var.tag_name
    Environment = var.tag_environment
  }
}

# Remove checks from bucket block public access
resource "aws_s3_bucket_public_access_block" "frontend_bucket_public_access_block" {
  bucket = aws_s3_bucket.frontend_bucket.id

  block_public_acls       = var.bucket_block_public_acls
  block_public_policy     = var.bucket_block_public_policy
  ignore_public_acls      = var.bucket_ignore_public_acls
  restrict_public_buckets = var.bucket_restrict_public_buckets

  # Ensure that the public access block is removed after the bucket is deleted
  depends_on = [aws_s3_bucket.frontend_bucket]
}

# Create a bucket policy to allow public read access to all objects in the bucket
resource "aws_s3_bucket_policy" "frontend_bucket_policy" {
  bucket = aws_s3_bucket.frontend_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "arn:aws:s3:::${aws_s3_bucket.frontend_bucket.id}/*"
      }
    ]
  })

  # Ensure that the bucket policy is created after the bucket is created
  depends_on = [aws_s3_bucket_public_access_block.frontend_bucket_public_access_block]
}

# Upload the web app files to the S3 bucket
resource "aws_s3_object" "frontend_object" {
  bucket = aws_s3_bucket.frontend_bucket.id

  for_each = fileset("../frontend/dist", "**/*")

  key    = each.value
  source = "../dist/${each.value}"

  # Set the content type for the files
  content_type = lookup({
    "html"  = "text/html",
    "css"   = "text/css",
    "js"    = "application/javascript",
    "png"   = "image/png",
    "jpg"   = "image/jpeg",
    "jpeg"  = "image/jpeg",
    "gif"   = "image/gif",
    "ico"   = "image/x-icon",
    "svg"   = "image/svg+xml",
    "json"  = "application/json",
    "woff"  = "font/woff",
    "woff2" = "font/woff2",
    "ttf"   = "font/ttf"
  }, regex("\\.([^.]+)$", each.value)[0], "application/octet-stream")

  depends_on = [aws_s3_bucket.frontend_bucket]
}

# Configure the S3 bucket as a static website
resource "aws_s3_bucket_website_configuration" "frontend_bucket_website_configuration" {
  bucket = aws_s3_bucket.frontend_bucket.id

  index_document {
    suffix = var.index_document
  }

  depends_on = [aws_s3_object.frontend_object]
}





