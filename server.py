import pathlib
import sys

PROJECT_ROOT = pathlib.Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from translation_server import main

if __name__ == "__main__":
    main()