# Module zone_stack: Composition of one residency zone (IN or EU) for one environment
terraform {
  required_version = ">= 1.9"   # OpenTofu 1.9+/Terraform 1.9+ (ADR-012/ADR-051); verify at implementation (27 Nov 2026)
  required_providers {
    aws      = { source = "hashicorp/aws", version = "~> 5.80" }
    supabase = { source = "supabase/supabase", version = "~> 1.5" }
    vercel   = { source = "vercel/vercel", version = "~> 2.0" }
  }
}

module "aws_network" {
  source = "../aws_network"
  env    = var.env
  zone   = var.zone
  tags   = local.tags
}

module "aws_security_baseline" {
  source = "../aws_security_baseline"
  env    = var.env
  zone   = var.zone
  tags   = local.tags
}

module "aws_data" {
  source = "../aws_data"
  env    = var.env
  zone   = var.zone
  tags   = local.tags
}

module "aws_compute" {
  source = "../aws_compute"
  env    = var.env
  zone   = var.zone
  tags   = local.tags
}

module "aws_edge_api" {
  source = "../aws_edge_api"
  env    = var.env
  zone   = var.zone
  tags   = local.tags
}

module "aws_dr_standby" {
  source = "../aws_dr_standby"
  env    = var.env
  zone   = var.zone
  tags   = local.tags
}

module "aws_observability" {
  source = "../aws_observability"
  env    = var.env
  zone   = var.zone
  tags   = local.tags
}

module "supabase_project" {
  source = "../supabase_project"
  env    = var.env
  zone   = var.zone
  tags   = local.tags
}

module "vercel_projects" {
  source = "../vercel_projects"
  env    = var.env
  zone   = var.zone
  tags   = local.tags
}

locals {
  tags = { product = "commercial", env = var.env, zone = var.zone, data_residency = var.zone }
}

