import xmltodict
import pprint
from pydantic import BaseModel


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
    return [item.value for item in result_nodes if item.id == endpoint]


if __name__ == '__main__':
    result = readxml("test-drawio-V5")
    my_dict = xmltodict.parse(result)
    objects_drawio = my_dict['mxfile']['diagram']['mxGraphModel']['root']['mxCell']
    objects_drawio_without_special_caract = []
    for item in objects_drawio:
        if 'mxGeometry' in (item) and '@x' in item['mxGeometry']:
            item.update({'@x':item['mxGeometry']['@x']})
        objects_drawio_without_special_caract.append({k.replace('@', ''): item[k] for k in item})
    result_nodes = [Node(**extraction) for extraction in objects_drawio_without_special_caract if len(extraction)>2]
    endpoints = []
    # search only the link between nodes
    for node in result_nodes:
        if node.value == '':
            endpoint_id = node.id
            endpoint_source = find_value(node.source)
            endpoint_target = find_value(node.target)
            endpoints.append([endpoint_id, endpoint_source[0], endpoint_target[0]])
    links_endpoints = []
    # search the interface used for the link
    for node_id in endpoints:
        interfaces = [[item.x, item.value] for item in result_nodes if item.value.find('eth') == 0 and item.parent == node_id[0]]
        links_endpoints.append([f"{node_id[1]}:{interfaces[0][1]}, {node_id[2]}:{interfaces[1][1]}"])
    print(links_endpoints)
