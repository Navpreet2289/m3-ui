# -*- coding: utf-8 -*-
"""
Created on 13.04.2011

@author: prefer
"""

from containers import *
from controls import *
from fields import *
from menus import *
from misc import *
from panels import *
from windows import *

try:
    from kladr.addrfield import ExtAddrComponent
except ImportError:
    """
    .. note::
        Компонент-заглушка, попытка инстанцирования которого
        возбуждает исключение, сообщающее о неустановленном КЛАДР
    """
    class ExtAddrComponent(object):
        def __new__(cls, *args, **kwargs):
            raise RuntimeError(u'kladr is not installed!')
