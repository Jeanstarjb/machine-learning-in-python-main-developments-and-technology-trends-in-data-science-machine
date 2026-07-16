terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.region
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "3.14.2"

  name                 = "ml-platform-vpc"
  cidr                 = "10.0.0.0/16"
  azs                  = ["${var.region}a", "${var.region}b"]
  private_subnets      = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets       = ["10.0.101.0/24", "10.0.102.0/24"]
  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "18.5.0"

  cluster_name    = "ml-platform-cluster"
  cluster_version = "1.24"
  vpc_id          = module.vpc.vpc_id
  subnet_ids      = module.vpc.private_subnets

  eks_managed_node_groups = {
    default = {
      min_size     = 1
      max_size     = 5
      desired_size = 2

      instance_types = [var.instance_type]
      capacity_type  = "SPOT"
    }
  }
}

resource "aws_rds_cluster" "ml_platform_db" {
  cluster_identifier      = "ml-platform-db"
  engine                  = "aurora-postgresql"
  engine_version          = "13.7"
  database_name           = "mlplatform"
  master_username         = var.db_username
  master_password         = var.db_password
  backup_retention_period = 7
  preferred_backup_window = "07:00-09:00"
  skip_final_snapshot     = true
  vpc_security_group_ids  = [module.eks.cluster_primary_security_group_id]
  db_subnet_group_name    = aws_db_subnet_group.ml_platform.name
  storage_encrypted       = true
}

resource "aws_db_subnet_group" "ml_platform" {
  name       = "ml-platform-db-subnet"
  subnet_ids = module.vpc.private_subnets
}

resource "aws_s3_bucket" "ml_models" {
  bucket = "ml-platform-models-${var.environment}"
  acl    = "private"

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

resource "aws_ecr_repository" "backend" {
  name                 = "ml-platform-backend"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "frontend" {
  name                 = "ml-platform-frontend"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
