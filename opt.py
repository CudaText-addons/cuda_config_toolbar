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

        hide_new = options.get('hide_new', False)
        hide_open = options.get('hide_open', False)
        hide_save = options.get('hide_save', False)
        hide_cut = options.get('hide_cut', False)
        hide_copy = options.get('hide_copy', False)
        hide_paste = options.get('hide_paste', False)
        hide_undo = options.get('hide_undo', False)
        hide_redo = options.get('hide_redo', False)
        hide_unpri = options.get('hide_unpri', False)
        hide_minimap = options.get('hide_minimap', False)
        hide_indent = options.get('hide_indent', False)
        hide_unindent = options.get('hide_unindent', False)


def do_save_ops():
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

    options['dir_icons'] = encode_fn(dir_icons)
    options['hide_new'] = hide_new
    options['hide_open'] = hide_open
    options['hide_save'] = hide_save
    options['hide_cut'] = hide_cut
    options['hide_copy'] = hide_copy
    options['hide_paste'] = hide_paste
    options['hide_undo'] = hide_undo
    options['hide_redo'] = hide_redo
    options['hide_unpri'] = hide_unpri
    options['hide_minimap'] = hide_minimap
    options['hide_indent'] = hide_indent
    options['hide_unindent'] = hide_unindent

    with open(fn_config, 'w', encoding='utf8') as f:
        f.write(json.dumps(options, indent=2))
