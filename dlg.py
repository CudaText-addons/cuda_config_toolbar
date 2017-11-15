import os
from cudatext import *
from . import opt


class DialogButtons:

    buttons = []
    clear_default = False
    is_submenu = False
    h_main = None
    show_result = False

    def update_list(self):

        items = [
            '(menu) '+item['cap'] if item['cmd']=='menu' else
            '(icon) '+item['hint'] if item['cap']=='' else
            item['cap']
            for item in self.buttons
            ]
        items = ['---' if s=='-' else '(icon)' if s=='' else s for s in items]
        items = '\t'.join(items)

        dlg_proc(self.h_main, DLG_CTL_PROP_SET, name='list', prop={'items': items} )


    def show(self):

        self.update_list()
        self.set_index(0)
        dlg_proc(self.h_main, DLG_CTL_FOCUS, name='list')
        dlg_proc(self.h_main, DLG_SHOW_MODAL)


    def callback_main_ok(self, id_dlg, id_ctl, data='', info=''):

        self.show_result = True
        dlg_proc(id_dlg, DLG_HIDE)


    def callback_main_cancel(self, id_dlg, id_ctl, data='', info=''):

        dlg_proc(id_dlg, DLG_HIDE)


    def callback_main_edit(self, id_dlg, id_ctl, data='', info=''):

        index = self.get_index()
        if index<0: return
        b = self.buttons[index]

        d = DialogProps()
        dlg_proc(d.h_dlg, DLG_CTL_PROP_SET, name='edit_cap', prop={'val': b['cap']})
        dlg_proc(d.h_dlg, DLG_CTL_PROP_SET, name='edit_tooltip', prop={'val': b['hint']})
        dlg_proc(d.h_dlg, DLG_CTL_PROP_SET, name='edit_cmd', prop={'val': b['cmd']})
        dlg_proc(d.h_dlg, DLG_CTL_PROP_SET, name='edit_icon', prop={'val': b['icon']})

        d.show()
        if d.show_result:
            b['cap'] = dlg_proc(d.h_dlg, DLG_CTL_PROP_GET, name='edit_cap')['val']
            b['hint'] = dlg_proc(d.h_dlg, DLG_CTL_PROP_GET, name='edit_tooltip')['val']
            b['cmd'] = dlg_proc(d.h_dlg, DLG_CTL_PROP_GET, name='edit_cmd')['val']
            b['icon'] = dlg_proc(d.h_dlg, DLG_CTL_PROP_GET, name='edit_icon')['val']
            self.update_list()

        dlg_proc(d.h_dlg, DLG_FREE)


    def get_index(self):

        p = dlg_proc(self.h_main, DLG_CTL_PROP_GET, name='list')
        return int(p['val'])


    def set_index(self, value):

        count = self.get_count()
        if value<0:
            value=0
        if value>=count:
            value = count-1
        dlg_proc(self.h_main, DLG_CTL_PROP_SET, name='list', prop={'val': value})


    def get_count(self):

        return len(self.buttons)


    def __init__(self):

        h=dlg_proc(0, DLG_CREATE)
        dlg_proc(h, DLG_PROP_SET, prop={'cap':'Configure toolbar', 'w': 430, 'h': 500 })

        n=dlg_proc(h, DLG_CTL_ADD, 'listbox')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'list',
          'w': 200,
          'align': ALIGN_LEFT,
          'sp_a': 10,
           } )

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_edit',
          'x': 220,
          'w': 200,
          'y': 10,
          'cap': 'Edit item...',
          'on_change': self.callback_main_edit,
           } )

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_ok',
          'x': 220,
          'w': 200,
          'y': 430,
          'cap': 'OK',
          'on_change': self.callback_main_ok,
           } )

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_cancel',
          'x': 220,
          'w': 200,
          'y': 460,
          'cap': 'Cancel',
          'on_change': self.callback_main_cancel,
           } )

        self.h_main = h


class DialogProps:

    cap = ''
    hint = ''
    cmd = 0
    icon = ''
    show_result = False
    h_dlg = None

    def show(self):

        dlg_proc(self.h_dlg, DLG_SHOW_MODAL)


    def callback_props_ok(self, id_dlg, id_ctl, data='', info=''):

        self.show_result = True
        dlg_proc(id_dlg, DLG_HIDE)


    def callback_props_cancel(self, id_dlg, id_ctl, data='', info=''):

        dlg_proc(id_dlg, DLG_HIDE)


    def callback_props_cmd(self, id_dlg, id_ctl, data='', info=''):

        s = dlg_commands(COMMANDS_USUAL+COMMANDS_PLUGINS)
        if s:
            s = s[2:]
            dlg_proc(id_dlg, DLG_CTL_PROP_SET, name='edit_cmd', prop={'val': s})


    def callback_props_menu(self, id_dlg, id_ctl, data='', info=''):

        dlg_proc(id_dlg, DLG_CTL_PROP_SET, name='edit_cmd', prop={'val': 'menu'})


    def callback_props_icon(self, id_dlg, id_ctl, data='', info=''):

        s = dlg_file(True, '', opt.dir_icons, 'Image files|*.png;*.bmp')
        if s:
            opt.dir_icons = os.path.dirname(s)
            dlg_proc(id_dlg, DLG_CTL_PROP_SET, name='edit_icon', prop={'val': s})


    def __init__(self):

        h=dlg_proc(0, DLG_CREATE)
        dlg_proc(h, DLG_PROP_SET, prop={'cap':'Button properties', 'w': 540, 'h': 216 })

        n=dlg_proc(h, DLG_CTL_ADD, 'label')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'label_cap',
          'x': 10,
          'y': 10,
          'w': 120,
          'cap': 'Caption:',
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'edit')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'edit_cap',
          'x': 130,
          'y': 8,
          'w': 400,
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'label')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'label_tooltip',
          'x': 10,
          'y': 40,
          'w': 120,
          'cap': 'Tooltip:',
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'edit')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'edit_tooltip',
          'x': 130,
          'y': 38,
          'w': 400,
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_cmd',
          'x': 10,
          'y': 70,
          'w': 115,
          'cap': 'Command...',
          'on_change': self.callback_props_cmd,
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_cmd_menu',
          'x': 10,
          'y': 100,
          'w': 115,
          'cap': 'Sub-menu',
          'on_change': self.callback_props_menu,
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'edit')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'edit_cmd',
          'x': 130,
          'y': 68,
          'w': 400,
          'props': (True, False, True),
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_icon',
          'x': 10,
          'y': 130,
          'w': 115,
          'cap': 'Icon...',
          'on_change': self.callback_props_icon,
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'edit')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'edit_icon',
          'x': 130,
          'y': 128,
          'w': 400,
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_ok',
          'x': 320,
          'y': 180,
          'w': 100,
          'cap': 'OK',
          'on_change': self.callback_props_ok,
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_cancel',
          'x': 430,
          'y': 180,
          'w': 100,
          'cap': 'Cancel',
          'on_change': self.callback_props_cancel,
          } )

        self.h_dlg = h



def _dialog_buttons(buttons, chk_clear, is_submenu=False):

    while True:

        b_sel = '1' if val_index>=0 else '0'
        b_sel_menu = '1' if val_index>=0 and buttons[val_index]['cmd']=='menu' else '0'
        b_en_up = '1' if val_index>0 else '0'
        b_en_down = '1' if (val_index>=0 and val_index<len(buttons)-1) else '0'
        b_clear = '1' if chk_clear else '0'
        b_en_clear = '1' if not is_submenu else '0'

            #, c1.join(['type=button', 'pos=200,210,394,0', 'cap=Add &button'])
            #, c1.join(['type=button', 'pos=200,240,394,0', 'cap=Add &separator'])
            #, c1.join(['type=button', 'pos=400,210,600,0', 'cap=Chan&ge selected item', 'en='+b_sel])
            #, c1.join(['type=button', 'pos=400,240,600,0', 'cap=&Delete selected item', 'en='+b_sel])
            #, c1.join(['type=button', 'pos=400,270,600,0', 'cap=&Config selected menu...', 'en='+b_sel_menu])
            #, c1.join(['type=check', 'pos=200,330,600,0', 'cap=Remo&ve standard buttons', 'val='+b_clear, 'en='+b_en_clear])

            #if not val_cap and not val_icon:
            #    msg_box('Button needs caption, or icon, or caption+icon', MB_OK+MB_ICONWARNING)
            #    continue
            #d = {'cap': val_cap, 'hint': val_hint, 'cmd': val_cmd, 'icon': val_icon}
            #buttons.append(d)

        #if res==RES_B_ADDSEP:
        #    d = {'cap': '-', 'hint': '', 'cmd': '', 'icon': ''}
        #    buttons.append(d)

#        if res==RES_MOVE_UP:
#            buttons.insert(val_index-1, buttons.pop(val_index))
#            val_index -= 1
#
#        if res==RES_MOVE_DOWN:
#            buttons.insert(val_index+1, buttons.pop(val_index))
#            val_index += 1

#        if res==RES_CONFIG_SUBMENU:
#            subitems = buttons[val_index].get('sub', [])
#            res = dialog_buttons(subitems, False, True)
#            if res:
#                buttons[val_index]['sub'] = subitems
#
