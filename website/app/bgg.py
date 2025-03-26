import requests
import xml.etree.ElementTree as ET
import sys

base_url_api = 'https://www.boardgamegeek.com/xmlapi'
base_url_api2 = 'https://www.boardgamegeek.com/xmlapi2'
url_builder = {'name': {'base_url': base_url_api, 'query': '/search?search={}'},
                'id': {'base_url': base_url_api2, 'query': '/thing?id={}'}}

# query_type needs to exist in url_builder
def get_bgg_data(query_value, query_type):
    game_search = url_builder[query_type]['query'].format(query_value)
    url = url_builder[query_type]['base_url'] + game_search
    print(url)
    response = requests.get(url)
    return response.content

def get_ele_attrib_obj(xml_obj):
    return xml_obj.attrib

def get_ele_text_obj(xml_obj):
    return xml_obj.text

# Look into better way to have optional arguments; making ele_type_value = None is 1 solution
def find_info(xml_root, path, ele_obj, ele_obj_value = None):
    try:
        child = xml_root.find(path)
        child_obj = getattr(sys.modules[__name__], f'get_ele_{ele_obj}_obj')(child)
        if ele_obj_value:
            return child_obj[ele_obj_value]
        else:
            return child_obj
    except:
        #print(f'root.find("{path}").{ele_obj}.["{ele_obj_value}"] does not exist') if ele_obj_value else print(f'root.find("{path}").{ele_obj} does not exist')
        return None

def find_link_info(xml_root, path):
    try:
        list_info = []
        for data in xml_root.findall(path):
            list_info.append(data.attrib['value'])
        return list_info
    except:
        return None

def get_sugg_numplayers(xml_root, path):
    try:
        sugg_numplayers = {}
        child = xml_root.find(path)
        for result in child:
            num_of_players = result.attrib['numplayers']
            voted_suggestions = {}
            for recc in result:
                voted_suggestions[recc.attrib['value']] = recc.attrib['numvotes']
            sugg_numplayers[num_of_players] = voted_suggestions
        return sugg_numplayers
    except:
        return None

def process_name_search(raw_xml):
    """Takes raw XML 'raw_xml' and returns dictionary of {game_id: {name: <game name>, year_published: <year_published>}}"""
    search_dict = {}
    root = ET.fromstring(raw_xml)
    for boardgame in root.findall('boardgame'):
        # WIP: Error catch game_id
        game_id = boardgame.attrib['objectid']
        name = find_info(boardgame, './name', 'text')
        year_published = find_info(boardgame, './yearpublished', 'text')
        search_dict[game_id] = {'name': name, 'year_published': year_published}
    return search_dict

def process_id_search(raw_xml):
    root = ET.fromstring(raw_xml)
    dict_keys = ['name', 'image', 'description', 'year_published', 'player_count', 'suggested_numplayers', 'categories', 'mechanics']
    data = dict.fromkeys(dict_keys)
    data['name'] = find_info(root, './item/name/[@type = \'primary\']', 'attrib', 'value')
    data['image'] = find_info(root, './item/image', 'text')
    data['description'] = find_info(root, './item/description', 'text')
    data['year_published'] = find_info(root, './item/yearpublished', 'attrib', 'value')
    minplayers = find_info(root, './item/minplayers', 'attrib', 'value')
    maxplayers = find_info(root, './item/maxplayers', 'attrib', 'value')
    data['player_count'] = f'{minplayers} - {maxplayers}'
    data['suggested_numplayers'] = get_sugg_numplayers(root, './item/poll/[@name = \'suggested_numplayers\']')
    data['categories'] = find_link_info(root, './item/link/[@type = \'boardgamecategory\']')
    data['mechanics'] = find_link_info(root, './item/link/[@type = \'boardgamemechanic\']')
    return data

def search_via_name(name):
    xml = get_bgg_data(name, 'name')
    name_search_dict = process_name_search(xml)
    return name_search_dict

def search_via_id(game_id):
    xml = get_bgg_data(game_id, 'id')
    game_info_dict = process_id_search(xml)
    return game_info_dict

def main():
    game = 'catan'
    xml = get_bgg_data(game, 'name')
    name_search_dict = process_name_search(xml)
    print(name_search_dict)

    game_id = 13
    xml = get_bgg_data(game_id, 'id')
    game_info_dict = process_id_search(xml)
    print(game_info_dict)

if __name__ == '__main__':
    main()