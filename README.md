# Cisco Inventory Exporter

This project automates the process of connecting to Cisco IOS devices via SSH, collecting essential device information, and exporting it into an Excel file.

## 📌 Features
- Connects to multiple Cisco IOS devices over SSH using [Netmiko](https://github.com/ktbyers/netmiko).
- Retrieves:
  - IP address
  - Hostname
  - Model number
  - Serial number
  - Software (IOS) version
- Exports results to a formatted Excel file using [OpenPyXL](https://openpyxl.readthedocs.io/).
- Secure password input with [pwinput](https://pypi.org/project/pwinput/).

## 🚀 Requirements
- Python 3.7+
- Install dependencies:
  ```bash
  pip install netmiko openpyxl pwinput
