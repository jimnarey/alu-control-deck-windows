import time
import threading

import hid

import shared

device_states = {}
REPORT_SIZE = shared.get_config().get("report_size")


def print_device_input(device, device_info, report_size):
    global device_states
    path = device_info["path"]
    vendor_id = device_info["vendor_id"]
    product_id = device_info["product_id"]
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


def read_all_devices():
    devices = hid.enumerate()
    print(f"Found {len(devices)} devices...")
    for device_info in devices:
        try:
            device = hid.device()
            device.open_path(device_info['path'])
            print(f"Opened device: {device_info['manufacturer_string']} {device_info['product_string']}")
            report_size = 256
            thread = threading.Thread(target=print_device_input, args=(device, device_info, report_size))
            thread.start()

        except Exception as e:
            print(f"Failed to open device {device_info['path']}: {e}")
