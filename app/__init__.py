import importlib
import pkgutil
from flask import Flask
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

API_VERSION = "v1"

def create_app():
    app = Flask(__name__)

    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["MONGO_DB_NAME"] = os.getenv("MONGO_DB_NAME")

    routes_path = Path(__file__).parent / "routes"

    for module_info in pkgutil.iter_modules([str(routes_path)]):
        module_name = f"app.routes.{module_info.name}"
        module = importlib.import_module(module_name)

        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if getattr(attr, "__class__", None).__name__ == "Blueprint":
                blueprint_prefix = f"/{module_info.name}" if module_info.name != "main" else ""

                bp_prefix = getattr(module, "bp_prefix", blueprint_prefix)

                full_prefix = f"/auth/{API_VERSION}{bp_prefix}"
                app.register_blueprint(attr, url_prefix=full_prefix)

                print(f"Registered {module_info.name} → {full_prefix}")

    return app