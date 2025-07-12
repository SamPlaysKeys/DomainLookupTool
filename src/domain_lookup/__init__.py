from .cli import main                         # export the CLI entry
from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version("domainlookup")
except PackageNotFoundError:
    __version__ = "0.0.0"
__all__ = ["main", "__version__"]
