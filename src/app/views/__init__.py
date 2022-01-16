from .rabbit import *

from fastapi.responses import HTMLResponse
from src.app.settings  import STATIC_DIRS


@app.get( '/' )
def index( ) -> HTMLResponse:
    index_html = os_path.join( STATIC_DIRS['static'], 'index.html' )

    with open( index_html, 'r' ) as file:
        return HTMLResponse( content=file.read( ) )