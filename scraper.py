import requests
from lxml import html
from urllib.parse import urlparse, urlencode, parse_qs
import constant
from fsmm import ModInfo, ModInfoAdv


def merge_url_params(url, params):
    url += ('&' if urlparse(url).query else '?') + urlencode(params)
    return url


def request_html(url):
    r = requests.get(url)
    return html.document_fromstring(r.content)


def scrape_mod_item_info(mod_item_info, url, mod_id):
    name = mod_item_info.xpath('h2/text()')[0]
    info_tabs = mod_item_info.xpath('div')
    description = info_tabs[0].xpath('div/text()')

    other_desc = info_tabs[1].xpath('div//div[@class="table-row"]')
    manufacturer = other_desc[1].xpath('div[@class="table-cell"]/text()')[0]
    category = other_desc[2].xpath('div[@class="table-cell"]/text()')[0]
    author = other_desc[3].xpath('div//a/text()')[0]
    size = other_desc[4].xpath('div[@class="table-cell"]/text()')[0]
    version = other_desc[5].xpath('div[@class="table-cell"]/text()')[0]
    release = other_desc[6].xpath('div[@class="table-cell"]/text()')[0]

    download = info_tabs[2].xpath('div//a/@href')[0]

    return ModInfoAdv(name, author, url, mod_id, description, manufacturer, category, size, version, release, download)


def scrape_mods_info(mod_items):
    mod_urls = [mod_item.xpath('a/@href')[0] for mod_item in mod_items]
    for i, url in enumerate(list(mod_urls)):
        if url.startswith('dlc'):
            del mod_urls[i]
            del mod_items[i]

    mod_ids = [parse_qs(urlparse(constant.FS_URL + mod_url).query).get('mod_id')[0] for
               mod_url in mod_urls]
    mod_contents = [mod_item.xpath('div[@class="mod-item__content"]')[0] for mod_item in mod_items]
    mod_names = [mod_content.xpath('h4/text()')[0] for mod_content in mod_contents]
    mod_author_texts = [mod_content.xpath('p/span/text()')[0] for mod_content in mod_contents]
    mod_authors = [mod_author_text[mod_author_text.index(' '):] for mod_author_text in mod_author_texts]
    return [ModInfo(mod_names[i], mod_authors[i], mod_urls[i], mod_ids[i]) for i in range(len(mod_names))]


def get_mods_info_mods_url(url):
    print('Searching...')
    tree = request_html(url)
    mod_items = tree.xpath('//div[@class="mod-item"]')
    return scrape_mods_info(mod_items)


def get_mod_info_adv_from_id(mod_id):
    print('Searching...')
    url = merge_url_params(constant.FS_MOD_URL, {'mod_id': str(mod_id)})
    tree = request_html(url)
    mod_item_info = tree.xpath('//div[@class="row box-mods-item-info"]')[0]
    return scrape_mod_item_info(mod_item_info, url, mod_id)


def get_mods_page_count(url):
    tree = request_html(url)
    pages = tree.xpath('//div[@class="pagination-wrap"]/ul[@role="navigation"]/li')
    return len(pages)


def get_mods_info_category(category):
    print('Searching...')
    url = merge_url_params(constant.FS_MODS_URL, {'filter': category})
    return get_mods_info_all(url)


def get_mods_info_search_category(search_query, category):
    all_mods = get_mods_info_category(category)

    mods = []
    for mod in all_mods:
        if search_query in mod.name:
            mods.append(mod)

    return mods


def get_mods_info_all(start_url):
    pages = get_mods_page_count(start_url)
    mods = get_mods_info_mods_url(start_url)
    for p in range(1, pages):
        page_url = merge_url_params(start_url, {'page': str(p)})
        mods.extend(get_mods_info_mods_url(page_url))

    return mods


def get_mods_info_search_all(search_query):
    url = merge_url_params(constant.FS_MODS_URL, {'searchMod': search_query})
    return get_mods_info_all(url)


def get_mods_info_search(search_query):
    url = merge_url_params(constant.FS_MODS_URL, {'searchMod': search_query})
    return get_mods_info_mods_url(url)
