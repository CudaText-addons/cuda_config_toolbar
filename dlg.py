import os
from cudatext import *
from shutil import copyfile
from . import opt
from . import dlg_choose_icon

from cudax_lib import get_translation
_   = get_translation(__file__)  # i18n


class DialogButtons:

    buttons = []
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

        n = self.get_index()
        dlg_proc(self.h_main, DLG_CTL_PROP_SET, name='list', prop={'items': items} )
        self.set_index(n)
        self.update_en()


    def update_en(self):

        n = self.get_index()
        dlg_proc(self.h_main, DLG_CTL_PROP_SET, name='btn_del', prop={'en': n>=0})
        dlg_proc(self.h_main, DLG_CTL_PROP_SET, name='btn_edit', prop={'en': n>=0 and self.buttons[n]['cap']!='-' })
        dlg_proc(self.h_main, DLG_CTL_PROP_SET, name='btn_edit_sub', prop={'en': n>=0 and self.buttons[n]['cmd']=='menu' })

        dlg_proc(self.h_main, DLG_CTL_PROP_SET, name='btn_move_up', prop={'en': n>0})
        dlg_proc(self.h_main, DLG_CTL_PROP_SET, name='btn_move_down', prop={'en': n<self.get_count()-1 })


    def show(self):

        self.update_list()
        self.set_index(0)

        dlg_proc(self.h_main, DLG_CTL_FOCUS, name='list')
        dlg_proc(self.h_main, DLG_SCALE)
        dlg_proc(self.h_main, DLG_SHOW_MODAL)


    def call_ok(self, id_dlg, id_ctl, data='', info=''):

        self.show_result = True
        dlg_proc(id_dlg, DLG_HIDE)


    def call_cancel(self, id_dlg, id_ctl, data='', info=''):

        dlg_proc(id_dlg, DLG_HIDE)


    def call_move_up(self, id_dlg, id_ctl, data='', info=''):

        index = self.get_index()
        if index<1: return
        self.buttons.insert(index-1, self.buttons.pop(index))
        self.set_index(index-1)
        self.update_list()


    def call_move_down(self, id_dlg, id_ctl, data='', info=''):

        index = self.get_index()
        if index<0 or index>=self.get_count(): return
        self.buttons.insert(index+1, self.buttons.pop(index))
        self.set_index(index+1)
        self.update_list()


    def call_del(self, id_dlg, id_ctl, data='', info=''):

        index = self.get_index()
        if index<0: return
        del self.buttons[index]
        self.update_list()


    def add_data_from_dlg(self, h_dlg):
    
        b = {}
        b['cap'] = dlg_proc(h_dlg, DLG_CTL_PROP_GET, name='edit_cap')['val']
        b['hint'] = dlg_proc(h_dlg, DLG_CTL_PROP_GET, name='edit_tooltip')['val']
        b['cmd'] = dlg_proc(h_dlg, DLG_CTL_PROP_GET, name='edit_cmd')['val']
        b['icon'] = opt.encode_fn( dlg_proc(h_dlg, DLG_CTL_PROP_GET, name='edit_icon')['val'] )
        b['lexers'] = dlg_proc(h_dlg, DLG_CTL_PROP_GET, name='edit_lexers')['val']
        self.buttons.append(b)
        self.update_list()

    def call_add(self, id_dlg, id_ctl, data='', info=''):

        d = DialogProps()
        d.show()
        if d.show_result:
            self.add_data_from_dlg(d.h_dlg)

        dlg_proc(d.h_dlg, DLG_FREE)


    def call_add_menu(self, id_dlg, id_ctl, data='', info=''):

        d = DialogProps()
        dlg_proc(d.h_dlg, DLG_CTL_PROP_SET, name='edit_cmd', prop={'val': 'menu'})
        dlg_proc(d.h_dlg, DLG_CTL_PROP_SET, name='btn_cmd', prop={'en': False})
        d.show()
        if d.show_result:
            self.add_data_from_dlg(d.h_dlg)

        dlg_proc(d.h_dlg, DLG_FREE)


    def call_add_sep(self, id_dlg, id_ctl, data='', info=''):

        b = {}
        b['cap'] = '-'
        b['hint'] = ''
        b['cmd'] = ''
        b['icon'] = ''
        self.buttons.append(b)
        self.update_list()


    def call_edit_sub(self, id_dlg, id_ctl, data='', info=''):

        index = self.get_index()
        if index<0: return

        delta = 30
        prop = dlg_proc(id_dlg, DLG_PROP_GET)

        d = DialogButtons()
        dlg_proc(d.h_main, DLG_PROP_SET, prop={
            'x': prop['x']+delta,
            'y': prop['y']+delta
            })

        d.buttons = list(self.buttons[index].get('sub', []))
        d.is_submenu = True
        d.show()
        if d.show_result:
            self.buttons[index]['sub'] = list(d.buttons)
        dlg_proc(d.h_main, DLG_FREE)


    def call_edit(self, id_dlg, id_ctl, data='', info=''):

        index = self.get_index()
        if index<0: return
        b = self.buttons[index]

        d = DialogProps()
        dlg_proc(d.h_dlg, DLG_CTL_PROP_SET, name='edit_cap', prop={'val': b['cap']})
        dlg_proc(d.h_dlg, DLG_CTL_PROP_SET, name='edit_tooltip', prop={'val': b['hint']})
        dlg_proc(d.h_dlg, DLG_CTL_PROP_SET, name='edit_cmd', prop={'val': b['cmd']})
        dlg_proc(d.h_dlg, DLG_CTL_PROP_SET, name='edit_icon', prop={'val': b['icon'] })
        dlg_proc(d.h_dlg, DLG_CTL_PROP_SET, name='edit_lexers', prop={'val': b.get('lexers', '') })

        d.show()
        if d.show_result:
            b['cap'] = dlg_proc(d.h_dlg, DLG_CTL_PROP_GET, name='edit_cap')['val']
            b['hint'] = dlg_proc(d.h_dlg, DLG_CTL_PROP_GET, name='edit_tooltip')['val']
            b['cmd'] = dlg_proc(d.h_dlg, DLG_CTL_PROP_GET, name='edit_cmd')['val']
            b['icon'] = opt.encode_fn( dlg_proc(d.h_dlg, DLG_CTL_PROP_GET, name='edit_icon')['val'] )
            b['lexers'] = dlg_proc(d.h_dlg, DLG_CTL_PROP_GET, name='edit_lexers')['val']
            self.update_list()

        dlg_proc(d.h_dlg, DLG_FREE)


    def call_list_change(self, id_dlg, id_ctl, data='', info=''):

        self.update_en()


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
        dlg_proc(h, DLG_PROP_SET, prop={'cap':_('Configure toolbar'), 'w': 430, 'h': 500 })

        n=dlg_proc(h, DLG_CTL_ADD, 'listbox')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'list',
          'w': 200,
          'align': ALIGN_LEFT,
          'sp_a': 10,
          'act': True,
          'on_change': self.call_list_change,
           } )

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_add',
          'x': 220,
          'w': 200,
          'y': 10,
          'cap': _('Add item...'),
          'on_change': self.call_add,
           } )

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_add_menu',
          'x': 220,
          'w': 200,
          'y': 40,
          'cap': _('Add sub-menu...'),
          'on_change': self.call_add_menu,
           } )

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_add_sep',
          'x': 220,
          'w': 200,
          'y': 70,
          'cap': _('Add separator'),
          'on_change': self.call_add_sep,
           } )

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_edit',
          'x': 220,
          'w': 200,
          'y': 130,
          'cap': _('Edit item...'),
          'on_change': self.call_edit,
           } )

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_edit_sub',
          'x': 220,
          'w': 200,
          'y': 160,
          'cap': _('Edit sub-menu...'),
          'on_change': self.call_edit_sub,
           } )

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_del',
          'x': 220,
          'w': 200,
          'y': 220,
          'cap': _('Delete item'),
          'on_change': self.call_del,
           } )

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_move_up',
          'x': 220,
          'w': 200,
          'y': 280,
          'cap': _('Move up'),
          'on_change': self.call_move_up,
           } )

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_move_down',
          'x': 220,
          'w': 200,
          'y': 310,
          'cap': _('Move down'),
          'on_change': self.call_move_down,
           } )

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_ok',
          'x': 220,
          'w': 200,
          'y': 430,
          'cap': _('OK'),
          'on_change': self.call_ok,
           } )

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_cancel',
          'x': 220,
          'w': 200,
          'y': 460,
          'cap': _('Cancel'),
          'on_change': self.call_cancel,
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

        dlg_proc(self.h_dlg, DLG_SCALE)
        dlg_proc(self.h_dlg, DLG_SHOW_MODAL)


    def call_ok(self, id_dlg, id_ctl, data='', info=''):

        prop1 = dlg_proc(id_dlg, DLG_CTL_PROP_GET, name='edit_cap')
        prop2 = dlg_proc(id_dlg, DLG_CTL_PROP_GET, name='edit_icon')
        if not prop1['val'] and not prop2['val']:
            msg_box(_('Button must have non-empty caption and/or icon'), MB_OK+MB_ICONWARNING)
            return

        self.show_result = True
        dlg_proc(id_dlg, DLG_HIDE)


    def call_cancel(self, id_dlg, id_ctl, data='', info=''):

        dlg_proc(id_dlg, DLG_HIDE)


    def call_cmd(self, id_dlg, id_ctl, data='', info=''):

        s = dlg_commands(COMMANDS_USUAL+COMMANDS_PLUGINS+COMMANDS_CENTERED, _('Button command'))
        if s:
            s = s[2:]
            dlg_proc(id_dlg, DLG_CTL_PROP_SET, name='edit_cmd', prop={'val': s})


    def call_cmdline(self, id_dlg, id_ctl, data='', info=''):
        
        prefix = 'exec='
        prop = dlg_proc(id_dlg, DLG_CTL_PROP_GET, name='edit_cmd')
        old_val = prop['val']
        if old_val.startswith(prefix):
            old_val = old_val[len(prefix):]
        else:
            old_val = ''

        s = dlg_input(_('Command line parameter(s):'), old_val)
        if s is not None:
            new_val = (prefix+s) if s else ''
            dlg_proc(id_dlg, DLG_CTL_PROP_SET, name='edit_cmd', prop={'val': new_val})


    def set_icon(self, filename):

        dir_sett = app_path(APP_DIR_SETTINGS)
        dir_icons = os.path.join(dir_sett, 'tool_icons')
        if not os.path.isdir(dir_icons):
            os.mkdir(dir_icons)

        filename2 = os.path.join(
            dir_icons,
            os.path.basename(os.path.dirname(filename))+'@'+os.path.basename(filename)
            )
        copyfile(filename, filename2)

        fn = filename2
        if fn.startswith(dir_sett):
            fn = fn.replace(dir_sett, '{op}')

        dlg_proc(self.h_dlg, DLG_CTL_PROP_SET, name='edit_icon', prop={'val': fn})


    def call_icon_file(self, id_dlg, id_ctl, data='', info=''):

        res = dlg_file(True, '', '', _('PNG files')+'|*.png')
        if not res: return
        self.set_icon(res)


    def call_icon(self, id_dlg, id_ctl, data='', info=''):

        dir = os.path.join(os.path.dirname(__file__), 'icons')
        d = dlg_choose_icon.DialogChooseIcon()
        res = d.choose_icon(dir)
        if res:
            filename, size = res
            self.set_icon(filename)


    def __init__(self):

        h=dlg_proc(0, DLG_CREATE)
        dlg_proc(h, DLG_PROP_SET, prop={'cap':_('Button properties'), 'w': 600, 'h': 325 })

        n=dlg_proc(h, DLG_CTL_ADD, 'label')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'label_cap',
          'x': 10,
          'y': 10,
          'w': 130,
          'cap': _('Caption:'),
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'edit')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'edit_cap',
          'x': 150,
          'y': 8,
          'w': 440,
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'label')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'label_tooltip',
          'x': 10,
          'y': 40,
          'w': 130,
          'cap': _('Tooltip:'),
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'edit')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'edit_tooltip',
          'x': 150,
          'y': 38,
          'w': 440,
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'label')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'label_cmd',
          'x': 10,
          'y': 70,
          'w': 130,
          'cap': _('Command:'),
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'edit')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'edit_cmd',
          'x': 150,
          'y': 68,
          'w': 440,
          'ex0': True, 
          'ex1': False, 
          'ex2': True,
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_cmd',
          'x': 150,
          'y': 100,
          'w': 180,
          'cap': _('Choose command...'),
          'on_change': self.call_cmd,
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_cmdline',
          'x': 340,
          'y': 100,
          'w': 180,
          'cap': _('Enter command line...'),
          'on_change': self.call_cmdline,
          'en': app_api_version() >= '1.0.411',
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'label')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'label_icon',
          'x': 10,
          'y': 130,
          'w': 130,
          'cap': _('Icon:'),
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'edit')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'edit_icon',
          'x': 150,
          'y': 128,
          'w': 440,
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'label')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'label_op_hint',
          'cap': _('{op} - path to "settings" dir'),
          'x': 150,
          'y': 160,
          'w': 400,
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_icon',
          'x': 150,
          'y': 182,
          'w': 180,
          'cap': _('Choose from icon set...'),
          'on_change': self.call_icon,
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_icon_file',
          'x': 340,
          'y': 182,
          'w': 180,
          'cap': _('Choose from file...'),
          'on_change': self.call_icon_file,
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'label')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'label_xsets',
          'x': 150,
          'y': 212,
          'w': 600,
          'cap': _('To enable more icon sets, install "toolbarxicons" add-ons'),
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'label')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'label_lexers',
          'x': 10,
          'y': 240,
          'w': 140,
          'cap': _('Visible for lexers:\n(comma-separated)'),
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'edit')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'edit_lexers',
          'x': 150,
          'y': 246,
          'w': 440,
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_ok',
          'x': 380,
          'y': 290,
          'w': 100,
          'cap': _('OK'),
          'ex0': True,
          'on_change': self.call_ok,
          } )

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_cancel',
          'x': 490,
          'y': 290,
          'w': 100,
          'cap': _('Cancel'),
          'on_change': self.call_cancel,
          } )

        self.h_dlg = h
