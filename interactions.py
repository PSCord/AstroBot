import requests

GUILD_ID = 860585050838663188

APPLICATION_ID = 848926333256859670
APPLICATION_TOKEN = 'Bot ODQ4OTI2MzMzMjU2ODU5Njcw.YLTuQg.A6YpaJmZtj1-d1GWGm9snTYTjFk'

URL = f'https://discord.com/api/v8/applications/{APPLICATION_ID}/guilds/{GUILD_ID}/commands'


def create_command(data):
    response = requests.post(URL, json=data, headers={'authorization': APPLICATION_TOKEN})

    if response.status_code in (200, 201, 204):
        print(response.json())
    else:
        print('Creating command failed!')
        print(response.status_code)
        print(response.json())


VALID_PRONOUNS = [
    {
        'name': 'She/Her',
        'value': 'She/Her',
    },
    {
        'name': 'He/Him',
        'value': 'He/Him',
    },
    {
        'name': 'They/Them',
        'value': 'They/Them',
    },
    {
        'name': 'Ask for Pronoun',
        'value': 'Ask for Pronoun',
    },
    {
        'name': 'Any Pronoun',
        'value': 'Any Pronoun',
    }
]
pronouns = {
  'name': 'pronouns',
  'description': 'Choose which pronoun roles you have in the server.',
  'options': [
    {
      'name': 'add',
      'description': 'Add a pronoun role to yourself.',
      'type': 1,
      'options': [
        {
          'name': 'pronoun',
          'description': 'The pronoun you want to add.',
          'type': 3,
          'required': True,
          'choices': VALID_PRONOUNS,
        }
      ]
    },
    {
      'name': 'remove',
      'description': 'Remove a pronoun role from yourself.',
      'type': 1,
      'options': [
        {
          'name': 'pronoun',
          'description': 'The pronoun you want to remove.',
          'type': 3,
          'required': True,
          'choices': VALID_PRONOUNS,
        }
      ]
    }
  ],
}

create_command(pronouns)
