TOKEN = ''
TOKEN_WEATHER = ''

with open('.env', 'r') as tokens:
    TOKENS = tokens.readlines()
    TOKEN = TOKENS[0].rsplit()
    TOKEN_WEATHER = TOKENS[1]

