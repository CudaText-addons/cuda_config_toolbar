import os
import json
from cudatext import *
from .dlg import *

dir_icons = os.path.join(os.path.dirname(__file__), 'icons')
fn_ini = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_config_icons.ini')
fn_buttons = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_config_toolbar.json')
name_def = '(default)'

buttons = []

def do_load_icons(name):
    dir = os.path.join(dir_icons, name)
    if not os.path.isdir(dir): return

    print('Setting icons:', name)
    s = name.split('_')[1].split('x')
    app_proc(PROC_TOOLBAR_ICON_SET_SIZE, s[0]+','+s[1])

    names = app_proc(PROC_TOOLBAR_ENUM, '').splitlines()
    for (i, name) in enumerate(names):
        if not name: continue
        name = name.split(';')[1]
        if not name: continue
        filename = os.path.join(dir, name+'.png')
        if not os.path.isfile(filename):
            print('Cannot find icon:', filename)
            continue
        index = app_proc(PROC_TOOLBAR_ICON_ADD, filename)
        if index is None:
            print('Cannot load icon:', filename)
            continue
        app_proc(PROC_TOOLBAR_ICON_SET, str(i)+','+str(index))


def do_load_buttons(buttons):
    print('btn cnt: ', str(len(buttons)))


class Command:

    def do_buttons(self):
        global buttons
        res = dialog_buttons(buttons)
        if not res: return
        buttons = res
        with open(fn_buttons, 'w', encoding='utf8') as f:
            f.write(json.dumps(buttons, indent=2))

        msg_box('Toolbar config will be applied after CudaText restart', MB_OK+MB_ICONINFO)

    def do_icons(self):
        dirs = os.listdir(dir_icons)
        if not dirs:
            print('Cannot find icon-sets')
            return
        dirs = [name_def] + sorted(dirs)
        res = dlg_menu(MENU_LIST, '\n'.join(dirs))
        if res is None: return

        name = dirs[res]
        ini_write(fn_ini, 'op', 'set', name)

        if name==name_def:
            msg_box('Default icons will be set after app restart', MB_OK)
            return
        do_load_icons(name)

    def on_start(self, ed_self):
        global buttons
        global name_def

        name = ini_read(fn_ini, 'op', 'set', '')
        if name and name!=name_def:
            do_load_icons(name)

        if os.path.isfile(fn_buttons):
            with open(fn_buttons, 'r', encoding='utf8') as f:
                s = f.read()
                buttons = json.loads(s)
                do_load_buttons(buttons)
