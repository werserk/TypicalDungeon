with open('data/texts/hello.txt') as f:
    HELLO_TEXT = f.read().split('\n')

with open('data/texts/howtoplay.txt') as f:
    INFO_TEXT = f.read().split('\n')

with open('data/info.txt') as f:
    _text = f.read().split('\n')
    FIRST_TIME = bool(int(_text[0].split(':')[1]))


def get_money():
    with open('data/info.txt') as f:
        text = f.read().split('\n')
        money = int(text[1].split(':')[1])
    return money
