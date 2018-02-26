import os
import json
import cudatext as app

options = {
    'icon_set': '',
    'sub': [],
    }

fn_config = os.path.join(app.app_path(app.APP_DIR_SETTINGS), 'cuda_config_toolbar.json')
dir_icons = ''
dir_settings = app.app_path(app.APP_DIR_SETTINGS)
macro_settings = '{op}'
hide = '' # space-separated indexes of toolbar buttons to hide


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
    global hide

    with open(fn_config, 'r', encoding='utf8') as f:
        options = json.load(f)
        dir_icons = decode_fn(options.get('dir_icons', ''))
        hide = options.get('hide', '')


def do_save_ops():
    global fn_config
    global options
    global dir_icons

    options['dir_icons'] = encode_fn(dir_icons)
    options['hide'] = hide

    with open(fn_config, 'w', encoding='utf8') as f:
        f.write(json.dumps(options, indent=2))
