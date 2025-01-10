"""_summary_
    #Este archivo es parte de chain of responsability pattern ☣️
    
    Do:
        paso 1: Crea una clase que encapsule customer y payment data para validarlos. (commons:Request.py)
        paso 2:Definir una clase abstracta que tendrá cada validator en la cadena (chain_handler.py)
        ☄️ Por qué es una clase abstracta y no un protocolo: porque el código va a ser compartido dentro de
        todas las definiciones que implementen la clase abstracta
        paso 3: Crear la instancia concreta que implemente la validación de customer. (customer_handler.py)
    Returns:
        _type_: _description_
"""

from abc import ABC, abstractmethod
from typing import Self
from dataclasses import dataclass
from commons import Request

@dataclass
class ChainHandler(ABC):
    _next_handler: Self
    """es una cadena, así que cada eslabón puede defirnir cuál es el siguiente elemento que se debe invocar.
    y es así para todos los objetos, por eso es una clase abstracta.
    """
    def set_next(self,handler: Self): # handler va a ser del mismo tipo que ChainHandler
        self._next_handler = handler
        return handler
    
    @abstractmethod # metodo que debe ser utilizado en todos los objetos que se instancien a ChainHandler
    def handle(self, request: Request):
        ...