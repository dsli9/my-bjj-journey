locals {
  project_id            = "bjj-dashboard-383320"
  region                = "us-east1"
  zone                  = "us-east1-b"
  docker_repo_id        = "bjj-docker-repo"
  image_name            = "bjj-journey"
  tier                  = "prod"
  migrations_op_name    = "migrations"
  data_pipeline_op_name = "data-pipeline"
  dbt_op_name           = "dbt"
  db_host_var           = "BJJ_DB_HOST"
  db_user_var           = "BJJ_DB_USER"
  db_pwd_var            = "BJJ_DB_PWD"
  db_name_var           = "BJJ_DB_DATABASE"
  schedule              = "0 12 * * SUN"
}

locals {
  full_image_name = "${local.region}-docker.pkg.dev/${local.project_id}/${local.docker_repo_id}/${local.image_name}:${local.tier}"
  operations      = [local.migrations_op_name, local.data_pipeline_op_name, local.dbt_op_name]
  secrets         = [local.db_host_var, local.db_user_var, local.db_pwd_var, local.db_name_var]
}
