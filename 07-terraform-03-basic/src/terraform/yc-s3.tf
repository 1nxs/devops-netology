terraform {
// Загрузка tfstate в Object Storage
  backend "s3" {
  endpoint = "storage.yandexcloud.net"
  bucket = "virt73"
  region = "ru-central1"
  key = "s3/terraform.tfstate"

  skip_region_validation = true
  skip_credentials_validation = true
  }
}
