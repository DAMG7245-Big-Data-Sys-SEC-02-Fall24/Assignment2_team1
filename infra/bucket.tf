resource "google_storage_bucket" "assignment2" {
  name          = "assignment2-damg7245-t1"  # Bucket name
  location      = "us-east1"  # Region: US East (South Carolina)
  storage_class = "STANDARD"  # Storage class: Standard
  
  # Enable uniform access control
  uniform_bucket_level_access = true
}
