resource "google_compute_firewall" "assignment_2_firewall" {
  name    = "assignment-2-firewall"
  network = "default"  # Replace with your desired network

  allow {
    protocol = "tcp"
    ports    = ["0-65535"]  # Allows all TCP ports
  }

  source_ranges = ["0.0.0.0/0"]  # Allows traffic from all IP addresses
}

