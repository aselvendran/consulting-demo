provider "aws" {
  endpoints {
    sts = var.aws_endpoint
    rds = var.aws_endpoint
  }
}

data "aws_caller_identity" "current" {}

data "aws_availability_zones" "available" {
  state = "available"

}

locals {
  account_id = data.aws_caller_identity.current.account_id
}

resource "aws_rds_cluster_parameter_group" "rds_parameter_group" {
  name = "consulting-demo-cluster-pg"
  family = "aurora5.6"
  description = "Demo Purposes"
  parameter {
    name  = "character_set_server"
    value = "utf8"
  }

}

resource "aws_db_parameter_group" "instance_parameter_group" {
  name = "consulting-demo-db-pg"
  family = "aurora5.6"
  description = "Demo Purposes"
  parameter {
    name  = "character_set_server"
    value = "utf8"
  }
}

resource "aws_rds_cluster" "cluster" {

  cluster_identifier = "consulting-demo"
  engine = var.engine
  engine_version = var.engine_version
  availability_zones = data.aws_availability_zones.available.names
  database_name = var.database_name
  master_username = "admin"
  master_password = "admin"
  backup_retention_period = 5
  preferred_backup_window = "02:00-04:00"
  db_cluster_parameter_group_name = aws_rds_cluster_parameter_group.rds_parameter_group.name
  db_instance_parameter_group_name = aws_db_parameter_group.instance_parameter_group.name

}
