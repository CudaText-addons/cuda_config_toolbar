import os
from cudatext import *

CHOOSE_FORM_W = 300
CHOOSE_FORM_H = 580
CHOOSE_COLOR_LIST = 0xFFFFFF
CHOOSE_COLOR_SEL = 0xE0A0A0

DIR_XICONS = os.path.join(app_path(APP_DIR_DATA), 'toolbarxicons')


def get_icon_size(filename):

    s = os.path.basename(filename)
    try:
        s = s.split('_')[-1].split('x')[0]
        return int(s)
    except:
        return 32


def get_dirs_in(basedir):

    if not os.path.isdir(basedir):
        return []
    d = os.listdir(basedir)
    d = [os.path.join(basedir, f) for f in d]
    d = [f for f in d if os.path.isdir(f)]
    return sorted(d)



class DialogChooseIcon:

    def __init__(self):

        self.img = image_proc(0, IMAGE_CREATE, value=0)
        self.h_dlg = self.init_dlg()


    def get_iconset(self, basedir):

        d1 = get_dirs_in(basedir)
        d2 = get_dirs_in(DIR_XICONS)
        dirs = d1+d2

        d1_nice = [os.path.basename(f) for f in d1]
        d2_nice = [os.path.basename(f)+' (additional)' for f in d2]
        d_nice = d1_nice+d2_nice

        res = dlg_menu(MENU_LIST, d_nice, caption='Choose icon set')
        if res is not None:
            return dirs[res]


    def get_files(self, basedir):

        ff = sorted(os.listdir(basedir))
        ff = [os.path.join(basedir, f) for f in ff if f.endswith('.png')]
        #print('files:', ff)
        return ff


    def update_filter(self):
        dlg_proc(self.h_dlg, DLG_CTL_PROP_SET, name='filter', prop={'cap': 'Filter: '+self.filter})

        listbox_proc(self.h_list, LISTBOX_DELETE_ALL)

        items = [os.path.basename(f)[:-4] for f in self.files]
        for (i, item) in enumerate(items):
            if not self.filter or self.filter in item:
                listbox_proc(self.h_list, LISTBOX_ADD, index=-1, text=item)

        listbox_proc(self.h_list, LISTBOX_SET_TOP, index=0)
        listbox_proc(self.h_list, LISTBOX_SET_SEL, index=0)


    def callback_keydown(self, id_dlg, id_ctl, data='', info=''):

        #react to text
        if (ord('A') <= id_ctl <= ord('Z')) or \
           (ord('0') <= id_ctl <= ord('9')):
            self.filter += chr(id_ctl).lower()
            self.update_filter()

        #react to BackSp
        if id_ctl==8:
            if self.filter:
                self.filter = self.filter[:-1]
                self.update_filter()

        #react to Enter
        if id_ctl==13:
            index_sel = listbox_proc(self.h_list, LISTBOX_GET_SEL)
            item = listbox_proc(self.h_list, LISTBOX_GET_ITEM, index=index_sel)
            if not item: return
            item_text = item[0]

            self.result = os.path.join(self.filedir, item_text+'.png')
            dlg_proc(self.h_dlg, DLG_HIDE)


    def callback_listbox_drawitem(self, id_dlg, id_ctl, data='', info=''):

        id_canvas = data['canvas']
        index = data['index']
        rect = data['rect']
        index_sel = listbox_proc(self.h_list, LISTBOX_GET_SEL)
        item_text = listbox_proc(self.h_list, LISTBOX_GET_ITEM, index=index)[0]

        if index==index_sel:
            back_color = CHOOSE_COLOR_SEL
        else:
            back_color = CHOOSE_COLOR_LIST

        canvas_proc(id_canvas, CANVAS_SET_BRUSH, color=back_color, style=BRUSH_SOLID)
        canvas_proc(id_canvas, CANVAS_RECT_FILL, x=rect[0], y=rect[1], x2=rect[2], y2=rect[3])

        size = canvas_proc(id_canvas, CANVAS_GET_TEXT_SIZE, text=item_text)
        canvas_proc(id_canvas, CANVAS_TEXT,
            text = item_text,
            x = rect[0] + self.icon_size + 6,
            y = (rect[1]+rect[3]-size[1])//2 )

        image_proc(self.img, IMAGE_LOAD, value=os.path.join(self.filedir, item_text+'.png'))
        image_proc(self.img, IMAGE_PAINT_SIZED, value=(id_canvas, rect[0], rect[1], rect[0]+self.icon_size, rect[1]+self.icon_size))


    def init_dlg(self):

        h=dlg_proc(0, DLG_CREATE)
        dlg_proc(h, DLG_PROP_SET, prop={'cap':'Choose icon',
          'w':CHOOSE_FORM_W,
          'h':CHOOSE_FORM_H,
          'on_key_down': self.callback_keydown,
          'keypreview': True
          })

        n=dlg_proc(h, DLG_CTL_ADD, 'label')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'filter',
            'align': ALIGN_TOP,
            'sp_a': 6,
            'cap': '',
            })

        n=dlg_proc(h, DLG_CTL_ADD, 'listbox_ex')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'list1',
            'align': ALIGN_CLIENT,
            'sp_a': 6,
            'on_draw_item': self.callback_listbox_drawitem,
            })

        self.h_list = dlg_proc(h, DLG_CTL_HANDLE, index=n)
        dlg_proc(h, DLG_CTL_FOCUS, index=n)

        listbox_proc(self.h_list, LISTBOX_SET_DRAWN, index=1)

        return h


    def choose_icon(self, basedir):

        self.result = ''
        self.filter = ''
        self.files = []
        self.filedir = self.get_iconset(basedir)
        if not self.filedir: return

        self.icon_size = get_icon_size(self.filedir)

        listbox_proc(self.h_list, LISTBOX_SET_ITEM_H, index=max(18, self.icon_size))

        self.files = self.get_files(self.filedir)
        if not self.files: return

        self.update_filter()

        dlg_proc(self.h_dlg, DLG_SHOW_MODAL)
        if self.result:
            return self.result, self.icon_size
