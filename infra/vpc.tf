resource "google_compute_subnetwork" "assignment_2_subnet" {
  name          = "assignment-2-subnet"
  ip_cidr_range = "10.0.0.0/24"
  region        = "us-east1"
  network       = "default"

}