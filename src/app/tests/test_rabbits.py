#! /usr/local/bin/python
from typing import Dict, List
from urllib.parse       import urlencode 
from pathlib            import Path
from sys                import path as sys_path

ROOT_DIR = Path( __file__ ).parent.parent.parent

sys_path.append( str( ROOT_DIR        ) )
sys_path.append( str( ROOT_DIR.parent ) )

from src.app.lib.utils.test.request import response as response_test
from src.app.models.collection      import Selection
from src.app.models.rabbit          import Rabbit
from fastapi.testclient             import TestClient
from src.app                        import app, views


client = TestClient(app)

GENRATOR_LEN_MIN  = 10
GENERATOR_LEN_MAX = 11

RABBITS_LIST = [ 
    { 'name': 'Liam'     , 'wool': 'long-haired', 'color': 'brown', 'weight': 'normal' }, 
    { 'name': 'Olivia'   , 'wool': 'long-haired', 'color': 'white', 'weight': 'normal' }, 
    { 'name': 'Ava'      , 'wool': 'long-haired', 'color': 'green', 'weight': 'plump'  }, 
    { 'name': 'Olivia'   , 'wool': 'shorthaired', 'color': 'black', 'weight': 'plump'  }, 
    { 'name': 'Olivia'   , 'wool': 'long-haired', 'color': 'black', 'weight': 'normal' },
    { 'name': 'Liam'     , 'wool': 'shorthaired', 'color': 'white', 'weight': 'plump'  }, 
    { 'name': 'Charlotte', 'wool': 'shorthaired', 'color': 'white', 'weight': 'plump'  }, 
    { 'name': 'Noah'     , 'wool': 'long-haired', 'color': 'white', 'weight': 'plump'  },
    { 'name': 'Olivia'   , 'wool': 'long-haired', 'color': 'black', 'weight': 'normal' },
    { 'name': 'Olivia'   , 'wool': 'long-haired', 'color': 'black', 'weight': 'normal' },
    { 'name': 'Olivia'   , 'wool': 'long-haired', 'color': 'black', 'weight': 'normal' },
    { 'name': 'Olivia'   , 'wool': 'long-haired', 'color': 'black', 'weight': 'normal' },
    { 'name': 'Olivia'   , 'wool': 'long-haired', 'color': 'black', 'weight': 'normal' },
    { 'name': 'Bobo'     , 'wool': 'long-haired', 'color': 'black', 'weight': 'normal' },
    { 'name': 'Olivia'   , 'wool': 'long-haired', 'color': 'black', 'weight': 'normal' },
    { 'name': 'Olivia'   , 'wool': 'long-haired', 'color': 'black', 'weight': 'normal' },
    { 'name': 'Olivia'   , 'wool': 'long-haired', 'color': 'black', 'weight': 'normal' },
] 

RABBITS_SELECT_WAITED = [ 
    { 'name': 'Ava'      , 'wool': 'long-haired', 'color': 'green', 'weight': 'plump' }, 
    { 'name': 'Olivia'   , 'wool': 'long-haired', 'color': 'white', 'weight': 'normal' }, 
    { 'name': 'Olivia'   , 'wool': 'shorthaired', 'color': 'black', 'weight': 'plump'  }, 
    { 'name': 'Liam'     , 'wool': 'shorthaired', 'color': 'white', 'weight': 'plump'  }, 
    { 'name': 'Charlotte', 'wool': 'shorthaired', 'color': 'white', 'weight': 'plump'  }, 
    { 'name': 'Noah'     , 'wool': 'long-haired', 'color': 'white', 'weight': 'plump'  }
] 

PREFFERNCE = { #? we preffer rabbits with white color and plump weight
    "color": 'white',
    "weight": 'plump',
    "selection_paremeters": {
        "limit"   : len( RABBITS_SELECT_WAITED ), #? 6 
        "order_by": "color"
    },
}

RABBIT_REQUIRED_ATTRIBUTE = 'weight'

RABBITS_REMAININ_WAITED = [
    _rabbit for _rabbit in RABBITS_LIST
    if not _rabbit in RABBITS_SELECT_WAITED
]

@response_test.status_code_eq( 200 )
@response_test.json_array_len_beetwen( GENRATOR_LEN_MIN, GENERATOR_LEN_MAX )
def test_generator( ):
    params  = dict( min=GENRATOR_LEN_MIN, max=GENERATOR_LEN_MAX )
    baseurl = views.generator.__url__
    url     = baseurl  + '/?' + urlencode( params )
        
    return client.get( url )

def __test_selected( _selected: List[Rabbit] ):
    selected = [  
        { 
            prop: value 
            for prop, value in _rabbit.items( )
            if prop in RABBITS_SELECT_WAITED[0] #? cut id and other generic propertie
        }
        for _rabbit in _selected
    ]

    assert len( RABBITS_SELECT_WAITED ) == len( selected )

    for _rabbit in RABBITS_SELECT_WAITED:
        assert _rabbit in selected

def __test_remaining( _remaining: List[Rabbit] ):
    remaining = [  
        { 
            prop: value 
            for prop, value in _rabbit.items( )
            if prop in RABBITS_REMAININ_WAITED[0] #? cut id and other generic propertie
        }
        for _rabbit in _remaining
    ]
   
    assert len( remaining ) == len( RABBITS_REMAININ_WAITED )

    for _rabbit in RABBITS_REMAININ_WAITED:
        assert _rabbit in remaining

@response_test.json_check_props( 
    selected  = __test_selected ,
    remaining = __test_remaining
)
@response_test.status_code_eq( 200 )
def test_select( ):
    url = views.select.__url__
    json = {
        'rabbits': RABBITS_LIST,
        'preferences': PREFFERNCE
    }
        
    return client.post( url, json=json )

def __test_select_exception_validation_error_detail( _detail: List[ Dict[str, any] ] ):
    assert len( _detail ) == 1
    assert RABBIT_REQUIRED_ATTRIBUTE in _detail[0].get( 'loc', [ ] )

@response_test.json_check_props( 
    detail = __test_select_exception_validation_error_detail 
)
@response_test.status_code_eq( 422 )
def test_select_exception_validation_error( ):
    url   = views.select.__url__
    clone = { **RABBITS_LIST[0] } #? coppy correct rabbit

    clone.pop( RABBIT_REQUIRED_ATTRIBUTE ) #? remove required rabbit attribute

    json = {
        'rabbits': [ clone ],
        'preferences': PREFFERNCE
    }

    return client.post( url, json=json )
