import os

def get_from_environment(name, cast = str):
    value = os.environ.get(name)

    if value is not None:
        if cast == 'array':
            return value.split(',')
        else:
            return cast(value)

