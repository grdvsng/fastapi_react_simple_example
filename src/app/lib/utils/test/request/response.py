from typing   import Callable, Any, Type, TypeVar
from requests import Response


T = TypeVar('T')

def json_array_len_beetwen( min: int=None, max: int=None ):
    def wrap( func:Callable[ [Any, Any], Response] ):
        def __wrap( *args, **kwargs ) -> Response:
            response = func( *args, **kwargs ) 
            data     = response.json()

            if min: assert len( data ) >= min

            if max: assert len( data ) <= max

            return response

        return __wrap

    return wrap

def status_code_eq( status_code: int ) :
    def wrap( func:Callable[ [Any, Any], Response] ):
        def __wrap( *args, **kwargs ):
            response = func( *args, **kwargs ) 
            
            assert response.status_code == status_code

            return response

        return __wrap
        
    return wrap

def json_check_props( **validators: Callable[[T],None] ) :
    def wrap( func:Callable[ [Any, Any], Response] ):
        def __wrap( *args, **kwargs ):
            response = func( *args, **kwargs ) 
            json     = response.json( )
            
            for prop, validator in validators.items( ):
                validator( json.get( prop, None ) )

            return response

        return __wrap
        
    return wrap
