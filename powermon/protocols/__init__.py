import importlib
import logging
import pkgutil
from enum import Enum, auto

log = logging.getLogger("protocols")


class ResponseType(Enum):
    DEFAULT = auto()
    ACK = auto()
    MULTIVALUED = auto()
    INDEXED = auto()


def get_protocol(protocol):
    """
    Get the protocol based on the protocol name
    """

    log.debug(f"Protocol {protocol}")
    if protocol is None:
        return None
    protocol_id = protocol.lower()
    # Try to import the protocol module with the supplied name (may not exist)
    try:
        proto_module = importlib.import_module("powermon.protocols." + protocol_id, ".")
    except ModuleNotFoundError:
        log.error(f"No module found for protocol {protocol_id}")
        return None
    # Find the protocol class - classname must be the same as the protocol_id
    try:
        protocol_class = getattr(proto_module, protocol_id)
    except AttributeError:
        log.error(f"Module {proto_module} has no attribute {protocol_id}")
        return None
    # Return the instantiated class
    return protocol_class()


def list_protocols():
    # print("outputs list protocols")
    pkgpath = __file__
    pkgpath = pkgpath[: pkgpath.rfind("/")]
    pkgpath += "/../protocols"
    # print(pkgpath)
    result = {}
    result["_command"] = "protocols help"
    result["_command_description"] = "List available protocol modules"
    for _, name, _ in pkgutil.iter_modules([pkgpath]):
        # print(name)
        try:
            _module_class = importlib.import_module("powermon.protocols." + name, ".")
            _module = getattr(_module_class, name)
        except ModuleNotFoundError as e:
            log.info(f"Error in module {name}: {e}")
            # result[name] = (str(_module()), "ERROR", "")
            continue
        except AttributeError as e:
            log.info(f"Error in module {name}: {e}")
            # result[name] = (name, "ERROR", "")
            continue
        # print(_module())
        result[name] = (str(_module()), "", "")
    # print(result)
    return result
