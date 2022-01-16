from .lib      import CustomFastAPI
from .settings import ROOT_DIR, STATIC_DIRS


app = CustomFastAPI( str( ROOT_DIR ), STATIC_DIRS )