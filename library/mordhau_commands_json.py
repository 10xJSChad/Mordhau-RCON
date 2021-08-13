import json

class mordhau_commands():
    socket = None
    
    def __init__(self):
        1+1

    def run(self, command:dict):
        command = json.dumps(command)
        if self.socket != None: return(self.socket.run(command))
        else: return command

    def help(self):
        command = { 
                "command":"help", 
                "type":"execute", 
            }
        return(self.run(command))

    def command_info(self, command:str):
        command = { 
                "command": command, 
                "type":"request info", 
            }
        return(self.run(command))

    def say(self, message:str):
        command = { 
                "command":"say", 
                "type":"execute", 
                "Data": {
                    "prefix":"ServerSay", 
                    "body": message
                    },
            }
        return(self.run(command))

    def kill(self, playfabID:str):
        command = { 
                "command":"kill", 
                "type":"execute", 
                "Data": {
                    "playfabid": playfabID
                    },
            }
        return(self.run(command))

    def teleport(self, playfabID:str, location:tuple):
        command = { 
                "command":"teleport", 
                "type":"execute", 
                "Data": {
                    "playfabid": playfabID,
                    "location": [location[0], location[1], location[2]],
                    },
            }
        return(self.run(command))
    
    def change_level(self, map:str):
        command = { 
                "command":"change level", 
                "type":"execute", 
                "Data": {
                    "map name": map,
                    },
            }
        return(self.run(command))