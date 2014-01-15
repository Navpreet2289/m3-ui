#coding:utf-8
"""
Created on 3.3.2010

@author: prefer
"""
import json
from django.conf import settings
from django.utils.datastructures import SortedDict

from m3_ext.ui.base import ExtUIComponent, BaseExtComponent
from base import BaseExtPanel


#==============================================================================
class ExtPivotGrid(BaseExtPanel):
    """
    Сводная таблица
    """
    def __init__(self, *args, **kwargs):
        super(ExtPivotGrid, self).__init__(*args, **kwargs)
        self.template = 'ext-grids/ext-pivot-grid.js'
        self.__store = None
        self.aggregator = None
        self.renderer = None
        self.measure = None
        self._left_axis = []
        self._top_axis = []
        self._items = []
        self.__cm = None
        self.col_model = ExtGridDefaultColumnModel()
        self.force_fit = True
        self.auto_fill = True
        self.__view = None
        self._view_config = {}
        self.init_component(*args, **kwargs)

    def t_render_store(self):
        return self.__store.render(self.columns)

    def t_render_columns(self):
        return self.t_render_items()

    def add_column(self, **kwargs):
        self.columns.append(ExtGridColumn(**kwargs))

    def add_left_axis(self, **kwargs):
        self.left_axis.append(ExtPivotGridAxis(**kwargs))

    def add_top_axis(self, **kwargs):
        self.top_axis.append(ExtPivotGridAxis(**kwargs))

    def render_base_config(self):
        super(ExtPivotGrid, self).render_base_config()
        self._view_config['forceFit'] = self.force_fit
        self._view_config['autoFill'] = self.auto_fill
        for args in (
            ('store', self.t_render_store, self.get_store()),
            ('measure', self.measure),
            ('aggregator', self.aggregator),
            ('renderer', self.renderer),
            ('leftAxis', self.t_render_left_axis),
            ('topAxis', self.t_render_top_axis),
            ('colModel', self.col_model.render),
            ('view', self.t_render_view, self.view),
            ('viewConfig', self._view_config),
        ):
            self._put_config_value(*args)

    @property
    def columns(self):
        return self._items

    @property
    def left_axis(self):
        return self._left_axis

    @property
    def top_axis(self):
        return self._top_axis

    @property
    def view(self):
        return self.__view

    @view.setter
    def view(self, value):
        self.__view = value

    def render(self):
        self.render_base_config()
        self.render_params()
        config = self._get_config_str()
        params = self._get_params_str()
        return 'new Ext.grid.PivotGrid({%s}, {%s})' % (config, params)

    def set_store(self, store):
        self.__store = store

    def get_store(self):
        return self.__store

    store = property(get_store, set_store)

    @property
    def col_model(self):
        return self.__cm

    @col_model.setter
    def col_model(self, value):
        self.__cm = value
        self.__cm.grid = self

    def t_render_view(self):
        return self.view.render()

    def t_render_left_axis(self):
        return '[%s]' % ','.join(
            ['''{
            dataIndex:"%s",
            header:"%s",
            width:%d,
            defaultHeaderWidth:%d,
            orientation:"%s"
            }''' % (
            axe.data_index,
            axe.header,
            axe.width,
            axe.default_header_width,
            axe.orientation) for axe in self.left_axis])

    def t_render_top_axis(self):
        return '[%s]' % ','.join(
            ['''{
            dataIndex:"%s",
            header:"%s",
            width:%d,
            defaultHeaderWidth:%d,
            orientation:"%s"
            }''' % (
            axe.data_index,
            axe.header,
            axe.width,
            axe.default_header_width,
            axe.orientation) for axe in self.top_axis])


#==============================================================================
class ExtGrid(BaseExtPanel):
    """
    Таблица (Grid)
    Внимание! Грид реализует двуличное поведение
    в зависимости от атрибута editor.
    Порождающая его функция createGridPanel может вернуть экземпляр
    Ext.m3.GridPanel (False) или Ext.m3.EditorGridPanel (True),
    поэтому некоторые атрибуты могут действовать в одном,
    но не действовать в другом гриде.
    """

    # TODO: Реализовать человеческий MVC грид

    def __init__(self, *args, **kwargs):
        super(ExtGrid, self).__init__(*args, **kwargs)
        self._items = []
        self.__store = None

        # Будет ли редактироваться
        self.editor = False

        # Объект маскирования, который будет отображаться при загрузке
        self.load_mask = False

        # Сколько раз нужно щелкнуть для редактирования ячейки.
        # Только для EditorGridPanel
        self.clicks_to_edit = 2

        self.drag_drop = False
        self.drag_drop_group = None

        # Разворачивать колонки грида по всей ширине (True)
        self.force_fit = True

        # selection model
        self.__sm = None

        self.__view = None

        # Колонка для авторасширения
        self.auto_expand_column = None

        # устанавливается True, если sm=CheckBoxSelectionModel. Этот флаг нужен
        # чтобы знать когда нужен дополнительный column
        self.__checkbox = False

        # перечень плагинов
        self.plugins = []

        # модель колонок
        self.__cm = None

        self.col_model = ExtGridDefaultColumnModel()

        # Конфигурация для уровня view
        self._view_config = {}
        self.show_preview = False
        self.enable_row_body = False
        self.get_row_class = None

        # признак отображения вертикальных линий в гриде
        self.column_lines = True

        #Если True не рендерим drag and drop, выключаем editor
        self.read_only = False

        # Метка. Использовать только если задан layout=form
        self.label = None

        self.init_component(*args, **kwargs)

        # protected
        self.show_banded_columns = False
        self.banded_columns = SortedDict()

    def t_render_plugins(self):
        """
        Рендеринг плагинов
        """
        res = []
        for plugin in self.plugins:
            res.append(plugin.render() if hasattr(plugin, 'render') else plugin)

        return '[%s]' % ','.join(res)

    def t_render_banded_columns(self):
        """
        Возвращает JS массив состоящий из массивов с описанием объединенных
        колонок. Каждый вложенный массив соответствует уровню шапки грида от
        верхней к нижней.
        """
        result = []
        for level_list in self.banded_columns.values():
            result.append('[%s]' % ','.join(
                [column.render() for column in level_list]))
        return '[%s]' % ','.join(result)

    def t_render_columns(self):
        return self.t_render_items()

    def t_render_store(self):
        assert self.__store, 'Store is not define'
        return self.__store.render(self.columns)

    def t_render_col_model(self):
        return self.__cm.render()

    def add_column(self, **kwargs):
        """
        Добавляет стандартную колонку
        """
        self.columns.append(ExtGridColumn(**kwargs))

    def add_bool_column(self, **kwargs):
        """
        Добавляет булевую колонку
        """
        self.columns.append(ExtGridBooleanColumn(**kwargs))

    def add_check_column(self, **kwargs):
        """
        Добавляет колонку для выбора значения
        """
        self.columns.append(ExtGridCheckColumn(**kwargs))

    def add_number_column(self, **kwargs):
        """
        Добавляет числовую колонку
        """
        self.columns.append(ExtGridNumberColumn(**kwargs))

    def add_date_column(self, **kwargs):
        """
        Добавляет колонку с датой
        """
        self.columns.append(ExtGridDateColumn(**kwargs))

    def add_banded_column(self, column, level, colspan):
        """
        Добавляет в грид объединенную ячейку.
        @param column: Колонка грида (ExtGridColumn)
        @param colspan: Количество колонок которые находятся
            под данной колонкой (int)
        @param level: Уровень учейки где
          0 - самый верхний,
          1-ниже, и т.д. (int)

        upd:26.10.2010 kirov
        колонка может быть не указана, т.е. None,
        в этом случае на указанном уровне будет "дырка"
        """
        class BlankBandColumn():
            colspan = 0

            def render(self):
                return '{%s}' % (
                    ('colspan:%s' % self.colspan) if self.colspan else '')

        assert isinstance(level, int)
        assert isinstance(colspan, int)
        assert isinstance(column, ExtGridColumn) or not column
        if not column:
            column = BlankBandColumn()
        # Колонки хранятся в списках внутки сортированного словаря,
        #чтобы их можно было
        # извечь по возрастанию уровней
        column.colspan = colspan
        level_list = self.banded_columns.get(level, [])
        level_list.append(column)
        self.banded_columns[level] = level_list
        self.show_banded_columns = True

    def clear_banded_columns(self):
        """
        Удаляет все объединенные колонки из грида
        """
        self.banded_columns.clear()
        self.show_banded_columns = False

    def set_store(self, store):
        self.__store = store

    def get_store(self):
        return self.__store

    store = property(get_store, set_store)

    def _make_read_only(
            self, access_off=True, exclude_list=[], *args, **kwargs):
        super(ExtGrid, self)._make_read_only(
            access_off, exclude_list, *args, **kwargs)
        self.read_only = access_off
        if self.columns:
            for column in self.columns:
                column._make_read_only(
                    self.read_only, exclude_list, *args, **kwargs)

        # убираем редактирование записи по даблклику
        self.handler_dblclick = 'Ext.emptyFn'

        # контекстное меню.
        context_menu_items = [self.handler_contextmenu,
                              self.handler_rowcontextmenu]
        for context_menu in context_menu_items:
            if (
                context_menu and
                hasattr(context_menu, 'items') and
                context_menu.items and
                hasattr(context_menu.items, '__iter__')
            ):
                for item in context_menu.items:
                    if isinstance(item, ExtUIComponent):
                        item._make_read_only(
                            self.read_only, exclude_list, *args, **kwargs)

    @property
    def columns(self):
        return self._items

    @property
    def sm(self):
        return self.__sm

    @sm.setter
    def sm(self, value):
        self.__sm = value
        self.checkbox_model = isinstance(self.__sm, ExtGridCheckBoxSelModel)

    @property
    def view(self):
        return self.__view

    @view.setter
    def view(self, value):
        self.__view = value

    def t_render_view(self):
        return self.view.render()

    def pre_render(self):
        super(ExtGrid, self).pre_render()
        if self.store:
            self.store.action_context = self.action_context

    @property
    def col_model(self):
        return self.__cm

    @col_model.setter
    def col_model(self, value):
        self.__cm = value
        self.__cm.grid = self

    #//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\
    # Врапперы над событиями listeners[...]
    #------------------------------------------------------------------------
    @property
    def handler_click(self):
        return self._listeners.get('click')

    @handler_click.setter
    def handler_click(self, function):
        self._listeners['click'] = function

    @property
    def handler_dblclick(self):
        return self._listeners.get('dblclick')

    @handler_dblclick.setter
    def handler_dblclick(self, function):
        self._listeners['dblclick'] = function

    @property
    def handler_contextmenu(self):
        return self._listeners.get('contextmenu')

    @handler_contextmenu.setter
    def handler_contextmenu(self, menu):
        menu.container = self
        self._listeners['contextmenu'] = menu

    @property
    def handler_rowcontextmenu(self):
        return self._listeners.get('rowcontextmenu')

    @handler_rowcontextmenu.setter
    def handler_rowcontextmenu(self, menu):
        menu.container = self
        self._listeners['rowcontextmenu'] = menu

    def render_base_config(self):
        super(ExtGrid, self).render_base_config()
        if self.force_fit:
            self._view_config['forceFit'] = self.force_fit
        if self.show_preview:
            self._view_config['showPreview'] = self.show_preview
        if self.enable_row_body:
            self._view_config['enableRowBody'] = self.enable_row_body
        if self.get_row_class:
            self._view_config['getRowClass'] = self.get_row_class

        for args in (
            ('stripeRows', True),
            ('stateful', True),
            ('loadMask', self.load_mask),
            ('autoExpandColumn', self.auto_expand_column),
            ('editor', self.editor),
            ('view', self.t_render_view, self.view),
            ('store', self.t_render_store, self.get_store()),
            ('viewConfig', self._view_config),
            ('columnLines', self.column_lines, self.column_lines),
            ('enableDragDrop', self.drag_drop) if self.read_only else (),
            ('ddGroup', self.drag_drop_group) if self.read_only else (),
            ('fieldLabel', self.label) if self.label else (),
            (
                'clicksToEdit',
                self.clicks_to_edit, self.clicks_to_edit != 2
            ) if self.editor else (),
        ):
            if args:
                self._put_config_value(*args)

    def render_params(self):
        super(ExtGrid, self).render_params()

        handler_cont_menu = (
            self.handler_contextmenu.render
            if self.handler_contextmenu else ''
        )
        handler_rowcontextmenu = (
            self.handler_rowcontextmenu.render
            if self.handler_rowcontextmenu else ''
        )

        self._put_params_value(
            'menus',
            {
                'contextMenu': handler_cont_menu,
                'rowContextMenu': handler_rowcontextmenu
            }
        )
        if self.sm:
            self._put_params_value('selModel', self.sm.render)

        self._put_params_value('colModel', self.col_model.render)
        # проверим набор колонок на наличие фильтров,
        # если есть, то добавим плагин с фильтрами
        for col in self.columns:
            if col.filter:
                self.plugins.append(
                    u"new Ext.ux.grid.GridFilters({menuFilterText:'Фильтр'})")
                break
        self._put_params_value('plugins', self.t_render_plugins)

        if self.show_banded_columns:
            self._put_params_value(
                'bundedColumns', self.t_render_banded_columns)

    def render(self):
        try:
            self.pre_render()

            self.render_base_config()
            self.render_params()
        except UnicodeDecodeError as msg:
            raise Exception(msg)

        config = self._get_config_str()
        params = self._get_params_str()
        return 'createGridPanel({%s}, {%s})' % (config, params)


#==============================================================================
# Оси к пивот гриду
#==============================================================================
class ExtPivotGridAxis(ExtUIComponent):
    DEFAULT_HEADER_WIDTH = 100

    def __init__(self, *args, **kwargs):
        super(ExtPivotGridAxis, self).__init__(*args, **kwargs)
        self.width = ExtPivotGridAxis.DEFAULT_HEADER_WIDTH
        self.data_index = None
        self.orientation = 'horizontal'
        self.header = None
        self.default_header_width = 80
        self.init_component(*args, **kwargs)


#==============================================================================
class BaseExtGridColumn(ExtUIComponent):

    # Умолчательная ширина колонок
    GRID_COLUMN_DEFAULT_WIDTH = 100

    # Рендерер для цен и сумм
    THOUSAND_CURRENCY_RENDERER = 'thousandCurrencyRenderer'

    def __init__(self, *args, **kwargs):
        super(BaseExtGridColumn, self).__init__(*args, **kwargs)

        # Заголовок
        self.header = None

        # Возможность сортировки
        self.sortable = False

        # Уникальное название колонки в пределах column model
        self.data_index = None

        # Расположение
        self.align = None

        # Ширина
        self.width = BaseExtGridColumn.GRID_COLUMN_DEFAULT_WIDTH

        # Редактор, если колонка может быть редактируемой
        self.editor = None

        # Список рендереров колонки
        self._column_renderer = []

        # Всплывающая подсказка
        self.tooltip = None

        # Признак того, скрыта ли колонка или нет
        self.hidden = False

        # Признак не активности
        self.read_only = False

        # TODO: В версии 3.3 нет такого свойства
        self.colspan = None

        # Запрет на изменение ширины колонки
        self.fixed = False

        # Признак зафиксированности колонки
        # используется вместе с ExtGridLockingView + ExtGridLockingColumnModel
        self.locked = False

        # дополнительные атрибуты колонки
        self.extra = {}

        # Настройки фильтра колонки для плагина Ext.ux.grid.GridFilters
        self.filter = None

        self.menu_disabled = False

    def t_render_extra(self):
        lst = []
        for key in self.extra.keys():
            val = self.extra[key]

            if isinstance(val, BaseExtComponent):
                lst.append('%s:%s' % (key, val.render()))
            elif isinstance(val, bool):
                lst.append('%s:%s' % (key, str(val).lower()))
            elif isinstance(val, (int, str, unicode)):
                lst.append('%s:%s' % (key, val))
            else:  # пусть как хочет так и рендерится
                lst.append('%s:%s' % (key, val))
        return ','.join(lst)

    def render_editor(self):
        return self.editor.render()

    def _make_read_only(
            self, access_off=True, exclude_list=[], *args, **kwargs):
        self.read_only = access_off
        if self.editor and isinstance(self.editor, ExtUIComponent):
            self.editor._make_read_only(
                self.read_only, exclude_list, *args, **kwargs)

    def render_base_config(self):
        super(BaseExtGridColumn, self).render_base_config()
        for args in (
            ('header', self.header),
            ('sortable', self.sortable),
            ('dataIndex', self.data_index),
            ('align', self.align),
            ('editor', self.editor.render if self.editor else None),
            ('hidden', self.hidden),
            ('readOnly', self.read_only),
            ('colspan', self.colspan),
            ('fixed', self.fixed),
            ('locked', self.locked),
            ('renderer', self.render_column_renderer),
            ('tooltip', self.tooltip),
            ('filter', self.filter),
            ('menuDisabled', self.menu_disabled),
        ):
            self._put_config_value(*args)

        for i, render in enumerate(self._column_renderer):
            if BaseExtGridColumn.THOUSAND_CURRENCY_RENDERER == render:
                # Финансовый формат для Сумм и Цен
                # подразумевает прижимание к правому краю.
                thousand_column_renderer = (
                    '(function(val, metaData){ '
                    'metaData.attr="style=text-align:right"; '
                    'return %s.apply(this, arguments);}) '
                ) % BaseExtGridColumn.THOUSAND_CURRENCY_RENDERER
                self._column_renderer[i] = thousand_column_renderer

    @property
    def column_renderer(self):
        return ','.join(self._column_renderer)

    @column_renderer.setter
    def column_renderer(self, value):
        self._column_renderer.append(value)

    def render_column_renderer(self):
        """
        Кастомный рендеринг функций-рендерера колонок
        """
        if self._column_renderer:
            self._column_renderer.reverse()
            val = self._get_renderer_func(self._column_renderer)
            return (
                'function(val, metaData, record, rowIndex, '
                'colIndex, store){return %s}'
            ) % val
        return None

    def _get_renderer_func(self, list_renderers):
        """
        Рекурсивная функция, оборачивающая друг в друга рендереры колонок
        """
        if list_renderers:
            return '%s(%s, metaData, record, rowIndex, colIndex, store)' % (
                list_renderers[0],
                self._get_renderer_func(list_renderers[1:])
            )
        else:
            return 'val'


class ExtGridColumn(BaseExtGridColumn):
    def __init__(self, *args, **kwargs):
        super(ExtGridColumn, self).__init__(*args, **kwargs)
        self.init_component(*args, **kwargs)

    def render(self):
        try:
            self.render_base_config()
        except UnicodeDecodeError as msg:
            raise Exception(msg)

        config = self._get_config_str()
        extra = self.t_render_extra()
        return '{%s}' % (config + ',' + extra if extra else config)


class ExtGridBooleanColumn(BaseExtGridColumn):
    def __init__(self, *args, **kwargs):
        super(ExtGridBooleanColumn, self).__init__(*args, **kwargs)
        self.template = 'ext-grids/ext-bool-column.js'
        self.text_false = None
        self.text_true = None
        self.text_undefined = None
        self.init_component(*args, **kwargs)


class ExtGridCheckColumn(BaseExtGridColumn):
    def __init__(self, *args, **kwargs):
        super(ExtGridCheckColumn, self).__init__(*args, **kwargs)
        self.template = 'ext-grids/ext-check-column.js'
        self.init_component(*args, **kwargs)


class ExtGridNumberColumn(BaseExtGridColumn):
    def __init__(self, *args, **kwargs):
        super(ExtGridNumberColumn, self).__init__(*args, **kwargs)
        self.template = 'ext-grids/ext-number-column.js'
        self.format = None
        self.init_component(*args, **kwargs)


class ExtGridDateColumn(BaseExtGridColumn):
    def __init__(self, *args, **kwargs):
        super(ExtGridDateColumn, self).__init__(*args, **kwargs)
        self.template = 'ext-grids/ext-date-column.js'
        try:
            self.format = settings.DATE_FORMAT.replace('%', '')
        except AttributeError:
            self.format = 'd.m.Y'

        self.init_component(*args, **kwargs)


class BaseExtGridSelModel(BaseExtComponent):
    def __init__(self, *args, **kwargs):
        super(BaseExtGridSelModel, self).__init__(*args, **kwargs)


class ExtGridCheckBoxSelModel(BaseExtGridSelModel):
    """
    Модель для грида с возможностью выбора ячейки
    """
    def __init__(self, *args, **kwargs):
        super(ExtGridCheckBoxSelModel, self).__init__(*args, **kwargs)
        self.single_select = False
        self.check_only = False
        self.init_component(*args, **kwargs)

    def render(self):
        self._put_config_value('singleSelect', self.single_select)
        self._put_config_value('checkOnly', self.check_only)
        return 'new Ext.grid.CheckboxSelectionModel({ %s })' % (
            self._get_config_str())


class ExtGridRowSelModel(BaseExtGridSelModel):
    """
    Модель для грида с выбором строк
    """
    def __init__(self, *args, **kwargs):
        super(ExtGridRowSelModel, self).__init__(*args, **kwargs)
        self.single_select = False
        self.init_component(*args, **kwargs)

    def render(self):
        single_sel = 'singleSelect: true' if self.single_select else ''
        return 'new Ext.grid.RowSelectionModel({ %s })' % single_sel


class ExtGridCellSelModel(BaseExtGridSelModel):
    """
    Модель для грида с выбором ячеек
    """
    def __init__(self, *args, **kwargs):
        super(ExtGridCellSelModel, self).__init__(*args, **kwargs)
        self.init_component(*args, **kwargs)

    def render(self):
        return 'new Ext.grid.CellSelectionModel()'


class ExtGridDefaultColumnModel(BaseExtComponent):
    """
    Модель колонок для грида по-умолчанию
    """
    # TODO: Этот класс, т.к. ссылка на грид порождает цикличную связь
    def __init__(self, *args, **kwargs):
        super(ExtGridDefaultColumnModel, self).__init__(*args, **kwargs)
        self.grid = None
        self.init_component(*args, **kwargs)

    def render(self):
        return 'new Ext.grid.ColumnModel({columns:%s})' % (
            self.grid.t_render_columns())


class ExtGridLockingColumnModel(BaseExtComponent):
    """
    Модель колонок для грида блокрирования
    """
    # TODO: Этот класс, т.к. ссылка на грид порождает цикличную связь
    def __init__(self, *args, **kwargs):
        super(ExtGridLockingColumnModel, self).__init__(*args, **kwargs)
        self.grid = None
        self.init_component(*args, **kwargs)

    def render(self):
        return 'new Ext.ux.grid.LockingColumnModel({columns:%s})' % (
            self.grid.t_render_columns())


class ExtGridLockingHeaderGroupColumnModel(BaseExtComponent):
    # TODO: Этот класс, т.к. ссылка на грид порождает цикличную связь
    def __init__(self, *args, **kwargs):
        super(ExtGridLockingHeaderGroupColumnModel, self).__init__(
            *args, **kwargs)
        self.grid = None
        self.init_component(*args, **kwargs)

    def render(self):
        return 'new Ext.ux.grid.LockingGroupColumnModel({columns:%s})' % (
            self.grid.t_render_columns())


class ExtAdvancedTreeGrid(ExtGrid):
    """
    Расширенное дерево на базе Ext.ux.maximgb.TreeGrid
    """
    def __init__(self, *args, **kwargs):
        super(ExtAdvancedTreeGrid, self).__init__(*args, **kwargs)
        self.template = 'ext-grids/ext-advanced-treegrid.js'
        self.url = None
        self.master_column_id = None

        # Свойства для внутреннего store:
        self.store_root = 'rows'

        # Свойства для внутеннего bottom bara:
        self.use_bbar = False

        # Количество записей
        self.bbar_page_size = 10

        self.init_component(*args, **kwargs)

    def t_render_columns_to_record(self):
        return '[%s]' % ','.join([
            '{name:"%s"}' % col.data_index
            for col in self.columns
        ])

    def add_column(self, **kwargs):
        # FIXME: Хак, с сгенерированным client_id
        # компонент отказывается работать
        if kwargs.get('data_index'):
            kwargs['client_id'] = kwargs.get('data_index')
        super(ExtAdvancedTreeGrid, self).add_column(**kwargs)

    def render_base_config(self):
        super(ExtAdvancedTreeGrid, self).render_base_config()
        self._put_config_value('master_column_id', self.master_column_id)

    def render_params(self):
        super(ExtAdvancedTreeGrid, self).render_params()
        self._put_params_value(
            'storeParams',
            {
                'url': self.url,
                'root': self.store_root
            }
        )
        self._put_params_value(
            'columnsToRecord', self.t_render_columns_to_record)

        if self.use_bbar:
            self._put_params_value('bbar', {'pageSize': self.bbar_page_size})

    def t_render_base_config(self):
        return self._get_config_str()

    def render(self):
        self.render_base_config()
        self.render_params()

        base_config = self._get_config_str()
        params = self._get_params_str()
        return 'createAdvancedTreeGrid({%s},{%s})' % (
            base_config, params)


class ExtGridGroupingView(BaseExtComponent):
    """
    Компонент используемый для группировки
    """
    def __init__(self, *args, **kwargs):
        super(ExtGridGroupingView, self).__init__(*args, **kwargs)
        self.force_fit = True
        self.show_preview = False
        self.enable_row_body = False
        self.get_row_class = None
        self.group_text_template = '{text} ({[values.rs.length]})'
        self.init_component(*args, **kwargs)

    def render_params(self):
        super(ExtGridGroupingView, self).render_params()
        if self.force_fit:
            self._put_params_value('forceFit', self.force_fit)
        if self.show_preview:
            self._put_params_value('showPreview', self.show_preview)
        if self.enable_row_body:
            self._put_params_value('enableRowBody', self.enable_row_body)
        if self.get_row_class:
            self._put_params_value('getRowClass', self.get_row_class)
        self._put_params_value('groupTextTpl', self.group_text_template)

    def render(self):
        try:
            self.pre_render()
            self.render_base_config()
            self.render_params()
        except UnicodeDecodeError as msg:
            raise Exception(msg)
        params = self._get_params_str()
        return 'new Ext.grid.GroupingView({%s})' % params


class ExtGridLockingView(BaseExtComponent):
    """
    Компонент используемый для блокирования колонок
    """
    def __init__(self, *args, **kwargs):
        super(ExtGridLockingView, self).__init__(*args, **kwargs)
        self.init_component(*args, **kwargs)

    def render(self):
        result = 'new Ext.ux.grid.LockingGridView()'
        return result


class ExtGridLockingHeaderGroupView(BaseExtComponent):
    """
    Компонент используемый для блокирования колонок и их группировки
    """
    def __init__(self, *args, **kwargs):
        super(ExtGridLockingHeaderGroupView, self).__init__(*args, **kwargs)
        self.grid = None
        self.init_component(*args, **kwargs)

    def render(self):
        result = 'new Ext.ux.grid.LockingHeaderGroupGridView({rows:%s})' % (
            self.grid.t_render_banded_columns())
        return result


class ExtLiveGridCheckBoxSelModel(ExtGridCheckBoxSelModel):
    """
    Модель выбора для live-грида с возможностью отметки чек-боксом
    """
    def __init__(self, *args, **kwargs):
        super(ExtLiveGridCheckBoxSelModel, self).__init__(*args, **kwargs)
        self.single_select = False
        self.check_only = False
        self.init_component(*args, **kwargs)

    def render(self):
        self._put_config_value('singleSelect', self.single_select)
        self._put_config_value('checkOnly', self.check_only)
        return 'new Ext.ux.grid.livegrid.CheckboxSelectionModel({ %s })' % (
            self._get_config_str())


class ExtLiveGridRowSelModel(ExtGridRowSelModel):
    """
    Модель выбора для live-грида с выбором строк
    """
    def __init__(self, *args, **kwargs):
        super(ExtLiveGridRowSelModel, self).__init__(*args, **kwargs)
        self.single_select = False
        self.init_component(*args, **kwargs)

    def render(self):
        single_sel = 'singleSelect: true' if self.single_select else ''
        return 'new Ext.ux.grid.livegrid.RowSelectionModel({ %s })' % (
            single_sel)


class ExtGridLockingHeaderGroupPlugin(BaseExtComponent):
    """
    Плагин для группировки и одновременного закрепления колонок

    columnModelConfig: {

        /**
         * lockedCount начальное количество блокированных столбцов
         */
        lockedCount: 0,

        /**
         * rows строки с объединениями для построения многоуровневой шапки
         */
        rows: [],

        hierarchicalColMenu: true
    },

    viewConfig: {

        //LockingView config****************************************************************

        lockText: 'Lock',
        unlockText: 'Unlock',
        rowBorderWidth: 1,
        lockedBorderWidth: 1,
        /*
         * This option ensures that height between the rows is synchronized
         * between the locked and unlocked sides. This option only needs to be used
         * when the row heights aren't predictable.
         */
        syncHeights: false,

        //GroupingView config*****************************************************************

        /**
         * @cfg {String} groupByText Text displayed in the grid header menu for grouping by a column
         * (defaults to 'Group By This Field').
         */
        groupByText: 'Group By This Field',
        /**
         * @cfg {String} showGroupsText Text displayed in the grid header for enabling/disabling grouping
         * (defaults to 'Show in Groups').
         */
        showGroupsText: 'Show in Groups',
        /**
         * @cfg {Boolean} hideGroupedColumn <tt>true</tt> to hide the column that is currently grouped (defaults to <tt>false</tt>)
         */
        hideGroupedColumn: false,
        /**
         * @cfg {Boolean} showGroupName If <tt>true</tt> will display a prefix plus a ': ' before the group field value
         * in the group header line.  The prefix will consist of the <tt><b>{@link Ext.grid.Column#groupName groupName}</b></tt>
         * (or the configured <tt><b>{@link Ext.grid.Column#header header}</b></tt> if not provided) configured in the
         * {@link Ext.grid.Column} for each set of grouped rows (defaults to <tt>true</tt>).
         */
        showGroupName: true,
        /**
         * @cfg {Boolean} startCollapsed <tt>true</tt> to start all groups collapsed (defaults to <tt>false</tt>)
         */
        startCollapsed: false,
        /**
         * @cfg {Boolean} enableGrouping <tt>false</tt> to disable grouping functionality (defaults to <tt>true</tt>)
         */
        enableGrouping: true,
        /**
         * @cfg {Boolean} enableGroupingMenu <tt>true</tt> to enable the grouping control in the column menu (defaults to <tt>true</tt>)
         */
        enableGroupingMenu: true,
        /**
         * @cfg {Boolean} enableNoGroups <tt>true</tt> to allow the user to turn off grouping (defaults to <tt>true</tt>)
         */
        enableNoGroups: true,
        /**
         * @cfg {String} emptyGroupText The text to display when there is an empty group value (defaults to <tt>'(None)'</tt>).
         * May also be specified per column, see {@link Ext.grid.Column}.{@link Ext.grid.Column#emptyGroupText emptyGroupText}.
         */
        emptyGroupText: '(None)',
        /**
         * @cfg {Boolean} ignoreAdd <tt>true</tt> to skip refreshing the view when new rows are added (defaults to <tt>false</tt>)
         */
        ignoreAdd: false,
        /**
         * @cfg {String} groupTextTpl The template used to render the group header (defaults to <tt>'{text}'</tt>).
         * This is used to format an object which contains the following properties:
         * <div class="mdetail-params"><ul>
         * <li><b>group</b> : String<p class="sub-desc">The <i>rendered</i> value of the group field.
         * By default this is the unchanged value of the group field. If a <tt><b>{@link Ext.grid.Column#groupRenderer groupRenderer}</b></tt>
         * is specified, it is the result of a call to that function.</p></li>
         * <li><b>gvalue</b> : Object<p class="sub-desc">The <i>raw</i> value of the group field.</p></li>
         * <li><b>text</b> : String<p class="sub-desc">The configured header (as described in <tt>{@link #showGroupName})</tt>
         * if <tt>{@link #showGroupName}</tt> is <tt>true</tt>) plus the <i>rendered</i> group field value.</p></li>
         * <li><b>groupId</b> : String<p class="sub-desc">A unique, generated ID which is applied to the
         * View Element which contains the group.</p></li>
         * <li><b>startRow</b> : Number<p class="sub-desc">The row index of the Record which caused group change.</p></li>
         * <li><b>rs</b> : Array<p class="sub-desc">Contains a single element: The Record providing the data
         * for the row which caused group change.</p></li>
         * <li><b>cls</b> : String<p class="sub-desc">The generated class name string to apply to the group header Element.</p></li>
         * <li><b>style</b> : String<p class="sub-desc">The inline style rules to apply to the group header Element.</p></li>
         * </ul></div></p>
         * See {@link Ext.XTemplate} for information on how to format data using a template. Possible usage:<pre><code>
         var grid = new Ext.grid.GridPanel({
         ...
         view: new Ext.grid.GroupingView({
         groupTextTpl: '{text} ({[values.rs.length]} {[values.rs.length > 1 ? "Items" : "Item"]})'
         }),
         });
         * </code></pre>
         */
        groupTextTpl: '{text}',

        /**
         * @cfg {String} groupMode Indicates how to construct the group identifier. <tt>'value'</tt> constructs the id using
         * raw value, <tt>'display'</tt> constructs the id using the rendered value. Defaults to <tt>'value'</tt>.
         */
        groupMode: 'value',

        /**
         * @cfg {Function} groupRenderer This property must be configured in the {@link Ext.grid.Column} for
         * each column.
         */

        /**
         * @cfg {Boolean} cancelEditOnToggle True to cancel any editing when the group header is toggled. Defaults to <tt>true</tt>.
         */
        cancelEditOnToggle: true,

        /**
         * @cfg {Boolean} totalSummaryRowEnabled True to render total summary row. Defaults to <tt>true</tt>.
         */
        totalSummaryEnabled: true
    }
    """

    def __init__(self, config):
        """
        :param dict config: Конфигурация плагина, описание выше
        """
        super(BaseExtComponent, self).__init__()
        self._ext_name = 'Ext.ux.grid.LockingGridColumnWithHeaderGroup'
        self.config = config

    def render(self):
        return 'new %s(%s)' % (self._ext_name, json.dumps(self.config))