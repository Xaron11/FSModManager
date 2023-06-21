import os
from zipfile import ZipFile
import requests
from lxml import etree
import constant
from tqdm import tqdm


class ModFileInfo:
    def __init__(self, title, author, version, description, multiplayer, store_items, brands, file):
        self.title = title
        self.author = author
        self.version = version
        self.description = description
        self.multiplayer = multiplayer
        self.store_items = store_items
        self.brands = brands
        self.file = file


class ModFileStoreItem:
    def __init__(self, type, name, specs, price, lifetime, brand, category):
        self.type = type
        self.name = name
        self.specs = specs
        self.price = price
        self.lifetime = lifetime
        self.brand = brand
        self.category = category


def get_default_lang_path(element, child):
    c = element.xpath(f'{child}/en')
    if len(c) == 0:
        c = element.xpath(f'{child}')
    return c[0].text


def set_default_lang_path(element, child, value):
    c = element.xpath(f'{child}/en')
    if len(c) == 0:
        c = element.xpath(f'{child}')
    c[0].text = value
    return c[0]


def read_mod_store_items(mod):
    store_items = []
    file = constant.MODS_DIR + '/' + mod.file
    with ZipFile(file, 'r') as z:
        for item in mod.store_items:
            with z.open(item, 'r') as f:
                tree = etree.parse(f)
                type = tree.xpath('/vehicle/@type')[0]
                data = tree.xpath('/vehicle/storeData')[0]
                name = get_default_lang_path(data, 'name')
                spec_nodes = data.xpath('specs/*')
                specs = dict(zip([spec.tag for spec in spec_nodes], [spec.text for spec in spec_nodes]))

                price = data.xpath('price')[0].text
                lifetime = data.xpath('lifetime')[0].text
                brand = data.xpath('brand')[0].text
                category = data.xpath('category')[0].text

                store_items.append(ModFileStoreItem(str(type), name, specs, int(price), int(lifetime), brand, category))

    return store_items


def write_mod_store_items(mod, changes):
    file = constant.MODS_DIR + '/' + mod.file
    dst_file = constant.MODS_DIR + '/' + mod.file + '.tmp'
    with ZipFile(file) as inzip, ZipFile(dst_file, "w") as outzip:
        for inzip_info in inzip.infolist():
            with inzip.open(inzip_info) as infile:
                for f in changes.keys():
                    if inzip_info.filename == f:
                        tree = etree.parse(infile)
                        content = modify_store_item(tree, changes[f])
                        outzip.writestr(inzip_info.filename, content)
                        break
                else:
                    outzip.writestr(inzip_info.filename, infile.read())

    os.remove(file)
    os.rename(dst_file, file)


def modify_store_item(tree, properties):
    for p_key, p_value in properties:
        p_key_l = p_key.lower()
        if p_key_l == 'type':
            tree.xpath('/vehicle')[0].attrib['type'] = p_value
        elif p_key_l == 'name':
            c = tree.xpath('/vehicle/storeData/name/en')
            if len(c) == 0:
                c = tree.xpath('/vehicle/storeData/name')
            c[0].text = p_value
        elif p_key_l == 'price':
            tree.xpath('/vehicle/storeData/price')[0].text = p_value
        elif p_key_l == 'lifetime':
            tree.xpath('/vehicle/storeData/lifetime')[0].text = p_value
        elif p_key_l == 'brand':
            tree.xpath('/vehicle/storeData/brand')[0].text = p_value
        elif p_key_l == 'category':
            tree.xpath('/vehicle/storeData/category')[0].text = p_value
        else:  # specs
            tree.xpath(f'/vehicle/storeData/specs/{p_key}')[0].text = p_value

    root = tree.getroot()
    return etree.tostring(root, encoding='utf-8', pretty_print=True)


def get_mod_files():
    files = os.listdir(constant.MODS_DIR)
    mod_files = []
    for file in files:
        if os.path.splitext(file)[1] == '.zip':
            mod_files.append(file)

    return mod_files


def get_mod_file_info(mod_file):
    file = constant.MODS_DIR + '/' + mod_file
    with ZipFile(file, 'r') as z:
        with z.open('modDesc.xml', 'r') as f:
            tree = etree.parse(f)
            desc = tree.xpath('/modDesc')[0]
            title = get_default_lang_path(desc, 'title')
            author = desc.xpath('author')[0].text
            version = desc.xpath('version')[0].text
            description = get_default_lang_path(desc, 'description')
            multiplayer = desc.xpath('multiplayer/@supported')[0]

            store_items = desc.xpath('storeItems/storeItem/@xmlFilename')
            if store_items is None:
                store_items_list = []
            else:
                store_items_list = [str(i) for i in store_items]
            brands = desc.xpath('brands/brand')
            if brands is None:
                brands_list = []
            else:
                brands_list = list(
                    zip([str(b.xpath('@name')[0]) for b in brands], [str(b.xpath('@title')[0]) for b in brands]))

    return ModFileInfo(title, author, version, description, bool(multiplayer), store_items_list, brands_list, mod_file)


def download_file(url, overwrite):
    print('Downloading...')
    h = {'Referer': constant.FS_URL}
    name = os.path.basename(url)
    file = constant.MODS_DIR + '/' + name
    if not overwrite and os.path.exists(file):
        print(f'File already exist. ({name})')
        return
    with open(file, "wb") as f:
        r = requests.get(url, headers=h)
        f.write(r.content)
        print(f'File downloaded. ({name})')


def check_string_and_append_to_file(file, string, new_line=True):
    with open(file, 'r+') as f:
        if string in f.readlines():
            return False
        if new_line:
            f.write('\n')
        f.write(string)
        return True


def append_to_file(file, string, new_line=True):
    with open(file, 'a+') as f:
        if new_line:
            f.write('\n')
        f.write(string)


def download_file_with_progress(url, overwrite):
    print('Downloading...')
    name = os.path.basename(url)
    file = constant.MODS_DIR + '/' + name
    if not overwrite and os.path.exists(file):
        print(f'File already exist. ({name})')
        return
    h = {'Referer': constant.FS_URL}
    r = requests.get(url, stream=True, headers=h)
    total_size_in_bytes = int(r.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(file, 'wb') as f:
        for data in r.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print(f'File was not downloaded correctly. ({name})')
        return

    print(f'File downloaded. ({name})')
