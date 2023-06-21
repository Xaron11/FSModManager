import display
import utils
from commands.command import Command


class ModsConfig(Command):
    def __init__(self, parent):
        super().__init__(description='Configure mod items', parent=parent)

    def add_arguments(self):
        self.parser.add_argument('mod', help='Name of the mod or the file')
        self.parser.add_argument('-r', '--read', action='store_true', help="Read mod's config. (Default)")
        self.parser.add_argument('-w', '--write', nargs='+', help="Write to mod's config. Takes 3 arguments: Store Item Index and Property Name and Propery Value. Can be used multiple times")

    def execute(self):
        mods = []
        mod = None
        files = utils.get_mod_files()
        results, _ = self.search_by_name(self.args.mod, files)
        if len(results) > 0:
            mod = utils.get_mod_file_info(results[0])
        else:
            mods = [utils.get_mod_file_info(f) for f in files]
            results, indexes = self.search_by_name(self.args.mod, [m.title for m in mods])
            if len(results) > 0:
                mod = mods[indexes[0]]
            else:
                print(f"No mods found for the name: '{self.args.mod}'")
                return

        if len(mod.store_items) == 0:
            print(f"Mod does not have items to configure. ({mod.title})")

        if self.args.read or self.args.write is None :
            store_items = utils.read_mod_store_items(mod)
            print(f"Showing {len(store_items)} store items for mod: {mod.title}")
            display.mod_store_items(store_items)

        elif self.args.write:
            items = []
            keys = []
            values = []
            for i, arg in enumerate(self.args.write):
                if i % 3 == 0:
                    items.append(mod.store_items[int(arg)-1])
                elif i % 3 == 1:
                    keys.append(arg)
                else:
                    values.append(arg)
            changes = dict()
            for index, i in enumerate(items):
                if i in changes.keys():
                    changes[i].append((keys[index], values[index]))
                else:
                    changes[i] = []
                    changes[i].append((keys[index], values[index]))

            utils.write_mod_store_items(mod, changes)
            print()
            print(f'{len(changes.keys())} store items changed.')
            store_items = utils.read_mod_store_items(mod)
            print(f"Showing {len(store_items)} store items for mod: {mod.title}")
            display.mod_store_items(store_items)

    def search_by_name(self, name, names):
        results = []
        indexes = []
        for i, n in enumerate(names):
            if name in n:
                results.append(n)
                indexes.append(i)
        return results, indexes
