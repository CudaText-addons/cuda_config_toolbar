import os
import time
from cudatext import *
from . import opt

from cudax_lib import get_translation
_   = get_translation(__file__)  # I18N

bar_h = app_proc(PROC_GET_MAIN_TOOLBAR, '')

def get_count():

    return toolbar_proc(bar_h, TOOLBAR_GET_COUNT)


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
    for index in range(get_count()):
        h = toolbar_proc(bar_h, TOOLBAR_GET_BUTTON_HANDLE, index=index)
        cap = button_proc(h, BTN_GET_TEXT)
        cmd = button_proc(h, BTN_GET_DATA1)
        _content += [(cap, cmd)]


def is_button_present(caption, command):

    for (cap, cmd) in _content:
        if (cap==caption) and (cmd==command):
            return True
    return False


def do_load_buttons(buttons):

    imglist = toolbar_proc(bar_h, TOOLBAR_GET_IMAGELIST)

    get_toolbar_content()
    cnt = get_count()

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

        if is_menu:
            toolbar_proc(bar_h, TOOLBAR_ADD_MENU)
        else:
            toolbar_proc(bar_h, TOOLBAR_ADD_ITEM)

        cnt += 1
        btn = toolbar_proc(bar_h, TOOLBAR_GET_BUTTON_HANDLE,
            index=cnt-1 )
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

        if is_menu:
            do_load_submenu(_cmd, b.get('sub', []))

    toolbar_proc(bar_h, TOOLBAR_UPDATE)


def do_update_buttons_visible():

    cur_lexer = ed.get_prop(PROP_LEXER_FILE).lower()
    if not cur_lexer:
        cur_lexer = '-'

    update_needed = False
    cnt = get_count()

    for i in range(cnt):
        btn = toolbar_proc(bar_h, TOOLBAR_GET_BUTTON_HANDLE, index=i)
        lexers = button_proc(btn, BTN_GET_DATA2)
        if not lexers: continue
        vis_now = ','+cur_lexer+',' in ','+lexers.lower()+','
        vis_before = button_proc(btn, BTN_GET_VISIBLE)
        if vis_now!=vis_before:
            update_needed = True
            button_proc(btn, BTN_SET_VISIBLE, vis_now)

    if update_needed:
        toolbar_proc(bar_h, TOOLBAR_UPDATE)


class Command:

    std_count = 0

    def do_buttons(self):

        from . import dlg
        d = dlg.DialogButtons()
        d.buttons = list(opt.options['sub']) #copy object
        d.show()
        if d.show_result:
            opt.options['sub'] = list(d.buttons) #copy back
            opt.do_save_ops()

            self.apply_user_buttons()


    def on_start(self, ed_self):

        self.std_count = get_count()

        if os.path.isfile(opt.fn_config):
            tick = time.monotonic()

            # Cud <=1.92.0 had slowdown with ConfigToolbar
            vis = app_proc(PROC_SHOW_TOOLBAR_GET, '')
            if vis:
                app_proc(PROC_SHOW_TOOLBAR_SET, False)

            opt.do_load_ops()

            hide_list = opt.hide.split(' ')
            hide_list = [i for i in hide_list if i]
            if hide_list:
                hide_list = reversed(sorted(list(map(int, hide_list))))
                for i in hide_list:
                    toolbar_proc(bar_h, TOOLBAR_DELETE_BUTTON, index=i)

            self.std_count = get_count()
            self.apply_user_buttons(True)

            if vis:
                app_proc(PROC_SHOW_TOOLBAR_SET, True)
            tick = (time.monotonic() - tick) * 1000
            print(_('Loading toolbar config (%dms)') % tick)


    def apply_user_buttons(self, upd_btn_visible=True):

        # delete old user buttons
        for i in reversed(range(self.std_count, get_count())):
            toolbar_proc(bar_h, TOOLBAR_DELETE_BUTTON, index=i)

        buttons = opt.options.get('sub', [])
        if buttons:
            do_load_buttons(buttons)
            if upd_btn_visible:
                do_update_buttons_visible()


    def on_lexer(self, ed_self):

        do_update_buttons_visible()

    def on_focus(self, ed_self):

        do_update_buttons_visible()

    def on_open(self, ed_self):

        do_update_buttons_visible()


    def _choose_icons(self, icon_dir, icon_option, icon_def):

        import cudax_lib as appx

        dir = os.path.join(app_path(APP_DIR_DATA), icon_dir)
        dirs = sorted(os.listdir(dir))
        if not dirs: return

        s = appx.get_opt(icon_option, icon_def, appx.CONFIG_LEV_USER)
        try:
            index = dirs.index(s)
        except:
            index = -1

        res = dlg_menu(DMENU_LIST, dirs, focused=index)
        if res is None: return

        s = dirs[res]
        appx.set_opt(icon_option, s, appx.CONFIG_LEV_USER)
        s_now = appx.get_opt(icon_option)
        if s != s_now:
            msg_box(_('Error writing option to user.json\nGot value "{}"').format(s_now), MB_OK+MB_ICONERROR)
        else:
            msg_box(_('Changed option in user.json, restart app to see effect'), MB_OK+MB_ICONINFO)


    def icons_toolbar(self):
        self._choose_icons('toolbaricons', 'ui_toolbar_theme', 'default_24x24')

    def icons_sidebar(self):
        self._choose_icons('sideicons', 'ui_sidebar_theme', 'common_20x20')

    def icons_codetree(self):
        self._choose_icons('codetreeicons', 'ui_tree_theme', 'default_16x16')

    def hide_std(self):

        res = dlg_input(_('Indexes of buttons to hide, space-separated (e.g. "0 2 10 11"):'), opt.hide)
        if res is None: return
        opt.hide = res
        opt.do_save_ops()
        msg_box(_('Option will be applied after app restart'), MB_OK+MB_ICONINFO)
