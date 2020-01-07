Plugin for CudaText.
Allows to configure main toolbar (on the top):
- hide some standard buttons (specify 0-based button indexes, e.g. "0 2 8 9")
- add additional buttons.

For additional buttons you can customize: 
- caption 
- tooltip 
- icon file (size can be any, can mismatch current icon set) 
- command: usual CudaText commands + plugin commands, you can choose both in menu (like CudaText Commands dialog).

Notes:
- buttons can have caption, or icon, or caption+icon.
- dialog field "Visible for lexers" needs comma-separated lexer names, in any case. None-lexer must be specified as "-" char. Empty field: button is always visible.
- buttons cannot be changed during configuring time, they will be changed after CudaText restart.

Author: Alexey Torgashin (CudaText)
License: MIT
