def parse_login(input):
    login = not input[-3:] == "out"
    username, playfabid = input[28:][:-29], input[-27:][:-11]
    playfabid = playfabid.replace("(", "").strip()
    return(playfabid, login)

