from cudatext import *


def dialog_buttons(buttons):

    c1 = chr(1)
    RES_LIST = 1
    RES_UP = 2
    RES_DOWN =  3
    RES_CAP = 5
    RES_HINT = 7
    RES_CMD_B = 8
    RES_CMD_VAL = 9
    RES_ICON_B = 10
    RES_ICON_VAL = 11
    RES_B_ADD = 12
    RES_B_ADDSEP = 13
    RES_B_CHANGE = 14
    RES_B_DELETE = 15
    RES_OK = 16
    RES_CANCEL = 17

    val_index = -1
    val_cap = '?'
    val_hint = ''
    val_cmd = ''
    val_icon = ''

    while True:
        items = '\t'.join([item['cap'] for item in buttons])
        b_sel = '1' if val_index>=0 else '0'

        text = '\n'.join([''
            , c1.join(['type=label', 'pos=6,6,194,0', 'cap=Additional buttons:'])
            , c1.join(['type=listbox', 'pos=6,30,194,330', 'items='+items, 'val='+str(val_index), 'act=1'])

            , c1.join(['type=button', 'pos=6,336,94,0', 'cap=Up', 'en='+b_sel])
            , c1.join(['type=button', 'pos=100,336,194,0', 'cap=Down', 'en='+b_sel])

            , c1.join(['type=label', 'pos=200,34,600,0', 'cap=Caption:'])
            , c1.join(['type=edit', 'pos=306,30,600,0', 'val='+val_cap])
            , c1.join(['type=label', 'pos=200,70,600,0', 'cap=Tooltip:'])
            , c1.join(['type=edit', 'pos=306,65,600,0', 'val='+val_hint])
            , c1.join(['type=button', 'pos=200,100,300,0', 'cap=Command...'])
            , c1.join(['type=edit', 'pos=306,100,600,0', 'cap='+val_cmd])
            , c1.join(['type=button', 'pos=200,135,300,0', 'cap=Icon file...'])
            , c1.join(['type=edit', 'pos=306,135,600,0', 'cap='+val_icon])

            , c1.join(['type=button', 'pos=400,180,600,0', 'cap=Add new button'])
            , c1.join(['type=button', 'pos=400,210,600,0', 'cap=Add separator'])
            , c1.join(['type=button', 'pos=400,240,600,0', 'cap=Change selected button', 'en='+b_sel])
            , c1.join(['type=button', 'pos=400,270,600,0', 'cap=Delete selected button', 'en='+b_sel])

            , c1.join(['type=button', 'pos=394,336,494,0', 'cap=OK'])
            , c1.join(['type=button', 'pos=500,336,600,0', 'cap=Cancel'])
            ])

        res = dlg_custom('Toolbar buttons', 606, 368, text, focused=RES_CAP)
        if not res: return

        res, text = res
        text = text.splitlines()
        if res==RES_CANCEL: return
        if res==RES_OK: return buttons

        val_cap = text[RES_CAP]
        val_hint = text[RES_HINT]
        val_cmd = text[RES_CMD_VAL]
        val_icon = text[RES_ICON_VAL]

        if res==RES_B_ADD:
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

        if res==RES_ICON_B:
            s = dlg_file(True, '', '', 'PNG files|*.png')
            if s:
                val_icon = s
