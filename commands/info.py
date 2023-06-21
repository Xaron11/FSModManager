import constant
import display
import scraper
import utils

from commands.command import Command


class Info(Command):
    def __init__(self, parent):
        super().__init__('Get info about the mod', parent=parent)

    def add_arguments(self):
        self.parser.add_argument('mod', help='Name of the mod or id')
        self.parser.add_argument('-a', '--advanced', action='store_true', help='Show advanced info about the mod')
        self.parser.add_argument('-d', '--nodesc', action='store_true', help='Hide description')
        self.parser.add_argument('-c', '--changes', action='store_true', help='Show changelogs')
        self.parser.add_argument('-m', '--save', metavar='FILE', nargs='?',
                                 const=f'{constant.MODS_DIR}/{constant.MOD_LIST}', default=None,
                                 help='Save mod id into the specified file (default: your_mods_folder/mods.txt)')

    def execute(self):
        mod = None
        try:
            mod_id = int(self.args.mod)
            mod = scraper.get_mod_info_adv_from_id(mod_id)
        except ValueError:
            mod = scraper.get_mods_info_search(self.args.mod)[0]
            if self.args.advanced or not self.args.nodesc or self.args.changes:
                mod = scraper.get_mod_info_adv_from_id(mod.mod_id)

        if self.args.save:
            if not utils.check_string_and_append_to_file(self.args.save, mod.mod_id):
                print('Mod is already on the list')

        print()
        display.mod_info(mod, self.args.advanced, self.args.nodesc, self.args.changes)
