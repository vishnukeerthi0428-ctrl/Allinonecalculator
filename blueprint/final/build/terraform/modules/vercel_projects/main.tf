# Module vercel_projects: Vercel projects website-{zone} and admin-{zone}: function region bom1/fra1, rewrites to api.{zone}, headers (CSP, HSTS), firewall rules, env (public only), log drain without bodies
resource "vercel_project" "site" {
  for_each  = toset(["website", "admin"])
  name      = "${each.key}-${lower(var.zone)}"
  framework = "vite"
  serverless_function_region = var.zone == "IN" ? "bom1" : "fra1"   # DEC-786; AU-296 verifies
}

