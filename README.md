# i3-improvements
Personal `i3` control wrapper library. Improvements to i3's workspace switching and renaming


## `workspace.py`
This script corrects issues with renaming workspaces. Stock `i3` has a few bugs with space renaming:
  - Renamed spaces are moved to the end of the list
  - Renamed workspaces cannot be accessed with `$mod+num`
  - There is no way (that I can find) to control the way the workspaces are arranged
  
A common workaround is to rename them with numbers, i.e. `1-www`, `2-vim`, etc. This allows for accessing with `$mod+num` but does not solve the other two issues. This script handles the above by using iterated `rename` commands to maintain the correct order of workspaces with renaming.

This script is meant to replace using `$mod+num` to create workspaces. Map a key to `--new` to create a new workspace with a randomized name from `vegetables.txt`.

### Usage
`workspace.py --rename` - Open an i3-input prompt to rename the workspace
`workspace.py --move {left,right}` - Move workspace
`workspace.py --move_container {left,right}` - Move container
`workspace.py --new` - Create a new container with a randomized name
`workspace.py --goto {index}` - Go to the *n*th workspace

## Todo
 - Test `workspace.py` with first boot
