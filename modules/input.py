def get_input(prompt: str) -> list:
    data = input(prompt + ' ')
    data = data.lower()
    return data.split(' ')