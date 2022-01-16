import uuid

from random            import randint, choice as random_choice
from typing            import Optional, Literal, List
from pydantic          import BaseModel
from typing_extensions import Self
from .collection       import PriorityFilter


RABBITS_WEIGHT = Literal[ 'thin', 'normal', 'plump'          ]
RABBITS_COLOR  = Literal[ 'white', 'black', 'brown', 'green' ]
RABBITS_WOOL   = Literal[ 'shorthaired', 'long-haired'       ]

RABBIT_NAMES = [
    'Olivia',
    'Emma',
    'Ava',
    'Charlotte',
    'Liam',
    'Noah',
    'Oliver',
    'Elijah'
]


class Rabbit( BaseModel ):
    id     : Optional[uuid.UUID] = None
    name   : Optional[str]       = None

    wool   : RABBITS_WOOL
    color  : RABBITS_COLOR
    weight : RABBITS_WEIGHT

    def __init__( self, *args, **kwargs ):
        super( ).__init__( *args, **kwargs )

        self.id = uuid.uuid4( )
    
    @classmethod
    def generate( cls ) -> Self:
        return cls( 
            name   = random_choice( RABBIT_NAMES ),
            wool   = random_choice( RABBITS_WOOL  .__args__ ),
            color  = random_choice( RABBITS_COLOR .__args__ ),
            weight = random_choice( RABBITS_WEIGHT.__args__ ),
        )

    @classmethod
    def generate_list( cls, min: int=30, max: int=100 ) -> List[Self]:
        total = randint( min, max )
        
        return [
            cls.generate( )
            for i in range( 0, total )
        ]
    
    
class FilterOfMostMuitable( PriorityFilter[Rabbit] ):
    wool    : Optional[RABBITS_WOOL  ] = None  
    color   : Optional[RABBITS_COLOR ] = 'white'        
    weight  : Optional[RABBITS_WEIGHT] = 'plump' 