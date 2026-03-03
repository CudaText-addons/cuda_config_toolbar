Plugin for CudaText.
Allows to configure the main toolbar (horizontally aligned on the top of GUI):
- hide standard buttons,
- add/remove/customize additional buttons and/or submenus.

For additional buttons you can customize:

- caption,
- tooltip,
- icon file (its sizes can be any, can mismatch sizes of the current icon set),
- command: usual CudaText commands + plugin commands, you can choose both from menu (like CudaText Commands dialog).

Notes:
- buttons can have caption, or icon, or caption+icon.
- dialog field "Visible for lexers" needs comma-separated lexer names, in any case. None-lexer must be specified as "-" char. Empty field: button is always visible.
- buttons cannot be changed during configuring time, they will be changed after CudaText restart.


Author: Alexey Torgashin (CudaText)
License: MIT
