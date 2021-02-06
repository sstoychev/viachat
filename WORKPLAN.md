# Target

1. Command resolution
    - ~~which Command was passed, default Command~~ - Done
    - ~~Command parameters verification~~ - Done

1. User connect
    - ~~before executing any commands the user should set username~~ - Done

1.  Create/Join rooms
    - ~~create room - check if the name is available~~ - Done
    - ~~join room - the user can be in more rooms~~ - Done
    - leave room
    - broadcast when another user joins the room
    - get list with active users in the room
    - nice-to-have - broadcast when user quits to all the rooms he was in

1. Post to room
    - by default to the current room
    - if used command /post _room_ - send to the specified room

1. Store information in database
    - ~~adapter classes for the different DBs - the should have the same set of default methods so they can be changed without changing anything in the code~~ - Done
    - store rooms messages in the database

1. Start server parameters handling
    - ~~argparse~~ - Done
    - ~~config file~~ - Done

# Optional

1. Executables

2. Web client
