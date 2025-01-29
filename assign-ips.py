import pynetbox

nb = pynetbox.api(url="{URL}", token="{APIKEY}")

devices = nb.dcim.devices.all()
addresses = nb.ipam.ip_addresses.all()

serial_to_device = {device.serial: device for device in devices}

for address in addresses:
    desc = address.description
    ipid = address.id

    if desc in serial_to_device:
        device = serial_to_device[desc]
        deviceid = device.id

        interfaces = nb.dcim.interfaces.filter(device_id=deviceid)
        interface_50 = next((iface for iface in interfaces if iface.name == '50'), None)

        if interface_50:
            interfaceid = interface_50.id

            address.assigned_object_id = interfaceid
            address.assigned_object_type = 'dcim.interface'
            address.save()
            print(f"Assigned IP {ipid} to Interface {interfaceid} on Device {deviceid}")

            device.primary_ip4 = address
            device.save()
            print(f"Set IP {ipid} as primary for Device {deviceid}")
        else:
            print(f"Interface 50 not found for Device {deviceid}")
    else:
        print(f"No match for Address: {desc}, ID: {ipid}")