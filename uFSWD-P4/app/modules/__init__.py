from app import server, server_logger
import importlib

modules = ["index",
           "catalog",
           "users"]


def registerBlueprints(module_name):
    """Registers blueprint modules based on the module name

    :param: module_name
    :type: string
        Module name
    """
    module = importlib.import_module(
        "app.modules." + module_name, package=None)
    bp = getattr(module, module_name)
    server_logger.info("Registering module: " + module_name)
    if bp.name == "index":
        server.register_blueprint(bp)
    else:
        server.register_blueprint(bp, url_prefix='/' + bp.name)


[registerBlueprints(mod) for mod in modules]
