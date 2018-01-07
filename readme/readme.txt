Plugin for CudaText.
Allows to config main toolbar (on the top):

1) Choose icon set, for standard buttons. 
Many icon sets are shipped with plugin.

2) Config additional buttons (to standard buttons).
For additional buttons you can customize: 
- caption 
- tooltip 
- icon file (size can be any, can mismatch current icon set) 
- command: usual CudaText commands + plugin commands, you can choose both in menu (like CudaText Commands dialog).

Notes:
- buttons can have caption, or icon, or caption+icon.
- dialog field "Visible for lexers" needs comma-separated lexer names, in any case. None-lexer must be specified as "-" char. Empty field: button is always visible.
- buttons cannot be changed during configuring time, they will be changed after CudaText restart.


Author: Alexey T.
License: MIT
