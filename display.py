import sys

from tabulate import tabulate


def mod_list(mods):
    table = [[i, mod.name, mod.author, mod.mod_id] for i, mod in enumerate(mods, start=1)]
    print(tabulate(table, headers=['#', 'Name', 'Author/s', 'ID']))


def mod_file_list(mod_files):
    table = [[i, mod.title, mod.author, mod.version, mod.multiplayer] for i, mod in enumerate(mod_files, start=1)]
    print(tabulate(table, headers=['#', 'Title', 'Author/s', 'Version', 'Multiplayer Support']))


def mod_store_items(store_items):
    table = [[i, item.name, item.type, item.price, item.lifetime, item.brand, item.category, item.specs] for i, item in enumerate(store_items, start=1)]
    print(tabulate(table, headers=['#', 'Name', 'Type', 'Price', 'Lifetime', 'Brand', 'Category', 'Specifications']))


def mod_file_info(mod_file, adv, nodesc, changes):
    if adv:
        table1 = [mod_file.title, mod_file.author, mod_file.version, mod_file.multiplayer]
        if len(mod_file.brands) > 0:
            brands_info = [f'{b[0]} ({b[1]})' for b in mod_file.brands]
            table1.append('\n'.join(brands_info))
        print(tabulate([table1], headers=["Name", "Author/s", "Version", "Multiplayer Support", "Brands"]))
        print()
        table2 = []
        headers2 = []
        splitted = ''.join(mod_file.description).split('Changelog', 1)
        desc = splitted[0]
        changelogs = 'Changelog'
        if not nodesc:
            table2.append(desc)
            headers2.append('Description')
        if changes:
            if len(splitted) > 1:
                table2.append(changelogs + splitted[1])
            else:
                table2.append('############')
            headers2.append('Changelogs')

        print(tabulate([table2], headers=headers2))
    else:
        table = [[mod_file.title, mod_file.author, mod_file.version, mod_file.multiplayer]]
        print(tabulate(table, headers=['Title', 'Author/s', 'Version', 'Description', 'Multiplayer Support']))


def mod_info(mod, adv, nodesc, changes):
    if adv:
        table1 = [
            [mod.name, mod.author, mod.mod_id, mod.manufacturer, mod.category, mod.size, mod.version, mod.released]]
        print(tabulate(table1, headers=["Name", "Author/s", "ID", "Manufacturer", "Category", "Size", "Version",
                                        "Released"]))
        print()
        table2 = []
        headers2 = []
        splitted = ''.join(mod.description).split('Changelog', 1)
        desc = splitted[0]
        changelogs = 'Changelog' + splitted[1]
        if not nodesc:
            table2.append(desc)
            headers2.append('Description')
        if changes:
            table2.append(changelogs)
            headers2.append('Changelogs')

        print(tabulate([table2], headers=headers2))
    else:
        table = [[mod.name, mod.author, mod.mod_id]]
        print(tabulate(table, headers=["Name", "Author/s", "ID"]))
