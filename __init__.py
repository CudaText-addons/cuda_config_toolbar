import os
from cudatext import *
from . import opt
from . import dlg
import cudatext_cmd as cmds
import cudax_lib as appx


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


_content = []

def get_toolbar_content():

    global _content
    _content = []
    cnt = toolbar_proc('top', TOOLBAR_GET_COUNT)
    for index in range(cnt):
        h = toolbar_proc('top', TOOLBAR_GET_BUTTON_HANDLE, index=index)
        cap = button_proc(h, BTN_GET_TEXT)
        cmd = button_proc(h, BTN_GET_DATA1)
        _content += [(cap, cmd)]


def is_button_present(caption, command):

    for (cap, cmd) in _content:
        if (cap==caption) and (cmd==command):
            return True
    return False


def do_load_buttons(buttons):

    print('Loading toolbar config')
    imglist = toolbar_proc('top', TOOLBAR_GET_IMAGELIST)

    get_toolbar_content()

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

        # prevent duplicate btns on "reset python plugins"
        if is_button_present(b['cap'], _cmd):
            continue

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


    def on_start(self, ed_self):

        if os.path.isfile(opt.fn_config):
            opt.do_load_ops()

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


    def _choose_icons(self, icon_dir, icon_option, icon_def):

        dir = os.path.join(app_path(APP_DIR_DATA), icon_dir)
        dirs = sorted(os.listdir(dir))
        if not dirs: return

        opt = appx.get_opt(icon_option, icon_def, appx.CONFIG_LEV_USER)
        try:
            index = dirs.index(opt)
        except:
            index = -1

        res = dlg_menu(MENU_LIST, dirs, focused=index)
        if res is None: return

        opt = dirs[res]
        appx.set_opt(icon_option, opt, appx.CONFIG_LEV_USER)
        opt_now = appx.get_opt(icon_option)
        if opt != opt_now:
            msg_box('Error writing option to user.json\nGot value "{}"'.format(opt_now), MB_OK+MB_ICONERROR)
        else:
            msg_box('Changed option in user.json, restart app to see effect', MB_OK+MB_ICONINFO)


    def icons_toolbar(self):
        self._choose_icons('toolbaricons', 'ui_toolbar_theme', 'default_24x24')

    def icons_sidebar(self):
        self._choose_icons('sideicons', 'ui_sidebar_theme', 'common_20x20')

    def icons_codetree(self):
        self._choose_icons('codetreeicons', 'ui_tree_theme', 'default_16x16')
