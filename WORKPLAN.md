<style>
r { color: Red }
o { color: Orange }
g { color: Green }
</style>

# Target

1. Command resolution
    - ~~which Command was passed, default Command~~ - <g>Done</g>
    - ~~Command parameters verification~~ - <g>Done</g>

1. User connect
    - ~~before executing any commands the user should set username~~ - <g>Done</g>

1.  Create/Join rooms
    - ~~create room - check if the name is available~~ - <g>Done</g>
    - ~~join room - the user can be in more rooms~~ - <g>Done</g>
    - ~~leave room~~ - <g>Done</g>
    - ~~broadcast when another user joins the room~~ - <g>Done</g>
    - ~~get list with active users in the room~~ - <g>Done</g>
    - ~~nice-to-have - broadcast when user quits to all the rooms he was in~~ <g>Done</g>

1. Post to room
    - ~~by default to the current room~~ - <g>Done</g>
    - if used command /post _room_ - send to the specified room - <span style="color:red">Not done, the user should switch with /room </span>.

1. Store information in database
    - ~~adapter classes for the different DBs - the should have the same set of default methods so they can be changed without changing anything in the code~~ - <g>Done</g>
    - ~~store rooms messages in the database~~ - <g>Done</g>

1. Start server parameters handling
    - argparse
    - ~~config file~~ - <g>Done</g>

# Optional

1. Executables

2. Web client
