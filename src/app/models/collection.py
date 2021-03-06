from pydantic import BaseModel
from typing   import TypeVar, Generic, List, Optional, Dict


T = TypeVar('T')


class Selection( BaseModel, Generic[T] ):
    selected : List[T] = [ ]
    remaining: List[T] = [ ]


class SelectionParameters( BaseModel ):
    limit   : Optional[int] = 6
    order_by: Optional[str] = None


class PriorityFilter( BaseModel, Generic[T] ):
    selection_paremeters: SelectionParameters

    @property
    def priority_fields( self ) -> Dict[str, str]:
        """
            Fields specified in the class implementation 
            that are not equal to None will be used as priority when generating results
        """
        return {
            field_name: getattr( self, field_name )
            for field_name in self.__class__.__fields__.keys( )
            if field_name != 'selection_paremeters'
            if not getattr( self, field_name, None ) is None
        }
    
    def get_field_priority( self, elem: T ) -> int:
        """
            Method calculates priority by instance data fields. 
            Every value in data row simmular with filter field row append 1 point to total.
        """
        level = 0
        
        for prop, value in self.priority_fields.items( ):
            if value == getattr( elem, prop, None ):
                level += 1

        return level

    def filter( self, elements: List[T] ) -> Selection[ T ]:
        """
            The method compares each element props with the filter parameters, 
            and sorting data by most simmular elements. 
        """
        result   = Selection( )
        selected = sorted( elements, key=self.get_field_priority, reverse=True )

        result.selected = [
            elem
            for i, elem in enumerate( selected )
            if i < self.selection_paremeters.limit
        ]

        result.remaining = [ x for x in filter( lambda elem: not elem in result.selected, elements ) ]

        if self.selection_paremeters.order_by:
            result.selected .sort( key=lambda elem: getattr( elem, self.selection_paremeters.order_by ) )
            result.remaining.sort( key=lambda elem: getattr( elem, self.selection_paremeters.order_by ) )

        return result
