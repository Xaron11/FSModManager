import display
import utils
from commands.command import Command


class ModsList(Command):
    def __init__(self, parent):
        super().__init__(description='List mods in your directory', parent=parent)

    def add_arguments(self):
        pass

    def execute(self):
        mods = []
        for f in utils.get_mod_files():
            mods.append(utils.get_mod_file_info(f))

        display.mod_file_list(mods)
