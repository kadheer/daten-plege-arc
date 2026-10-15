# main.tf
#
# Minimale Terraform-Konfiguration für den CI/CD-Test.
# Ich hab hier absichtlich einen null_resource genommen -
# der macht nichts, aber man sieht, dass die Pipeline läuft.
# Echte Infrastruktur kommt später dazu.

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}

resource "null_resource" "data_pflege_arc" {
  triggers = {
    value = "data-pflege-arc"
  }
}
