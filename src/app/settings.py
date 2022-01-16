import os.path as os_path

from pathlib import Path
from typing  import Dict


ROOT_DIR: Path = Path( __file__ ).parent

STATIC_DIRS: Dict[ str, str ] = { 
    'static': os_path.join( ROOT_DIR.parent, 'client', 'build' )
}

DEV_HOST: str = '0.0.0.0'
DEV_PORT: int = 8080