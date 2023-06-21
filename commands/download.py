import constant
import display
import scraper
import utils

from commands.command import Command


class Download(Command):
    def __init__(self, parent):
        super().__init__('Download a mod by its name or id', parent=parent)

    def add_arguments(self):
        self.parser.add_argument('mod', help='Name of the mod or id', nargs='?', default=None)
        self.parser.add_argument('-a', '--advanced', action='store_true', help='Show advanced info about the mod')
        self.parser.add_argument('-n', '--noinfo', action='store_true', help="Don't show any info")
        self.parser.add_argument('-d', '--nodesc', action='store_true', help='Hide description')
        self.parser.add_argument('-c', '--changes', action='store_true', help='Show changelogs')
        self.parser.add_argument('-p', '--noprogress', action='store_true', help='Hide progress bar')
        self.parser.add_argument('-o', '--overwrite', action='store_true',
                                 help='Overwrite current mods if the names are the same as downloaded ones')
        self.parser.add_argument('-f', '--file', nargs='?', const=f'{constant.MODS_DIR}/{constant.MOD_LIST}',
                                 default=None,
                                 help='Download mods specified in the file by ids (default: your_mods_folder/mods.txt)')
        self.parser.add_argument('-s', '--skip', action='store_true',
                                 help="Skip downloading a mod if its id isn't correct")
        self.parser.add_argument('-m', '--save', metavar='FILE', nargs='?',
                                 const=f'{constant.MODS_DIR}/{constant.MOD_LIST}', default=None,
                                 help='Save mod id into the specified file (default: your_mods_folder/mods.txt)')

    def execute(self):
        if self.args.file:
            lines = []
            with open(self.args.file, "r") as f:
                lines = f.readlines()

            for i, line in enumerate(lines, start=1):
                if len(line) == 0:
                    continue
                mod_id = None
                try:
                    mod_id = int(line)
                except ValueError:
                    if self.args.skip:
                        continue
                    else:
                        print(f"ID: '{line}' in file: '{self.args.file}' is not correct. (Line: {i})")
                        exit(1)

                mod = scraper.get_mod_info_adv_from_id(mod_id)
                print(f'Mod found. ({mod.name})')
                self.display_and_download(mod, not self.args.noprogress)
            return

        if self.args.mod is None:
            print("'mod' argument is required unless you use: '--file' flag")
            self.parser.print_help()
            exit(1)

        mod = None
        try:
            mod_id = int(self.args.mod)
            mod = scraper.get_mod_info_adv_from_id(mod_id)
        except ValueError:
            found_mods = scraper.get_mods_info_search(self.args.mod)
            if len(found_mods) == 0:
                print('Mod not found.')
                exit(1)

            mod = scraper.get_mod_info_adv_from_id(found_mods[0].mod_id)

        print(f'Mod found. ({mod.name})')

        if self.args.save:
            if not utils.check_string_and_append_to_file(self.args.save, mod.mod_id):
                print('Mod is already on the list')

        self.display_and_download(mod, not self.args.noprogress)

    def display_and_download(self, mod, progress):
        if not self.args.noinfo:
            print()
            display.mod_info(mod, self.args.advanced, self.args.nodesc, self.args.changes)
            print()
        if progress:
            utils.download_file_with_progress(mod.download_url, self.args.overwrite)
        else:
            utils.download_file(mod.download_url, self.args.overwrite)