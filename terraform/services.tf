# Enable the Cloud Run API
resource "google_project_service" "cloud_run" {
  service            = "run.googleapis.com"
}

# Enable the Workflows api
resource "google_project_service" "workflows" {
  service                    = "workflows.googleapis.com"
  disable_dependent_services = true
}

# Enable the cloud scheduler API
resource "google_project_service" "scheduler" {
  service            = "cloudscheduler.googleapis.com"
}
