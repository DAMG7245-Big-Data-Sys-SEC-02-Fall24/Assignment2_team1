# Create a new PostgreSQL database instance named "assignment2"
resource "google_sql_database_instance" "postgres_instance" {
  name             = "assignment2-postgres"
  database_version = "POSTGRES_13"
  region           = "us-east1"

  settings {
    tier = "db-f1-micro"  # Adjust according to your needs

    ip_configuration {
      ipv4_enabled = true

      authorized_networks {
        name  = "public-ip-whitelist"
        value = "0.0.0.0/0"  # Replace with the public IP to whitelist
      }
    }
  }

  deletion_protection = false  # Set to true for production
}

# Create a new database within the "assignment2-postgres" instance
resource "google_sql_database" "default" {
  name      = "assignment2"  # Database name
  instance  = google_sql_database_instance.postgres_instance.name
  charset   = "UTF8"
  collation = "en_US.UTF8"
}

# Generate a random password for the database user
resource "random_password" "db_password" {
  length           = 16
  special          = false
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

# Create a new PostgreSQL user with the randomly generated password
resource "google_sql_user" "default" {
  name     = "admin"
  instance = google_sql_database_instance.postgres_instance.name
  password = random_password.db_password.result
}

# Provision the schema for the Users table to store login details
resource "null_resource" "schema_setup" {
  depends_on = [google_sql_database.default, google_sql_user.default]

  provisioner "local-exec" {
    command = <<EOT
      PGPASSWORD=${random_password.db_password.result} psql -h ${google_sql_database_instance.postgres_instance.public_ip_address} -U admin -d assignment2 -f schema.sql
    EOT
  }
}

# Outputs for connection and credentials
output "postgres_instance_connection_name" {
  value = google_sql_database_instance.postgres_instance.connection_name
}

output "postgres_public_ip" {
  value = google_sql_database_instance.postgres_instance.public_ip_address
}

output "database_username" {
  value = google_sql_user.default.name
}

output "database_password" {
  value     = random_password.db_password.result
  sensitive = true
}

# Store the database credentials in a local file
resource "local_file" "db_credentials" {
  content = <<EOT
Database Host: ${google_sql_database_instance.postgres_instance.public_ip_address}
Database Name: ${google_sql_database.default.name}
Database Username: ${google_sql_user.default.name}
Database Password: ${random_password.db_password.result}
EOT
  filename = "${path.module}/db_credentials.txt"

  # Set permissions so only the owner can read and write the file
  file_permission = "0600"
}
