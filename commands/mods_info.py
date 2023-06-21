import display
import utils
from commands.command import Command


class ModsInfo(Command):
    def __init__(self, parent):
        super().__init__(description='Get info about mod/s', parent=parent)

    def add_arguments(self):
        self.parser.add_argument('mod', help='Name of the mod or mod file')
        self.parser.add_argument('-a', '--advanced', action='store_true', help='Show advanced info about the mod')
        self.parser.add_argument('-d', '--nodesc', action='store_true', help='Hide description')
        self.parser.add_argument('-c', '--changes', action='store_true', help='Show changelogs')

    def execute(self):
        mods = []
        files = utils.get_mod_files()
        results, _ = self.search_by_name(self.args.mod, files)
        if len(results) > 0:
            mod = utils.get_mod_file_info(results[0])
            display.mod_file_info(mod, self.args.advanced, self.args.nodesc, self.args.changes)
        else:
            mods = [utils.get_mod_file_info(f) for f in files]
            results, indexes = self.search_by_name(self.args.mod, [m.title for m in mods])
            if len(results) > 0:
                display.mod_file_info(mods[indexes[0]], self.args.advanced, self.args.nodesc, self.args.changes)
            else:
                print(f"No mods found for the name: '{self.args.mod}'")

    def search_by_name(self, name, names):
        results = []
        indexes = []
        for i, n in enumerate(names):
            if name in n:
                results.append(n)
                indexes.append(i)
        return results, indexes
