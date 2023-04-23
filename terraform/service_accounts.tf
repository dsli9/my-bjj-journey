# Create service account for cloud run
resource "google_service_account" "cloudrun_service_account" {
  account_id   = "bjj-cloudrun-sa"
  display_name = "BJJ Cloud Run Service Account"
}

# Create service account for workflow
resource "google_service_account" "workflows_service_account" {
  account_id   = "bjj-workflows-sa"
  display_name = "BJJ Workflows Service Account"
}

# Create service account for cloud scheduler
resource "google_service_account" "scheduler_service_account" {
  account_id   = "bjj-scheduler-sa"
  display_name = "BJJ Cloud Scheduler Service Account"
}

# Grant secret manager accessor role to cloud run service account for secrets
resource "google_secret_manager_secret_iam_member" "member" {
  for_each  = toset(local.secrets)
  secret_id = each.key
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloudrun_service_account.email}"
}

# Grant workflows service account permission to invoke cloud run jobs
resource "google_cloud_run_v2_job_iam_member" "invoker" {
  for_each = toset(local.operations)

  location = local.region
  name     = google_cloud_run_v2_job.cloud_run_job["${each.key}"].name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.workflows_service_account.email}"
  depends_on = [
    google_cloud_run_v2_job.cloud_run_job
  ]
}

# Grant workflows service account permission to view cloud run jobs
resource "google_cloud_run_v2_job_iam_member" "viewer" {
  for_each = toset(local.operations)

  location = local.region
  name     = google_cloud_run_v2_job.cloud_run_job["${each.key}"].name
  role     = "roles/run.viewer"
  member   = "serviceAccount:${google_service_account.workflows_service_account.email}"
  depends_on = [
    google_cloud_run_v2_job.cloud_run_job
  ]
}

# Grant cloud scheduler service account permission to invoke workflows
resource "google_project_iam_member" "scheduler_account_role" {
  project = local.project_id
  role    = "roles/workflows.invoker"
  member  = "serviceAccount:${google_service_account.scheduler_service_account.email}"
  depends_on = [
    google_service_account.scheduler_service_account
  ]
}
