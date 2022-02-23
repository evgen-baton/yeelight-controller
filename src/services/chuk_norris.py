from requests import get
from json import loads


def get_random_joke() -> str:
    """
    :return: random joke about Chuck Norris
    """
    result = get('https://api.chucknorris.io/jokes/random')
    json_string = loads(result.text)

    return json_string['value']
