## PyMacro
This program is portable macro editor. Used libraries:
- pyautogui -> for handling mouse, keyboard and pixel color in cursor position
- pyperclip -> for handling clipboard
- pyautogui/PIL -> for image matching (search for image in requested area)

## Features to add
- ~~saving macro to some kind of file (**json**, xml, ...?)~~
- ~~loading file~~
- ~~logic and loops (if statement, conditional jumps) -> some kind of AST~~
- running macro in debug and in 'production'
- kill macro key combination -> similiar to interrupts in microcontrollers
- get cursor position (probably save it in program memory)
- idiotproof creating (dropdown menus, type hinting)
- ~~checking image pattern~~ more or less done
- ~~checking string values -> regex, normal matching~~
- ~~3 variable files:, coords: label;x;y;,  colors: label;RGB;, user_varibles: label;value~~ -> ~~one will be enough, but with possibility of dumping variables to file~~
- custom python script execution
- misc functions(nothing, save variables, load variables...)

## GUI
looks like FWK, left(table with tasks), right(task edition), task operations(move, delete, add new, copy, copy from another macro). get cursor position, variables subwindow, new/open/save macro, run program/kill (as button and shortcut), settings(), mark jumps(?) 
