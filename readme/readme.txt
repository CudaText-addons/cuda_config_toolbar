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

Note: buttons can have caption, or icon, or caption+icon.
Note: buttons cannot be added during configuring session, they will be added after CudaText restart.
Note: dialog field "Visible for lexers" needs comma-separated lexer names, in any case. None-lexer must be specified as "-" char. Empty field: buttons is always visible.


Author: Alexey T.
License: MIT
