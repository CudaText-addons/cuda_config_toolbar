from cudatext import *


def dialog_buttons(buttons, clear):

    c1 = chr(1)
    RES_LIST = 1
    RES_MOVE_UP = 2
    RES_MOVE_DOWN =  3
    RES_CAP = 5
    RES_HINT = 7
    RES_CMD_B = 8
    RES_SUBMENU_B = 9
    RES_CMD_VAL = 10
    RES_ICON_B = 11
    RES_ICON_VAL = 12
    RES_B_ADD = 13
    RES_B_ADDSEP = 14
    RES_B_CHANGE = 15
    RES_B_DELETE = 16
    RES_OK = 17
    RES_CANCEL = 18
    RES_DEL_DEF = 19

    val_index = -1
    val_cap = ''
    val_hint = ''
    val_cmd = ''
    val_icon = ''

    while True:
        items = [item['cap'] if not item['cmd'].startswith('toolmenu:') else '(sub-menu)' for item in buttons]
        items = ['---' if s=='-' else '(no text)' if s=='' else s for s in items]
        items = '\t'.join(items)

        b_sel = '1' if val_index>=0 else '0'
        b_en_up = '1' if val_index>0 else '0'
        b_en_down = '1' if (val_index>=0 and val_index<len(buttons)-1) else '0'
        b_clear = '1' if clear else '0'

        text = '\n'.join([''
            , c1.join(['type=label', 'pos=6,6,194,0', 'cap=Buttons:'])
            , c1.join(['type=listbox', 'pos=6,30,194,350', 'items='+items, 'val='+str(val_index), 'act=1'])

            , c1.join(['type=button', 'pos=6,356,94,0', 'cap=Move &up', 'en='+b_en_up])
            , c1.join(['type=button', 'pos=100,356,194,0', 'cap=Move &down', 'en='+b_en_down])

            , c1.join(['type=label', 'pos=200,34,600,0', 'cap=&Caption:'])
            , c1.join(['type=edit', 'pos=306,30,600,0', 'val='+val_cap])
            , c1.join(['type=label', 'pos=200,70,600,0', 'cap=&Tooltip:'])
            , c1.join(['type=edit', 'pos=306,65,600,0', 'val='+val_hint])
            , c1.join(['type=button', 'pos=200,100,300,0', 'cap=C&ommand...'])
            , c1.join(['type=button', 'pos=200,130,300,0', 'cap=Sub-&menu'])
            , c1.join(['type=edit', 'pos=306,100,600,0', 'cap='+val_cmd])
            , c1.join(['type=button', 'pos=200,165,300,0', 'cap=&Icon file...'])
            , c1.join(['type=edit', 'pos=306,165,600,0', 'cap='+val_icon])

            , c1.join(['type=button', 'pos=400,210,600,0', 'cap=Add &button'])
            , c1.join(['type=button', 'pos=400,240,600,0', 'cap=Add &separator'])
            , c1.join(['type=button', 'pos=400,270,600,0', 'cap=Chan&ge selected button', 'en='+b_sel])
            , c1.join(['type=button', 'pos=400,300,600,0', 'cap=&Delete selected button', 'en='+b_sel])

            , c1.join(['type=button', 'pos=394,356,494,0', 'cap=OK', 'props=1'])
            , c1.join(['type=button', 'pos=500,356,600,0', 'cap=Cancel'])

            , c1.join(['type=check', 'pos=400,330,600,0', 'cap=Remo&ve std buttons', 'val='+b_clear])
            ])

        res = dlg_custom('Toolbar buttons', 606, 388, text, focused=RES_CAP)
        if not res: return

        res, text = res
        text = text.splitlines()

        val_cap = text[RES_CAP]
        val_hint = text[RES_HINT]
        val_cmd = text[RES_CMD_VAL]
        val_icon = text[RES_ICON_VAL]
        val_del_def = text[RES_DEL_DEF]=='1'

        if res==RES_CANCEL: return
        if res==RES_OK: return (buttons, val_del_def)

        if res==RES_B_ADD:
            if not val_cap and not val_icon:
                msg_box('Button needs caption, or icon, or caption+icon', MB_OK+MB_ICONWARNING)
                continue
            d = {'cap': val_cap, 'hint': val_hint, 'cmd': val_cmd, 'icon': val_icon}
            buttons.append(d)

        if res==RES_B_ADDSEP:
            d = {'cap': '-', 'hint': '', 'cmd': '', 'icon': ''}
            buttons.append(d)

        if res==RES_B_CHANGE:
            d = {'cap': val_cap, 'hint': val_hint, 'cmd': val_cmd, 'icon': val_icon}
            buttons[val_index] = d

        if res==RES_B_DELETE:
            if val_index>=0:
                del buttons[val_index]
                if val_index >= len(buttons):
                    val_index -= 1

        if res==RES_LIST:
            val_index = int(text[RES_LIST])
            if val_index>=0:
                val_cap = buttons[val_index]['cap']
                val_hint = buttons[val_index]['hint']
                val_cmd = buttons[val_index]['cmd']
                val_icon = buttons[val_index]['icon']

        if res==RES_CMD_B:
            s = dlg_commands(COMMANDS_USUAL+COMMANDS_PLUGINS)
            if s:
                val_cmd = s[2:]

        if res==RES_SUBMENU_B:
            val_cmd = 'toolmenu:id'+str(val_index+1)

        if res==RES_ICON_B:
            s = dlg_file(True, '', '', 'PNG files|*.png')
            if s:
                val_icon = s

        if res==RES_MOVE_UP:
            buttons.insert(val_index-1, buttons.pop(val_index))
            val_index -= 1

        if res==RES_MOVE_DOWN:
            buttons.insert(val_index+1, buttons.pop(val_index))
            val_index += 1

