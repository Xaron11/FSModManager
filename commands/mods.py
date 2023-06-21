import argparse

from commands.command import Command
import commands.mods_list
import commands.mods_info
import commands.mods_config


class Mods(Command):
    def __init__(self, parent):
        super().__init__(description='Mod Management Commands', parent=parent,
                         subcommands=[('list', commands.mods_list.ModsList), ('info', commands.mods_info.ModsInfo),
                                      ('config', commands.mods_config.ModsConfig)],
                         usage='''
                                  fsmm mods <subcommand> [<args>]
                                  Available subcommands:
                                  list     List mods in your directory.
                                  info     Get info about mod/s.
                                  config   Configure mod items.
                                  update   Update mod/s to the newest version.
                               ''')

    def add_arguments(self):
        pass

    def execute(self):
        self.subcommand.execute()
