from random import choice, randint


def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'Well, you\'re using silent treatment!!!'
    elif 'hello' in lowered:
        return 'Hello there!'
    elif 'how are you' in lowered:
        return 'I\'m good, thanks!'
    elif 'bye' in lowered:
        return 'Have a nice day!!!'
    else:
        return choice(['I don\'t understand...',
                       'Can you explain more details ?',
                       'Make it more simple to understand, pls!!!'])