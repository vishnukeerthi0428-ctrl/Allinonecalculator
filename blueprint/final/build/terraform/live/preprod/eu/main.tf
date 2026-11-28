# preprod / EU — provisioned when the first EU tenant is contracted (DEC-772)
terraform {
  backend "s3" {
    bucket       = "growth-tfstate-eu"
    key          = "preprod/eu/terraform.tfstate"
    region       = "eu-central-1"
    encrypt      = true
    use_lockfile = true
  }
}

module "zone" {
  source = "../../../modules/zone_stack"
  env    = "preprod"
  zone   = "EU"
}
