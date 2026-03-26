# CommentWall

A plugin for Sublime Text to insert walls of comments at specific columns in a file.

## Add to Sublime Text

### tty

```
cp comment_wall.py ~/.config/sublime-text/Packages/User/.
```

### Sublime Keybinds

```
{ "keys": ["ctrl+k", "ctrl+w"], "command": "comment_wall", "args":  {"col": 40} },
{ "keys": ["ctrl+k", "ctrl+enter"], "command": "comment_wall_insert", "args":  {"characters": "\n", "col": 40} },
```