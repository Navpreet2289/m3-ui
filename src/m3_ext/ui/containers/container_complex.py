#coding:utf-8
"""
Created on 21.04.2010

@author: prefer <telepenin@bars-open.ru>
"""

from m3_ext.ui.base import ExtUIComponent
from containers import ExtContainer


class ExtContainerTable(object):
    """
    Контейнерный компонент.
    Имеет в себе табличную настройку (строки и колонки)
    и позволяет в ячейках указывать произвольные контролы,
    которые будут помещены в ExtContainer с layout=form
    """
    _DEFAULT_HEIGHT = 36

    def __init__(self, columns=0, rows=0, **kwargs):
        """
        :param columns: Количество колонок
        :type columns: int
        :param rows: Количество строк
        :type rows: int
        """
        self._cont = ExtContainer(**kwargs)

        self.__columns_count = 0
        self.__rows_count = 0
        self.__table = []
        self.__rows_height = {}

        # Количество колонок
        self.columns_count = columns

        # Количество строк
        self.rows_count = rows

    def _init_properties(self):
        """
        Первоначальное заполнение матрицы пустыми словарями.
        .. note::
            Вложенный словарь с произвольными свойствами для каждой ячейки,
            например {1: {2: {'width': 100}}},
            где 1-номер колонки, 2-номер строки.
        """
        self._properties = {}
        for col_num in range(self.__columns_count):
            d = dict([(row_num, {}) for row_num in range(self.__rows_count)])
            self._properties[col_num] = d

    def create(self):
        for row_num, row in enumerate(self.__table):
            col_cont_list = []
            for col_num, col in enumerate(row):
                if col is not None:
                    if isinstance(col, int):
                        col = ExtContainer(layout='form', flex=1)
                    elif not isinstance(col, ExtContainer):
                        raise Exception('Unknown type of column "%s"' % col)

                    col_cont_list.append(col)

                    # Устанавливаем произвольные свойства для колонки,
                    # если они есть
                    props = self._properties[col_num][row_num]
                    for key, value in props.items():
                        setattr(col, key, value)

            height = self.__rows_height.get(row_num) or (
                ExtContainerTable._DEFAULT_HEIGHT)

            row_cont = ExtContainer(
                layout_config=dict(align="stretch"),
                layout='hbox',
                height=height
            )
            row_cont.items.extend(col_cont_list)
            self._cont.items.append(row_cont)

        return self._cont

    def set_properties(self, row_num=None, col_num=None, **kwargs):
        """
        Устанавливает свойство контейнера в заданной колонке и(или) строке.
        :param col_num: Номер колонки. Если не задано, то вся колонка.
        :type col_num: int
        :param row_num: Номер строки. Если не задано, то вся строка.
        :type row_num: int

        :raise: AssertionError
        """
        assert col_num is None or 0 <= col_num <= self.columns_count, (
            'Number %s more than the number of columns %s' % (
                col_num, self.columns_count
            )
        )
        assert row_num is None or 0 <= row_num <= self.rows_count, (
            'Number %s more than the number of rows %s' % (
                row_num, self.rows_count
            )
        )
        if col_num is not None and row_num is not None:
            self._properties[col_num][row_num].update(kwargs)
        # Задана только колонка
        elif col_num is not None:
            for d in self._properties[col_num].values():
                d.update(kwargs)
        # Задана только строка
        elif row_num is not None:
            for d in self._properties.values():
                d[row_num].update(kwargs)

    def _make_read_only(
            self, access_off=True, exclude_list=(), *args, **kwargs):
        for item in self.items:
            item.make_read_only(
                access_off, exclude_list, *args, **kwargs)

    @property
    def items(self):
        return [
            col
            for row in self.__table
            for col in row
            if isinstance(col, ExtContainer)
        ]

    @property
    def columns_count(self):
        return self.__columns_count

    @columns_count.setter
    def columns_count(self, value):
        assert isinstance(value, int), 'Value must be INT'
        self.__columns_count = value
        self._init_properties()
        if self.__rows_count:
            self.__init_table()

    @property
    def rows_count(self):
        return self.__rows_count

    @rows_count.setter
    def rows_count(self, value):
        assert isinstance(value, int), 'Value must be INT'
        self.__rows_count = value
        self._init_properties()
        if self.__columns_count:
            self.__init_table()

    def __init_table(self):
        self.__table = [
            range(self.__columns_count)
            for col in range(self.__rows_count)
        ]

    def set_item(self, row, col, cmp, colspan=1, **kwargs):
        """
        Устанавливает контрол *cmp* в ячейку с колонкой *col* и строкой *row*
        :param row: строка
        :type row: int
        :param col: колонка
        :type col: int
        :param cmp: контрол
        :type cmp: BaseExtUIComponent или наследник
        :param colspan: сколько строк будет занимать компонент
        :type colspan: int
        :param **kwargs: свойства контейнера
        """
        assert isinstance(cmp, ExtUIComponent)
        assert isinstance(colspan, int)
        cont = ExtContainer(
            layout='form',
            flex=colspan,
            style=dict(padding="0px")
        )
        # добавляем отступ слева, если это уже не первая колонка
        if col != 0:
            cont.style = dict(padding="0px 0px 0px 5px")
        cmp.anchor = '100%'
        cont.items.append(cmp)
        self.__table[row][col] = cont
        self.set_properties(row, col, **kwargs)
        if colspan > 1:
            self.__table[row][col + 1: col + colspan] = [None] * (colspan - 1)

    def set_row_height(self, row, height):
        """
        Устанавливает ширину и высоту ячейки
        :param row: Индекс ячейки
        :type row: int
        :param height: Высота
        :type height: int
        """
        assert isinstance(height, int), 'Height must be INT'
        assert isinstance(row, int), 'Row num must be INT'
        assert 0 <= row <= self.rows_count, (
            'Row num %d must be in range 0 to %d' % (row, self.rows_count))
        self.__rows_height[row] = height

    def set_rows_height(self, height):
        """
        Устанавливает у всех строк высоту
        :param height: Высота
        :type height: int
        """
        assert isinstance(height, int), 'Height must be INT'
        for row in range(self.rows_count):
            self.__rows_height[row] = height

    def __getattr__(self, item):
        if item.startswith('_') or item in ['columns_count',
                                            'rows_count',
                                            'items']:
            return super(ExtContainerTable, self).__getattr__(item)
        else:
            return getattr(self._cont, item)

    def __setattr__(self, key, value):
        if key.startswith('_') or key in ['columns_count',
                                          'rows_count',
                                          'items']:
            super(ExtContainerTable, self).__setattr__(key, value)

        else:
            setattr(self._cont, key, value)