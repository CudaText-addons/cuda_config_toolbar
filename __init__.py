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


def do_load_icons(name):

    dir = os.path.join(opt.dir_icon_sets, name)
    if not os.path.isdir(dir): return

    print('Loading icons:', name)
    s = name.split('_')[1].split('x')

    imglist = toolbar_proc('top', TOOLBAR_GET_IMAGELIST)
    imagelist_proc(imglist, IMAGELIST_SET_SIZE, (s[0], s[1]))

    if True:
        count = toolbar_proc('top', TOOLBAR_GET_COUNT)
        for i in range(count):
            btn = toolbar_proc('top', TOOLBAR_GET_BUTTON_HANDLE, index=i)
            cmd = button_proc(btn, BTN_GET_DATA1)
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
            button_proc(btn, BTN_SET_IMAGEINDEX, imageindex)

        toolbar_proc('top', TOOLBAR_UPDATE)


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
        fn = opt.decode_fn(b['icon'])
        imageindex = None
        if fn:
            imageindex = imagelist_proc(imglist, IMAGELIST_ADD, fn)
        if imageindex is None:
            imageindex = -1

        _cmd = b['cmd']
        is_menu = _cmd=='menu'
        if is_menu:
            _cmd = 'toolmenu:id'+str(index)

        if True:
            if is_menu:
                toolbar_proc('top', TOOLBAR_ADD_MENU)
            else:
                toolbar_proc('top', TOOLBAR_ADD_ITEM)

            btn = toolbar_proc('top', TOOLBAR_GET_BUTTON_HANDLE,
                index=toolbar_proc('top', TOOLBAR_GET_COUNT)-1 )
            nkind = BTNKIND_SEP_HORZ if b['cap']=='-' \
                else BTNKIND_TEXT_ONLY if imageindex<0 \
                else BTNKIND_ICON_ONLY if not b['cap'] \
                else BTNKIND_TEXT_ICON_HORZ

            button_proc(btn, BTN_SET_TEXT, b['cap'])
            button_proc(btn, BTN_SET_HINT, b['hint'])
            button_proc(btn, BTN_SET_DATA1, _cmd)
            button_proc(btn, BTN_SET_DATA2, b.get('lexers', ''))
            button_proc(btn, BTN_SET_IMAGEINDEX, imageindex)
            button_proc(btn, BTN_SET_KIND, nkind)

            if b['cap']:
                button_proc(btn, BTN_SET_ARROW_ALIGN, 'R')

            toolbar_proc('top', TOOLBAR_UPDATE)

        else:
            #---del this block later
            toolbar_proc('top', TOOLBAR_ADD_BUTTON,
                text = b['cap'],
                text2 = b['hint'],
                command = _cmd,
                index2 = imageindex
                )

        if is_menu:
            do_load_submenu(_cmd, b.get('sub', []))


def do_update_buttons_visible():

    cur_lexer = ed.get_prop(PROP_LEXER_FILE).lower()
    if not cur_lexer:
        cur_lexer = '-'

    update_needed = False
    cnt = toolbar_proc('top', TOOLBAR_GET_COUNT)

    for i in range(cnt):
        btn = toolbar_proc('top', TOOLBAR_GET_BUTTON_HANDLE, index=i)
        lexers = button_proc(btn, BTN_GET_DATA2)
        if not lexers: continue
        vis_now = ','+cur_lexer+',' in ','+lexers.lower()+','
        vis_before = button_proc(btn, BTN_GET_VISIBLE)
        if vis_now!=vis_before:
            update_needed = True
            button_proc(btn, BTN_SET_VISIBLE, vis_now)

    if update_needed:
        toolbar_proc('top', TOOLBAR_UPDATE)


class Command:

    def do_buttons(self):

        d = dlg.DialogButtons()
        d.buttons = list(opt.options['sub']) #copy object
        d.show()
        if d.show_result:
            opt.options['sub'] = list(d.buttons) #copy back
            opt.do_save_ops()
            msg_box('Toolbar config will be applied after CudaText restart', MB_OK+MB_ICONINFO)


    def do_icons(self):

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

        if os.path.isfile(opt.fn_config):
            opt.do_load_ops()

            icons = opt.options.get('icon_set', '')
            if icons and icons!=icons_default:
                do_load_icons(icons)

            hide_list = opt.hide.split(' ')
            hide_list = [i for i in hide_list if i]
            if hide_list:
                hide_list = reversed(sorted(list(map(int, hide_list))))
                for i in hide_list:
                    toolbar_proc('top', TOOLBAR_DELETE_BUTTON, index=i)

            buttons = opt.options.get('sub', [])
            if buttons:
                do_load_buttons(buttons)
                do_update_buttons_visible()


    def on_lexer(self, ed_self):

        do_update_buttons_visible()

    def on_focus(self, ed_self):

        do_update_buttons_visible()

