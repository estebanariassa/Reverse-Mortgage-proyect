import os
import importlib.util


def _load_real_controller():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    real_path = os.path.join(base_dir, "controller.py", "hipotecas_controller.py")
    spec = importlib.util.spec_from_file_location("hipotecas_controller_real", real_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


_module = _load_real_controller()
HipotecasController = getattr(_module, "HipotecasController")


