import re
import inspect

from os                  import path as os_path
from sys                 import path as sys_path
from typing              import Dict
from fastapi             import FastAPI
from fastapi.staticfiles import StaticFiles


ALLOW_HTTP_METHODS_FOR_DIRECTORY_DICORATE = [
    'get', 
    'put',
    'post',
    'delete' 
]

class CustomFastAPIError( Exception):
    ...


class CustomFastAPI( FastAPI ):
    __root_directory: str           = None
    __static_dirs:   Dict[str, str] = None

    def __init__( self, root_directory: str=None, static_dirs: str=None, *args, **kwargs ):
        super( ).__init__( *args, **kwargs )

        self.__root_directory = root_directory
        self.__static_dirs    = static_dirs

        if self.__static_dirs:
            self.__mount_static_directoryes( **self.__static_dirs )

        if self.__root_directory:
            sys_path.append( self.__root_directory )

    @property
    def root_directory( self ) -> str:
        return self.__root_directory

    @property 
    def static_dirs( self ) -> Dict[str, str]:
        return self.__static_dirs

    def __mount_static_directoryes( self, **directoryes: Dict[ str, str ] ) -> None:
        for name, folder in  directoryes.items( ):
            path = name if re.findall( name, r'^/' ) else '/' + name

            self.mount( path, StaticFiles( directory=os_path.abspath( folder ) ), name=name )
    
    def directory( self, method: str ):
        def wrap( func ):
            prefix = func.__module__.split( "." )

            prefix.append( func.__name__ )
            
            url = "/" + "/".join( prefix )

            request_handler = getattr( self, method.lower( ), False )
            
            setattr( func, '__url__'   , url    )
            setattr( func, '__method__', method )

            if method in ALLOW_HTTP_METHODS_FOR_DIRECTORY_DICORATE:
                return request_handler( url, response_model=func.__annotations__.get( 'return', None ))( func )
            else:
                raise CustomFastAPIError( f"Can't decorate function='{ func.__name__ }' with http mathod='{method}'")

        return wrap

