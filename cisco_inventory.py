from netmiko import ConnectHandler
from openpyxl import Workbook
import pwinput  # pip install pwinput
 
def get_cisco_device_info(ip, username, password):
    device = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': username,
        'password': password,
        'secret': password,
    }
   
    connection = ConnectHandler(**device)
    connection.enable()
   
    # Get hostname from device prompt
    prompt = connection.find_prompt()
    hostname = prompt.replace('#', '').strip()
   
    output = connection.send_command("show version")
    connection.disconnect()
   
    info = {'ip': ip, 'hostname': hostname, 'model_number': '', 'serial_number': '', 'software_version': ''}
   
    for line in output.splitlines():
        line = line.strip()
       
        # Model number (robust)
        if "Model number" in line:
            parts = line.split(":")
            if len(parts) > 1:
                info['model_number'] = parts[1].strip()
       
        # Serial number
        if "System serial number" in line or "Processor board ID" in line:
            info['serial_number'] = line.split()[-1]
       
        # Software version
        if "Cisco IOS Software" in line and "Version" in line:
            try:
                info['software_version'] = line.split("Version")[1].split(",")[0].strip()
            except IndexError:
                continue
   
    return info
 
# -------------------------------
# Main program for multiple IPs
# -------------------------------
if _name_ == "_main_":
    ips = input("Enter Cisco device IPs (comma separated): ").split(",")
    username = input("Enter SSH username: ")
    password = pwinput.pwinput("Enter SSH password: ")  # shows stars
   
    results = []
    for ip in ips:
        ip = ip.strip()
        print(f"Connecting to {ip}...")
        info = get_cisco_device_info(ip, username, password)
        results.append(info)
   
    # Write to Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Cisco Devices"
   
    # Header
    headers = ["IP", "Hostname", "Model Number", "Serial Number", "Software Version"]
    ws.append(headers)
   
    for r in results:
        ws.append([
            r['ip'],
            r['hostname'],
            r['model_number'],
            r['serial_number'],
            r['software_version']
        ])
   
    filename = input("Enter the Excel filename: ").strip()
    if not filename.endswith(".xlsx"):
        filename += ".xlsx"
    wb.save(filename)
   
    print(f"\nResults saved to {filename}")
