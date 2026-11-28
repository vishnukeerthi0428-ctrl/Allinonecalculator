# dev / EU — provisioned from Sprint 0
terraform {
  backend "s3" {
    bucket       = "growth-tfstate-eu"
    key          = "dev/eu/terraform.tfstate"
    region       = "eu-central-1"
    encrypt      = true
    use_lockfile = true
  }
}

module "zone" {
  source = "../../../modules/zone_stack"
  env    = "dev"
  zone   = "EU"
}
