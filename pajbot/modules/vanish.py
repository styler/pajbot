import logging

import pajbot.models
from pajbot.modules import BaseModule
from pajbot.modules import ModuleSetting

log = logging.getLogger(__name__)


class VanishModule(BaseModule):

    ID = __name__.split('.')[-1]
    NAME = 'Vanish'
    DESCRIPTION = 'Gives users a command to use if they want to time themselves out for a second.'
    CATEGORY = 'Feature'
    SETTINGS = [
            ModuleSetting(
                key='command_name',
                label='Command name (i.e. vanish)',
                type='text',
                required=True,
                placeholder='Command name (no !)',
                default='vanish',
                constraints={
                    'min_str_len': 2,
                    'max_str_len': 15,
                    }),
            ModuleSetting(
                key='online_global_cd',
                label='Global cooldown (seconds)',
                type='number',
                required=True,
                placeholder='',
                default=0,
                constraints={
                    'min_value': 0,
                    'max_value': 600,
                    }),
            ModuleSetting(
                key='online_user_cd',
                label='Per-user cooldown (seconds)',
                type='number',
                required=True,
                placeholder='',
                default=60,
                constraints={
                    'min_value': 0,
                    'max_value': 3600,
                    }),
            ModuleSetting(
                key='cost',
                label='Point cost',
                type='number',
                required=True,
                placeholder='Point cost',
                default=0,
                constraints={
                    'min_value': 0,
                    'max_value': 5000,
                    }),
            ]

    def __init__(self):
        super().__init__()

    def vanish_command(self, **options):
        source = options['source']
        bot = options['bot']
        bot.execute_delayed(0.5, bot._timeout, (source.username, 1))

    def load_commands(self, **options):
        self.commands[self.settings['command_name'].lower().replace('!', '').replace(' ', '')] = pajbot.models.command.Command.raw_command(self.vanish_command,
                delay_all=self.settings['online_global_cd'],
                delay_user=self.settings['online_user_cd'],
                description='Time yourself out for a second!',
                cost=self.settings['cost'],
                )
