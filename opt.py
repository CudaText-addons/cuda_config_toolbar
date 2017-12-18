import os
import json
import cudatext as app

options = {
    'icon_set': '',
    'sub': [],
    }

fn_config = os.path.join(app.app_path(app.APP_DIR_SETTINGS), 'cuda_config_toolbar.json')
dir_icon_sets = os.path.join(os.path.dirname(__file__), 'icons')
dir_icons = ''
dir_settings = app.app_path(app.APP_DIR_SETTINGS)
macro_settings = '{op}'

hide_new = False
hide_open = False
hide_save = False
hide_cut = False
hide_copy = False
hide_paste = False
hide_undo = False
hide_redo = False
hide_unpri = False
hide_minimap = False
hide_indent = False
hide_unindent = False


def encode_fn(fn):
    s = fn
    if s.startswith(dir_settings):
        s = macro_settings+s[len(dir_settings):]
    return s

def decode_fn(fn):
    s = fn
    if s.startswith(macro_settings):
        s = dir_settings + s[len(macro_settings):]
    return s


def do_load_ops():
    global fn_config
    global options
    global dir_icons
    global hide_new
    global hide_open
    global hide_save
    global hide_cut
    global hide_copy
    global hide_paste
    global hide_undo
    global hide_redo
    global hide_unpri
    global hide_minimap
    global hide_indent
    global hide_unindent

    with open(fn_config, 'r', encoding='utf8') as f:
        options = json.load(f)
        dir_icons = decode_fn(options.get('dir_icons', ''))

        hide = options.get('hide', [])
        hide_new = 'f_new' in hide
        hide_open = 'f_open' in hide
        hide_save = 'f_save' in hide
        hide_cut = 'e_cut' in hide
        hide_copy = 'e_copy' in hide
        hide_paste = 'e_paste' in hide
        hide_undo = 'e_undo' in hide
        hide_redo = 'e_redo' in hide
        hide_unpri = 'unpri' in hide
        hide_minimap = 'map' in hide
        hide_indent = 'indent' in hide
        hide_unindent = 'unindent' in hide


def do_save_ops():
    global fn_config
    global options
    global dir_icons

    options['dir_icons'] = encode_fn(dir_icons)

    hide = []
    if hide_new: hide+=['f_new']
    if hide_open: hide+=['f_open']
    if hide_save: hide+=['f_save']
    if hide_cut: hide+=['e_cut']
    if hide_copy: hide+=['e_copy']
    if hide_paste: hide+=['e_paste']
    if hide_undo: hide+=['e_undo']
    if hide_redo: hide+=['e_redo']
    if hide_unpri: hide+=['unpri']
    if hide_minimap: hide+=['map']
    if hide_indent: hide+=['indent']
    if hide_unindent: hide+=['unindent']
    options['hide'] = hide

    with open(fn_config, 'w', encoding='utf8') as f:
        f.write(json.dumps(options, indent=2))
