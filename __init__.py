import os
import json
from cudatext import *
from .dlg import *

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_config_toolbar.json')
dir_icons = os.path.join(os.path.dirname(__file__), 'icons')
icons_def = '(default)'

options = {
    'icons': '',
    'sub': [],
    'clear': False,
    }
blocked = None

if app_api_version()<'1.0.173':
    msg_box('Plugins "Config Toolbar" needs newer CudaText', MB_OK)
    blocked = True

try:
    import cuda_config_icons
    msg_box('Plugin "Config Toolbar" is new one, and "Config Icons" is old one - you must delete "Config Icons" plugin, its functions are included', MB_OK)
except ImportError:
    pass


def do_load_ops():
    global options
    with open(fn_config, 'r', encoding='utf8') as f:
        options = json.load(f)

def do_save_ops():
    global options
    with open(fn_config, 'w', encoding='utf8') as f:
        f.write(json.dumps(options, indent=2))


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


def do_load_submenu(id_menu, items):

    menu_proc(id_menu, MENU_CLEAR)
    for item in items:
        _cap = item.get('cap', '')
        _cmd = item.get('cmd', 0)
        is_menu = _cmd=='menu'
        if is_menu: _cmd = 0
        id_new = menu_proc(id_menu, MENU_ADD, caption=_cap, command=_cmd)
        if is_menu:
            do_load_submenu(id_new, item.get('sub', []))


def do_load_buttons(buttons):

    print('Loading toolbar config')
    for (index, b) in enumerate(buttons):
        fn = b['icon']
        if fn:
            imageindex = toolbar_proc('top', TOOLBAR_ADD_ICON, text=fn)
        else:
            imageindex = -1

        _cmd = b['cmd']
        is_menu = _cmd=='menu'
        if is_menu:
            _cmd = 'toolmenu:id'+str(index)

        toolbar_proc('top', TOOLBAR_ADD_BUTTON,
            text = b['cap'],
            text2 = b['hint'],
            command = _cmd,
            index2 = imageindex
            )

        if is_menu:
            do_load_submenu(_cmd, b.get('sub', []))


class Command:

    def do_buttons(self):
        global options
        global blocked
        if blocked: return

        res = dialog_buttons(options['sub'], options['clear'])
        if res is None: return
        options['sub'], options['clear'] = res
        do_save_ops()
        msg_box('Toolbar config will be applied after CudaText restart', MB_OK+MB_ICONINFO)


    def do_icons(self):
        global options
        global blocked
        if blocked: return

        dirs = os.listdir(dir_icons)
        if not dirs:
            print('Cannot find icon-sets')
            return
        dirs = [icons_def] + sorted(dirs)
        res = dlg_menu(MENU_LIST, '\n'.join(dirs))
        if res is None: return

        name = dirs[res]
        options['icons'] = name
        do_save_ops()

        if name==icons_def:
            msg_box('Default icons will be set after app restart', MB_OK)
            return
        do_load_icons(name)

    def on_start(self, ed_self):
        global options
        global blocked
        global icons_def
        if blocked: return

        if os.path.isfile(fn_config):
            do_load_ops()

            icons = options.get('icons', '')
            if icons and icons!=icons_def:
                do_load_icons(icons)

            if options.get('clear', False):
                toolbar_proc('top', TOOLBAR_DELETE_ALL)
            buttons = options.get('sub', [])
            if buttons:
                do_load_buttons(buttons)
