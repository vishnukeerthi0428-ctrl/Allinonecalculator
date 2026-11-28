variable "env" { type = string }
variable "zone" {
  type = string
  validation {
    condition     = contains(["IN", "EU"], var.zone)
    error_message = "zone must be IN or EU (DEC-772)."
  }
}
variable "tags" {
  type    = map(string)
  default = {}
}
