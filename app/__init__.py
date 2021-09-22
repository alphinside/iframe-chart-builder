import toml

project_meta = toml.load("pyproject.toml")
__version__ = f"v{project_meta['tool']['poetry']['version']}"
