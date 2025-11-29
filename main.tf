terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.9.0"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

data "docker_registry_image" "my_app_image" {
  name = "localhost/test:v1"
  insecure_skip_verify = true
}

resource "docker_image" "app" {
  name = data.docker_registry_image.my_app_image.name
  pull_triggers = [data.docker_registry_image.my_app_image.sha256_digest]
}

resource "docker_container" "my_app" { 
    name  = "my_app"
    image = docker_image.app.name
    ports {
        internal = 5000
        external = 4000
    }
}
