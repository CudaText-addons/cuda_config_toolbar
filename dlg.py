from cudatext import *


def dialog_buttons(buttons):

    c1 = chr(1)
    RES_LIST = 1
    RES_UP = 2
    RES_DOWN =  3
    RES_CAP = 6
    RES_HINT = 8
    RES_CMD_B = 9
    RES_CMD_VAL = 10
    RES_ICON_B = 11
    RES_ICON_VAL = 12
    RES_B_ADD = 13
    RES_B_CHG = 14
    RES_B_SEP = 15
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
            , c1.join(['type=listbox', 'pos=6,30,194,300', 'items='+items, 'val='+str(val_index), 'act=1'])

            , c1.join(['type=button', 'pos=6,306,94,0', 'cap=Up', 'en='+b_sel])
            , c1.join(['type=button', 'pos=100,306,194,0', 'cap=Down', 'en='+b_sel])
            , c1.join(['type=button', 'pos=6,336,94,0', 'cap=Delete', 'en='+b_sel])

            , c1.join(['type=label', 'pos=200,34,600,0', 'cap=Caption:'])
            , c1.join(['type=edit', 'pos=306,30,600,0', 'val='+val_cap])
            , c1.join(['type=label', 'pos=200,70,600,0', 'cap=Tooltip:'])
            , c1.join(['type=edit', 'pos=306,65,600,0', 'val='+val_hint])
            , c1.join(['type=button', 'pos=200,100,300,0', 'cap=Command...'])
            , c1.join(['type=edit', 'pos=306,100,600,0', 'cap='+val_cmd])
            , c1.join(['type=button', 'pos=200,135,300,0', 'cap=Icon file...'])
            , c1.join(['type=edit', 'pos=306,135,600,0', 'cap='+val_icon])

            , c1.join(['type=button', 'pos=400,180,600,0', 'cap=Add this button'])
            , c1.join(['type=button', 'pos=400,210,600,0', 'cap=Change selected button', 'en='+b_sel])
            , c1.join(['type=button', 'pos=400,240,600,0', 'cap=Add separator'])

            , c1.join(['type=button', 'pos=394,336,494,0', 'cap=OK'])
            , c1.join(['type=button', 'pos=500,336,600,0', 'cap=Cancel'])
            ])

        res = dlg_custom('Toolbar buttons', 606, 368, text, focused=RES_CAP)
        if not res: return

        res, text = res
        text = text.splitlines()
        if res==RES_CANCEL: return
        if res==RES_OK: return buttons

        if res==RES_B_ADD:
            d = {
                'cap': text[RES_CAP],
                'hint': text[RES_HINT],
                'cmd': text[RES_CMD_VAL],
                'icon': text[RES_ICON_VAL]
                }
            buttons.append(d)

        if res==RES_B_SEP:
            d = {
                'cap': '-',
                'hint': '',
                'cmd': '',
                'icon': ''
                }
            buttons.append(d)

        if res==RES_LIST:
            val_index = int(text[RES_LIST])
            if val_index>=0:
                val_cap = buttons[val_index]['cap']
                val_hint = buttons[val_index]['hint']
                val_cmd = buttons[val_index]['cmd']
                val_icon = buttons[val_index]['icon']


