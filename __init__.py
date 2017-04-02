import os
import json
from cudatext import *
from .dlg import *

dir_icons = os.path.join(os.path.dirname(__file__), 'icons')
fn_ini = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_config_icons.ini')
fn_buttons = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_config_toolbar.json')
name_def = '(default)'

options = {'sub': [], 'clear': False}
blocked = None

if app_api_version()<'1.0.173':
    msg_box('Plugins "Config Toolbar" needs newer CudaText', MB_OK)
    blocked = True

try:
    import cuda_config_icons
    msg_box('Plugin "Config Toolbar" is new one, and "Config Icons" is old one - you must delete "Config Icons" plugin, its functions are included', MB_OK)
except ImportError:
    pass


def do_load_icons(name):
    dir = os.path.join(dir_icons, name)
    if not os.path.isdir(dir): return

    print('Loading icons:', name)
    s = name.split('_')[1].split('x')
    toolbar_proc('top', TOOLBAR_SET_ICON_SIZES, index=int(s[0]), index2=int(s[1]))

    items = toolbar_proc('top', TOOLBAR_ENUM)
    for (i, item) in enumerate(items):
        name = item['cap']
        cmd = item['cmd']
        if not name:
            continue
        if cmd: #user-added item
            continue

        filename = os.path.join(dir, name+'.png')
        if not os.path.isfile(filename):
            print('Cannot find icon:', filename)
            continue
        imageindex = toolbar_proc('top', TOOLBAR_ADD_ICON, text=filename)
        if imageindex is None:
            print('Cannot load icon:', filename)
            continue
        toolbar_proc('top', TOOLBAR_SET_BUTTON, index=i, index2=imageindex)


def do_load_buttons(buttons):
    print('Loading toolbar config')
    for b in buttons:
        fn = b['icon']
        if fn:
            imageindex = toolbar_proc('top', TOOLBAR_ADD_ICON, text=fn)
        else:
            imageindex = -1

        toolbar_proc('top', TOOLBAR_ADD_BUTTON,
            text = b['cap'],
            text2 = b['hint'],
            command = b['cmd'],
            index2 = imageindex
            )


class Command:

    def do_buttons(self):
        global options
        global blocked
        if blocked: return

        res = dialog_buttons(options['sub'], options['clear'])
        if res is None: return
        options['sub'], options['clear'] = res
        with open(fn_buttons, 'w', encoding='utf8') as f:
            f.write(json.dumps(options, indent=2))

        msg_box('Toolbar config will be applied after CudaText restart', MB_OK+MB_ICONINFO)

    def do_icons(self):
        global blocked
        if blocked: return

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
        global options
        global blocked
        global name_def
        if blocked: return

        name = ini_read(fn_ini, 'op', 'set', '')
        if name and name!=name_def:
            do_load_icons(name)

        if os.path.isfile(fn_buttons):
            with open(fn_buttons, 'r', encoding='utf8') as f:
                s = f.read()
                options = json.loads(s)

                if options.get('clear', False):
                    toolbar_proc('top', TOOLBAR_DELETE_ALL)
                do_load_buttons(options['sub'])
