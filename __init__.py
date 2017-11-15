import os
from cudatext import *
from . import opt
from . import dlg
import cudatext_cmd as cmds

icons_default = '(default)'
icons_filenames = {
  cmds.cCommand_ClipboardCopy: 'e_copy',
  cmds.cCommand_ClipboardCut: 'e_cut',
  cmds.cCommand_ClipboardPaste: 'e_paste',
  cmds.cCommand_Undo: 'e_undo',
  cmds.cCommand_Redo: 'e_redo',
  cmds.cmd_FileNew: 'f_new',
  cmds.cmd_FileOpen: 'f_open',
  cmds.cmd_FileSave: 'f_save',
  cmds.cCommand_TextIndent: 'indent',
  cmds.cCommand_TextUnindent: 'unindent',
  cmds.cCommand_ToggleMinimap: 'map',
  cmds.cCommand_ToggleUnprinted: 'unpri',
}


try:
    import cuda_config_icons
    msg_box('Plugin "Config Toolbar" is new one, and "Config Icons" is old one - you must delete "Config Icons" plugin, its functions are included', MB_OK)
except ImportError:
    pass



def do_load_icons(name):

    dir = os.path.join(opt.dir_icon_sets, name)
    if not os.path.isdir(dir): return

    print('Loading icons:', name)
    s = name.split('_')[1].split('x')

    imglist = toolbar_proc('top', TOOLBAR_GET_IMAGELIST)
    imagelist_proc(imglist, IMAGELIST_SET_SIZE, (s[0], s[1]))

    items = toolbar_proc('top', TOOLBAR_ENUM)
    for (i, item) in enumerate(items):
        cmd = item['cmd']
        try:
            cmd_code = int(cmd)
        except:
            continue

        filename = os.path.join(dir, icons_filenames.get(cmd_code, '-')+'.png')
        if not os.path.isfile(filename):
            continue
        imageindex = imagelist_proc(imglist, IMAGELIST_ADD, filename)
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
    imglist = toolbar_proc('top', TOOLBAR_GET_IMAGELIST)

    for (index, b) in enumerate(buttons):
        fn = b['icon']
        imageindex = None
        if fn:
            imageindex = imagelist_proc(imglist, IMAGELIST_ADD, fn)
        if imageindex is None:
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
        if opt.blocked: return

        d = dlg.DialogButtons()
        d.buttons = opt.options['sub']
        d.clear_default = opt.options['clear']
        d.show()
        if d.show_result:
            opt.options['sub'] = d.buttons
            opt.options['clear'] = d.clear_default
            opt.do_save_ops()
            msg_box('Toolbar config will be applied after CudaText restart', MB_OK+MB_ICONINFO)


    def do_icons(self):
        if opt.blocked: return

        dirs = os.listdir(opt.dir_icon_sets)
        if not dirs:
            print('Cannot find icon-sets')
            return
        dirs = [icons_default] + sorted(dirs)
        res = dlg_menu(MENU_LIST, '\n'.join(dirs))
        if res is None: return

        name = dirs[res]
        opt.options['icon_set'] = name
        opt.do_save_ops()

        if name==icons_default:
            msg_box('Default icons will be set after app restart', MB_OK)
            return
        do_load_icons(name)

    def on_start(self, ed_self):
        if opt.blocked: return

        if os.path.isfile(opt.fn_config):
            opt.do_load_ops()

            icons = opt.options.get('icon_set', '')
            if icons and icons!=icons_default:
                do_load_icons(icons)

            if opt.options.get('clear', False):
                toolbar_proc('top', TOOLBAR_DELETE_ALL)
            buttons = opt.options.get('sub', [])
            if buttons:
                do_load_buttons(buttons)
