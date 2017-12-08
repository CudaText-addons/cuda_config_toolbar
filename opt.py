import os
import json
import cudatext as app

options = {
    'icon_set': '',
    'sub': [],
    'clear': False,
    }

fn_config = os.path.join(app.app_path(app.APP_DIR_SETTINGS), 'cuda_config_toolbar.json')
dir_icon_sets = os.path.join(os.path.dirname(__file__), 'icons')
dir_icons = ''
dir_settings = app.app_path(app.APP_DIR_SETTINGS)
macro_settings = '{op}'


def _encode_fn(fn):
    s = fn
    if s.startswith(dir_settings):
        s = macro_settings+s[len(dir_settings):]
    return s

def _decode_fn(fn):
    s = fn
    if s.startswith(macro_settings):
        s = dir_settings + s[len(macro_settings):]
    return s


def do_load_ops():
    global fn_config
    global options
    global dir_icons

    with open(fn_config, 'r', encoding='utf8') as f:
        options = json.load(f)
        dir_icons = _decode_fn(options.get('dir_icons', ''))


def do_save_ops():
    global fn_config
    global options
    global dir_icons

    options['dir_icons'] = _encode_fn(dir_icons)
    with open(fn_config, 'w', encoding='utf8') as f:
        f.write(json.dumps(options, indent=2))
