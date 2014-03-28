#coding:utf-8
"""
Created on 25.02.2010

@author: prefer <telepenin@bars-open.ru>
"""
from m3.actions.context import ActionContext

from m3_ext.ui.base import ExtUIComponent


class BaseExtContainer(ExtUIComponent):
    """
    Базовый класс qдля контейнерных компонентов
    """
    AUTO = 'auto'
    FIT = 'fit'
    FORM = 'form'
    BORDER = 'border'
    VBOX = 'vbox'
    HBOX = 'hbox'
    ABSOLUTE = 'absolute'
    ACCORDITION = 'accordition'

    _js_attrs = ExtUIComponent._js_attrs + (
        'items', 'split',
        ('layout_config', 'layoutConfig'), 'layout',
        ('label_width', 'labelWidth'),
        ('collapse_mode', 'collapseMode'), 'collapsible', 'collapsed',
    )

    def __init__(self, *args, **kwargs):
        super(BaseExtContainer, self).__init__(*args, **kwargs)
        self._init_attr('items', [])

    def _make_read_only(
            self, access_off=True, exclude_list=(), *args, **kwargs):
        if self._items:
            for item in self._items:
                if hasattr(item, "make_read_only") and callable(
                        item.make_read_only):
                    item.make_read_only(
                        access_off, exclude_list, *args, **kwargs)


class BaseExtPanel(BaseExtContainer):
    """
    Базовый класс для визуальных контейнерных компонентов
    """
    _xtype = 'panel'

    _js_attrs = BaseExtContainer._js_attrs + (
        'title', 'border', 'split', 'header',
        ('icon_cls', 'iconCls'),
        ('dd_group', 'ddGroup'),
        ('top_bar', 'tbar'),
        ('bottom_bar', 'bbar'),
        ('footer_bar', 'fbar'),
        ('collapse_mode', 'collapseMode'),
        ('collapsed', 'collapsed'),
    )

    def __init__(self, *args, **kwargs):
        super(BaseExtPanel, self).__init__(*args, **kwargs)
        self.title = None
        self.header = False
        self.border = True

        self._init_attr('top_bar', []),
        self._init_attr('bottom_bar', []),
        self._init_attr('footer_bar', []),

    def _make_read_only(
            self, access_off=True, exclude_list=(), *args, **kwargs):
        #FIXME: нельзя использовать в качестве умолчательных параметров
        # изменяемые типы. Это может привести к неприятным side эффектам
        super(BaseExtPanel, self)._make_read_only(
            access_off, exclude_list, *args, **kwargs)

        bar_typle = (self.footer_bar, self.bottom_bar, self.top_bar)
        for bar in bar_typle:
            if bar and bar._items:
                # Обязательно проверяем, что пришел контейнер.
                assert isinstance(bar, BaseExtContainer)
                for item in bar._items:
                    if hasattr(item, "make_read_only") and callable(
                            item.make_read_only):

                        item.make_read_only(
                            access_off, exclude_list, *args, **kwargs)
