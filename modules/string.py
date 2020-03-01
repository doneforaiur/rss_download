def str_to_filename(name: str, placeholder: str='') -> str:
    invalid_characters = [
        '\\',
        '/',
        ':',
        '*',
        '?',
        '"',
        '<',
        '>',
        '|',
    ]

    for character in invalid_characters:
        name = name.replace(character, placeholder)

    return name
