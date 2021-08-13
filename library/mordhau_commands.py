class mordhau_commands():
    socket = None
    
    def __init__(self):
        None

    def run(self, command:str):
        print(command)
        if self.socket != None: return(self.socket.run(command))
        else: return command
    
    def say(self, message:str):
        return(self.run("say " + message))