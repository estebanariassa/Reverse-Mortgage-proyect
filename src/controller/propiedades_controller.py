import os
import importlib.util


def _load_real_controller():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    real_path = os.path.join(base_dir, "controller.py", "propiedades_controller.py")
    spec = importlib.util.spec_from_file_location("propiedades_controller_real", real_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


_module = _load_real_controller()
PropiedadesController = getattr(_module, "PropiedadesController")


