# staging / IN — provisioned from Sprint 0
terraform {
  backend "s3" {
    bucket       = "growth-tfstate-in"
    key          = "staging/in/terraform.tfstate"
    region       = "ap-south-1"
    encrypt      = true
    use_lockfile = true
  }
}

module "zone" {
  source = "../../../modules/zone_stack"
  env    = "staging"
  zone   = "IN"
}
