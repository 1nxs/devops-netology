resource "yandex_compute_instance" "srv72-01" {
  name                      = "srv72-01"
  zone                      = "ru-central1-a"
  hostname                  = "srv72-01.netology.lab"
  allow_stopping_for_update = true

  resources {
    cores  = 2
    memory = 2
  }
}
