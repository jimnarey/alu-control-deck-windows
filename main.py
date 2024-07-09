from optparse import OptionParser

import hid

import read


class GameController:

    def __init__(self, config):
        pass


def get_controllers(all_devices: list[dict], configs: dict[str, dict]) -> list[GameController]:
    controllers = []
    for dev in all_devices:
        if match := configs.get(f"{dev.get("vendor_id")}:{dev.get("product_id")}"):
            controllers.append(GameController(match))
    return controllers


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-r", "--read", dest="read", action="store_true", default=False)
    (options, args) = parser.parse_args()
    if options.read:
        read.read_all_devices()



