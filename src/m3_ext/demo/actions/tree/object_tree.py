# coding: utf-8
from django import http

from m3.actions import Action
from m3.actions.results import PreJsonResult
from m3.actions.urls import get_url
from m3_ext.demo.actions.grids.objectgrid import ObjectGridNewAction, ObjectGridEditAction
from m3_ext.demo.actions.tree.trees import TreeDataAction

from m3_ext.ui import all_components as ext
from m3_ext.ui.results import UIJsonEncoder

from m3_ext.demo.actions import UIAction, Pack


@Pack.register
class ObjectTreeAction(UIAction):
    """
    ExtObjectTree
    """
    title = u'ExtObjectTree'

    def get_ui(self, request, context):
        win = super(ObjectTreeAction, self).get_ui(request, context)
        win.layout = win.FIT
        win.width, win.height = 400, 300

        adv_tree = ext.ExtObjectTree()
        adv_tree.add_column(header=u'Имя',
                            data_index='first_name',
                            width=140,
                            sortable=True)
        adv_tree.master_column_id = 'first_name'
        adv_tree.auto_expand_column = 'first_name'
        adv_tree.add_column(header=u'Фамилия',
                            data_index='second_name',
                            width=140)
        # adv_tree.top_bar.button_refresh.text = None

        # adv_tree.url_new = '/data'

        adv_tree.action_data = TreeDataAction

        adv_tree.url_new = get_url(ObjectGridNewAction)
        adv_tree.action_edit = ObjectGridEditAction
        # adv_tree.action_delete = TreeDataAction
        #adv_tree.top_bar.button_new.text = u'Добавить новую роль'
        adv_tree.row_id_name = 'userrole_id'
        adv_tree.use_bbar = True
        adv_tree.sm = ext.ExtGridCheckBoxSelModel()

        win.items.append(adv_tree)
        return win
