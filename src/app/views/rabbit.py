import os.path as os_path

from typing              import List
from src.app             import app
from models.rabbit       import Rabbit, FilterOfMostMuitable
from models.collection   import Selection

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