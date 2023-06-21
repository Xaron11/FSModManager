import constant
import display
import scraper
import utils

from commands.command import Command


class Search(Command):

    def __init__(self, parent):
        super().__init__('Search for available mods to download', parent=parent)

    def add_arguments(self):
        self.parser.add_argument('query', help='Query to search for', nargs='?', default=None)
        self.parser.add_argument('-a', '--all', action='store_true', help='Show all search results')
        self.parser.add_argument('-c', '--category', choices=constant.CATEGORIES)
        self.parser.add_argument('-d', '--download', action='store_true', help='Download all search results')
        self.parser.add_argument('-p', '--noprogress', action='store_true', help='Hide progress bar when downloading')

    def execute(self):
        if self.args.query is None and self.args.category is None:
            print("'query' argument can be omitted only if you use: '--category' flag")
            self.parser.print_help()
            exit(1)

        if self.args.category:
            if self.args.query:
                mods = scraper.get_mods_info_search_category(self.args.query, self.args.category)
            else:
                mods = scraper.get_mods_info_category(self.args.category)
        else:
            if self.args.all:
                mods = scraper.get_mods_info_search_all(self.args.query)
            else:
                mods = scraper.get_mods_info_search(self.args.query)
        print(f'Mods found: {len(mods)}.')
        print()
        display.mod_list(mods)

        if self.args.download:
            for mod in mods:
                if self.args.noprogress:
                    utils.download_file(scraper.get_mod_info_adv_from_id(mod.mod_id).download_url, False)
                else:
                    utils.download_file_with_progress(scraper.get_mod_info_adv_from_id(mod.mod_id).download_url, False)
