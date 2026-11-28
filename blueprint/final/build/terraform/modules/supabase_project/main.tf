# Module supabase_project: Supabase project in the zone region, PITR add-on, network restrictions, SSL enforcement, Data API disabled/ge not exposed, log drain (verify provider resources)
resource "supabase_project" "this" {
  organization_id   = var.supabase_org_id
  name              = "growth-${var.env}-${lower(var.zone)}"
  database_password = var.db_bootstrap_password   # rotated immediately; app roles created by migration V0001
  region            = var.zone == "IN" ? "ap-south-1" : "eu-central-1"   # verify Supabase region identifiers
  lifecycle { prevent_destroy = true }
}

resource "supabase_settings" "this" {
  project_ref = supabase_project.this.id
  api = jsonencode({ db_schema = "graphql_public", max_rows = 1 })   # schema ge never exposed (SA-01)
}

