#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv
import argparse

import constant
import commands.download
import commands.info
import commands.search
import commands.mods
from commands.command import Command


class ModInfo:
    def __init__(self, name, author, mod_url, mod_id):
        self.name = name
        self.author = author
        self.mod_url = mod_url
        self.mod_id = mod_id


class ModInfoAdv(ModInfo):
    def __init__(self, name, author, mod_url, mod_id, description, manufacturer, category, size, version, released,
                 download_url):
        super().__init__(name, author, mod_url, mod_id)
        self.description = description
        self.manufacturer = manufacturer
        self.category = category
        self.size = size
        self.version = version
        self.released = released
        self.download_url = download_url


class Fsmm(Command):

    def __init__(self):
        super().__init__(description='FS19 Mod Manager Commands',
                         subcommands=[('search', commands.search.Search), ('download', commands.download.Download),
                                      ('info', commands.info.Info), ('mods', commands.mods.Mods)],
                         usage='''
                                  fsmm <subcommand> [<args>]
                                  Available commands:
                                  search     Search for available mods to download.
                                  download   Download a mod by its name or id.
                                  info       Get info about the mod.
                                  mods       Mod management commands
                               ''')

    def add_arguments(self):
        pass

    def execute(self):
        self.subcommand.execute()


if __name__ == '__main__':
    load_dotenv()
    constant.MODS_DIR = os.getenv('MODS_DIR')
    constant.MOD_LIST = os.getenv('MOD_LIST')
    Fsmm().execute()
