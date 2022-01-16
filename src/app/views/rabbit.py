import os.path as os_path

from typing              import List
from src.app             import app
from src.app.settings    import STATIC_DIRS
from models.rabbit       import Rabbit, FilterOfMostMuitable
from models.collection   import Selection
from fastapi.responses   import HTMLResponse

@app.directory( 'get' )
def generator( min: int=30, max: int=50 ) -> List[Rabbit]:
    """
        Create list of random rabbits.
    """

    return Rabbit.generate_list( min, max )

@app.directory( 'post' )
def select( rabbits: List[Rabbit], preferences: FilterOfMostMuitable ) -> Selection[Rabbit]:
    """
        The method of selecting the most attractive 
        rabbits for the user from the available list.
    """
    
    return preferences.filter( rabbits )


@app.get( '/' )
def index( ):
    index_html = os_path.join( STATIC_DIRS['static'], 'index.html' )

    with open( index_html, 'r' ) as file:
        return HTMLResponse( content=file.read( ) )