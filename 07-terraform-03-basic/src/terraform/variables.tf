variable "yandex_cloud_id" {
  default = "b1gn303gl4s828djdqfi"
}

variable "yandex_folder_id" {
  default = "b1gprhi83f991tp8b54f"
}

variable "centos-7-base" {
  default = "fd87hrmj6opa30n655a6"
}

locals {
  instance_count = {
    "prod"=2
    "stage"=1
  }
  vm_cores = {
    "prod"=2
    "stage"=1
  }
  vm_memory = {
    "prod"=2
    "stage"=1
  }
  vm_foreach = {
    prod = {
      "3" = { cores = "2", memory = "2" },
      "2" = { cores = "2", memory = "2" }
    }
	stage = {
      "1" = { cores = "1", memory = "1" }
    }
  }
}