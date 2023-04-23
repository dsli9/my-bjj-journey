provider "google" {
  project = local.project_id
  region  = local.region
  zone    = local.zone
}

# Create cloud run job for each operation
resource "google_cloud_run_v2_job" "cloud_run_job" {
  for_each = toset(local.operations)

  name     = "bjj-${each.key}-cloudrun-job"
  location = local.region

  template {
    template {
      service_account = google_service_account.cloudrun_service_account.email
      containers {
        image = local.full_image_name

        env {
          name  = "TIER"
          value = local.tier
        }
        env {
          name  = "OPERATION"
          value = each.key
        }
        env {
          name  = "USER_TYPE"
          value = "machine"
        }
        env {
          name = local.db_host_var
          value_source {
            secret_key_ref {
              secret  = local.db_host_var
              version = "latest"
            }
          }
        }
        env {
          name = local.db_user_var
          value_source {
            secret_key_ref {
              secret  = local.db_user_var
              version = "latest"
            }
          }
        }
        env {
          name = local.db_pwd_var
          value_source {
            secret_key_ref {
              secret  = local.db_pwd_var
              version = "latest"
            }
          }
        }
        env {
          name = local.db_name_var
          value_source {
            secret_key_ref {
              secret  = local.db_name_var
              version = "latest"
            }
          }
        }
      }
    }
  }

  # Waits for the Cloud Run API to be enabled
  depends_on = [google_project_service.cloud_run]
}

# Create workflow that runs the cloud run jobs
resource "google_workflows_workflow" "workflows_bjj" {
  name            = "bjj-workflow"
  region          = local.region
  description     = "Workflow for BJJ data pipeline"
  service_account = google_service_account.workflows_service_account.id
  source_contents = <<-EOF
    - run_migrations:
        call: googleapis.run.v1.namespaces.jobs.run
        args:
            name: "namespaces/${local.project_id}/jobs/bjj-${local.migrations_op_name}-cloudrun-job"
            location: "${local.region}"

    - run_data_pipeline:
        call: googleapis.run.v1.namespaces.jobs.run
        args:
            name: "namespaces/${local.project_id}/jobs/bjj-${local.data_pipeline_op_name}-cloudrun-job"
            location: "${local.region}"

    - run_dbt:
        call: googleapis.run.v1.namespaces.jobs.run
        args:
            name: "namespaces/${local.project_id}/jobs/bjj-${local.dbt_op_name}-cloudrun-job"
            location: "${local.region}"

    - finish:
        return: "SUCCESS"
EOF

  depends_on = [google_cloud_run_v2_job.cloud_run_job]
}

# Schedule the cloud workflow
resource "google_cloud_scheduler_job" "bjj_workflows_scheduler" {
  name             = "bjj-workflow-schedule"
  description      = "Cloud scheduler job for bjj-workflow"
  schedule         = local.schedule
  time_zone        = "America/New_York"
  attempt_deadline = "320s"

  http_target {
    http_method = "POST"
    uri         = "https://workflowexecutions.googleapis.com/v1/${google_workflows_workflow.workflows_bjj.id}/executions"
    body = base64encode(
      jsonencode(
        {
          "callLogLevel" : "CALL_LOG_LEVEL_UNSPECIFIED"
        }
      )
    )

    oauth_token {
      service_account_email = google_service_account.scheduler_service_account.email
    }
  }

  depends_on = [google_workflows_workflow.workflows_bjj]
}
