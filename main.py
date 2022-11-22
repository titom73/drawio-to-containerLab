import xmltodict
import pprint
from pydantic import BaseModel
from jinja2 import FileSystemLoader, Environment
import docker
from simple_term_menu import TerminalMenu


def readxml(file_name):
    with open(f'data/{file_name}.xml', 'r', encoding='utf-8') as file:
        my_xml = file.read()
    return my_xml


class Node(BaseModel):
    id = ""
    value = ""
    target = ""
    source = ""
    parent = ""
    x = ""


def find_value(endpoint):
    return [item.value for item in objects_drawio_in_class_node if item.id == endpoint]


def find_link(objects_drawio):
    return [[item.id,item.source, item.target] for item in objects_drawio if item.value == '']


def find_interfaces(links):
    links_tempo = []
    for node_id in links:
        interfaces = [[item.x, item.value] for item in objects_drawio_in_class_node if item.value.lower().find('eth') == 0 and item.parent == node_id[0]]
        links_tempo.append([f"{find_value(node_id[1])[0]}:{interfaces[0][1].lower()}", f"{find_value(node_id[2])[0]}:{interfaces[1][1].lower()}"])
    return links_tempo

def moving_x(objects_drawio):
    objects_drawio_without_special_caract = []
    for item in objects_drawio:
        if 'mxGeometry' in (item) and '@x' in item['mxGeometry']:
            item.update({'@x':item['mxGeometry']['@x']})
        objects_drawio_without_special_caract.append({k.replace('@', ''): item[k] for k in item})
    return objects_drawio_without_special_caract


if __name__ == '__main__':
    lab_name = input('Enter your Lab name : ')
    client = docker.from_env()
    images_docker_brut = client.images.list()
    images_docker = [str(item).split("'")[1] for item in images_docker_brut]
    terminal_menu = TerminalMenu(images_docker)
    menu_entry_index = terminal_menu.show()
    lab_image = images_docker[menu_entry_index]

    result = readxml("test-drawio-V7")
    my_dict = xmltodict.parse(result)
    objects_drawio = my_dict['mxfile']['diagram']['mxGraphModel']['root']['mxCell']

    result = moving_x(objects_drawio)
    objects_drawio_in_class_node = [Node(**extraction) for extraction in result if len(extraction) > 2]
    nodes_yaml = [item.value for item in objects_drawio_in_class_node if item.value.lower().find('eth') != 0 and len(item.value) > 0]
    links = find_link(objects_drawio_in_class_node)
    links_yaml = find_interfaces(links)

    # lab_name = "Lab_test"
    # lab_image = "arista/ceos:4.29.0.2F"

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('lab_template.txt')

    output = template.render(lab_name=lab_name,lab_image=lab_image,nodes_yaml=nodes_yaml,links_yaml=links_yaml)

    with open(f'data/{lab_name}.yml', 'w') as yaml_file:
        yaml_file.write(output)
