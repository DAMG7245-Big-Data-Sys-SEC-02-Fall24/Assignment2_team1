provider "google" {
  project     = "damg7245-big-data-sys-436220"
  region      = "us-east1"
  credentials = file(var.google_credentials)
}

variable "google_credentials" {
  type = string
}
