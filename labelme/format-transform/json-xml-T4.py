'''
labelme标注工具标注一些关键点，没有标注框,此程序用于将这些json文件批量转成VOC格式的xml文件
'''
import json
import os
import xml.etree.ElementTree as ET

def json_to_xml(json_file, xml_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    root = ET.Element('annotation')

    folder = ET.SubElement(root, 'folder')
    folder.text = 'VOC2007'  # 替换为你自己的文件夹名称

    filename = ET.SubElement(root, 'filename')
    filename.text = os.path.splitext(os.path.basename(json_file))[0] + '.jpg'  # 将 .json 文件的文件名替换为对应的 .jpg 文件名

    size = ET.SubElement(root, 'size')
    width = ET.SubElement(size, 'width')
    width.text = str(data['imageWidth'])
    height = ET.SubElement(size, 'height')
    height.text = str(data['imageHeight'])
    depth = ET.SubElement(size, 'depth')
    depth.text = '3'  # 如果您的图像是灰度图像，请将此值更改为 1

    for shape in data['shapes']:
        if shape['shape_type'] == 'point':  # 仅处理关键点类型的标注
            point = shape['points'][0]

            object_node = ET.SubElement(root, 'object')
            name = ET.SubElement(object_node, 'name')
            name.text = shape['label']
            pose = ET.SubElement(object_node, 'pose')
            pose.text = 'Unspecified'
            truncated = ET.SubElement(object_node, 'truncated')
            truncated.text = '0'
            difficult = ET.SubElement(object_node, 'difficult')
            difficult.text = '0'
            bndbox = ET.SubElement(object_node, 'bndbox')
            xmin_node = ET.SubElement(bndbox, 'xmin')
            xmin_node.text = str(int(point[0]))
            ymin_node = ET.SubElement(bndbox, 'ymin')
            ymin_node.text = str(int(point[1]))
            xmax_node = ET.SubElement(bndbox, 'xmax')
            xmax_node.text = str(int(point[0]))
            ymax_node = ET.SubElement(bndbox, 'ymax')
            ymax_node.text = str(int(point[1]))

    tree = ET.ElementTree(root)
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    input_dir = '\json'  # 输入目录
    output_dir = '\xml输出'  # 输出目录

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            json_file = os.path.join(input_dir, filename)
            xml_file = os.path.join(output_dir, os.path.splitext(filename)[0] + '.xml')
            json_to_xml(json_file, xml_file)

