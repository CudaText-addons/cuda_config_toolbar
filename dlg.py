from cudatext import *


def dialog_buttons(buttons):

    c1 = chr(1)
    RES_UP = 2
    RES_DOWN =  3
    RES_CAP = 6
    RES_HINT = 8
    RES_CMD = 9
    RES_CMD_VAL = 10
    RES_ICON = 11
    RES_ICON_VAL = 12
    RES_ADD = 13
    RES_OK = 14
    RES_CANCEL = 15

    val_cap = 'cap?'
    val_hint = 'hint?'
    val_cmd = 'cmd?'
    val_icon = 'icon?'

    while True:
        items = '\t'.join([item['cap'] for item in buttons])

        text = '\n'.join([''
            , c1.join(['type=label', 'pos=6,6,194,0', 'cap=Additional buttons:'])
            , c1.join(['type=listbox', 'pos=6,30,194,300', 'items='+items])

            , c1.join(['type=button', 'pos=6,306,94,0', 'cap=Up'])
            , c1.join(['type=button', 'pos=100,306,194,0', 'cap=Down'])
            , c1.join(['type=button', 'pos=6,336,94,0', 'cap=Delete'])

            , c1.join(['type=label', 'pos=200,34,600,0', 'cap=Caption:'])
            , c1.join(['type=edit', 'pos=306,30,600,0', 'val='+val_cap])
            , c1.join(['type=label', 'pos=200,70,600,0', 'cap=Tooltip:'])
            , c1.join(['type=edit', 'pos=306,65,600,0', 'val='+val_hint])
            , c1.join(['type=button', 'pos=200,100,300,0', 'cap=Command...'])
            , c1.join(['type=edit', 'pos=306,100,600,0', 'cap='+val_cmd])
            , c1.join(['type=button', 'pos=200,135,300,0', 'cap=Icon file...'])
            , c1.join(['type=edit', 'pos=306,135,600,0', 'cap='+val_icon])
            , c1.join(['type=button', 'pos=400,180,600,0', 'cap=Add this button'])

            , c1.join(['type=button', 'pos=394,336,494,0', 'cap=OK'])
            , c1.join(['type=button', 'pos=500,336,600,0', 'cap=Cancel'])
            ])

        res = dlg_custom('Toolbar buttons', 606, 368, text, focused=-1)
        if not res: return

        res, text = res
        text = text.splitlines()
        if res==RES_CANCEL: return
        if res==RES_OK: return buttons

        if res==RES_ADD:
            d = {
                'cap': text[RES_CAP],
                'hint': text[RES_HINT],
                'cmd': text[RES_CMD_VAL],
                'icon': text[RES_ICON_VAL]
                }
            buttons.append(d)
