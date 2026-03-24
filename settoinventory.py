import pynetbox

NETBOX_URL = "https://enter.netbox.url.here"
NETBOX_TOKEN = "n3tb0xAP1T0k3nH3r3"

nb = pynetbox.api(NETBOX_URL, token=NETBOX_TOKEN)
nb.http_session.verify = False

print("Enter serial numbers to update devices to 'Inventory' status. Type 'exit' to quit.")

while True:
    serial_number = input("Enter serial number: ").strip()
    if serial_number.lower() == "exit":
        print("Exiting...")
        break

    try:
        device = nb.dcim.devices.get(serial=serial_number)
        if device:
            device.status = "inventory"
            device.save()
            print(f"Device with serial '{serial_number}' updated to Inventory status.")
        else:
            print(f"No device found with serial '{serial_number}'.")
    except Exception as e:
        print(f"Error updating device with serial '{serial_number}': {e}")