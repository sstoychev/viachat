1. Command resolution
    - which Command was passed, default Command
    - Command parameters verification

1. User connect
    - before executing any commands the user should set username

1.  Create/Join rooms
    - create room - check if the name is available
    - join room - the user can be in more rooms
    - leave room
    - broadcast when another user joins the room
    - get list with active users in the room
    - nice-to-have - broadcast when user leaves the room because of disconnect

1. Post to room
    - by default to the current room
    - if used command /post _room_ - send to the specified room

1. Store information in database
    - adapter classes for the different DBs - the should have the same set of default methods so they can be changed without changing anything in the code
    - store rooms messages in the database

1. Start server parameters handling
    - argparse
    - config file
