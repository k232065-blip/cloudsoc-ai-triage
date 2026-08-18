resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "${var.project_name}-vpc"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project_name}-igw"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block               = var.public_subnet_cidr
  availability_zone         = var.availability_zone
  map_public_ip_on_launch  = true

  tags = {
    Name = "${var.project_name}-public-subnet"
  }
}

resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidr
  availability_zone = var.availability_zone

  tags = {
    Name = "${var.project_name}-private-subnet"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${var.project_name}-public-rt"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

resource "aws_s3_bucket" "soc_bucket" {
  bucket = "${var.project_name}-bucket-${data.aws_caller_identity.current.account_id}"

  tags = {
    Name = "${var.project_name}-bucket"
  }
}

resource "aws_s3_bucket_versioning" "soc_bucket_versioning" {
  bucket = aws_s3_bucket.soc_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "soc_bucket_encryption" {
  bucket = aws_s3_bucket.soc_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "soc_bucket_block" {
  bucket = aws_s3_bucket.soc_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

data "aws_caller_identity" "current" {}

# ---- IAM Role #1: Admin-Limited (least-privilege, no IAM/Billing) ----
resource "aws_iam_policy" "admin_limited_policy" {
  name = "${var.project_name}-AdminLimited-Policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "AllowCoreServices"
        Effect   = "Allow"
        Action   = ["ec2:*", "s3:*", "vpc:*", "cloudtrail:*", "guardduty:*", "logs:*"]
        Resource = "*"
      },
      {
        Sid      = "DenyIAMAndBilling"
        Effect   = "Deny"
        Action   = ["iam:*", "organizations:*", "account:*", "billing:*"]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role" "admin_limited_role" {
  name = "${var.project_name}-AdminLimited-Role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root" }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "admin_limited_attach" {
  role       = aws_iam_role.admin_limited_role.name
  policy_arn = aws_iam_policy.admin_limited_policy.arn
}

# ---- IAM Role #2: Read-Only Auditor (SecurityAudit managed policy) ----
resource "aws_iam_role" "readonly_auditor_role" {
  name = "${var.project_name}-ReadOnly-Auditor-Role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root" }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "readonly_auditor_attach" {
  role       = aws_iam_role.readonly_auditor_role.name
  policy_arn = "arn:aws:iam::aws:policy/SecurityAudit"
}
