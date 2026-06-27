terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}
provider "docker" {}

resource "docker_network" "anfa_net" {
  name = "anfa-network"
}

resource "docker_volume" "minio_data" {
  name = "anfa-minio-data-tf"
}

resource "docker_image" "minio" {
  name = "minio/minio:latest"
}

resource "docker_container" "minio" {
  name    = "anfa-minio-tf"
  image   = docker_image.minio.image_id
  command = ["server", "/data", "--console-address", ":9001"]
  restart = "unless-stopped"
  ports {
    internal = 9000
    external = 9010
  }
  ports {
    internal = 9001
    external = 9011
  }
  env = [
    "MINIO_ROOT_USER=anfa-admin",
    "MINIO_ROOT_PASSWORD=anfa-password-2026",
  ]
  volumes {
    volume_name    = docker_volume.minio_data.name
    container_path = "/data"
  }
  networks_advanced {
    name = docker_network.anfa_net.name
  }
  lifecycle {
    ignore_changes = [log_opts]
  }
}
