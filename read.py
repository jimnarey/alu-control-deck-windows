import time
import threading

import hid

device_states = {}


def print_device_input(device, device_spec, report_size):
    global device_states
    path = device_spec["path"]
    vendor_id = device_spec["vendor_id"]
    product_id = device_spec["product_id"]
    previous_state = device_states.get(path, [])

    try:
        while True:
            current_state = device.read(report_size)
            if current_state and current_state != previous_state:
                print(f"vendor_id: {vendor_id}, product_id: {product_id}, path {path}")
                print(f"state: {current_state}")
                device_states[path] = current_state
                previous_state = current_state
            time.sleep(0.01)
    except Exception as e:
        print(f"Error reading from device {path}: {e}")


def read_all_devices(report_size: int):
    device_specs = hid.enumerate()
    print(f"Found {len(device_specs)} devices...")
    for device_spec in device_specs:
        try:
            device = hid.device()
            device.open_path(device_spec['path'])
            print(f"Opened device: {device_spec['manufacturer_string']} {device_spec['product_string']}")
            thread = threading.Thread(target=print_device_input, args=(device, device_spec, report_size))
            thread.start()

        except Exception as e:
            print(f"Failed to open device {device_spec['path']}: {e}")
