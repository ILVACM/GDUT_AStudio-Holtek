['''
将用于目标检测的标注文件又json格式转化为xml格式
''']
 
import json
import os
 
try:
    import tqdm
except ImportError:
    _IPMtqdm = False
else:
    _IPMtqdm = True
 
class Json_to_Voc():
    #---------------------------
    #头字符串
    #---------------------------
    headstr = """\
    <annotation>
        <folder>VOC</folder>
        <filename>%s</filename>
        <source>
            <database>Database</database>
        </source>
        <size>
            <width>%d</width>
            <height>%d</height>
            <depth>%d</depth>
        </size>
        <segmented>0</segmented>
    """
    #---------------------------
    #目标框字符串
    #---------------------------
    objstr = """\
    <object>
        <name>%s</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>%d</xmin>
            <ymin>%d</ymin>
            <xmax>%d</xmax>
            <ymax>%d</ymax>
        </bndbox>
    </object>
    """
    tailstr = '''\
    </annotation>
    '''
 
    def __init__(self,jsondir:str,xmlsavedir:str) -> None:
        '''
        :description 
        :param 
            jsondir:该目录为存放json文件路径
            xmlsavedir:该目录为放xml文件路径
        :return 
        '''
        self.jsondir = jsondir
        self.xmlsavedir = xmlsavedir
        self.jsonPathList = os.listdir(jsondir)
        self.depth = 3
 
    def convert(self):
        '''
        :description 进行转化json ---> xml
        :param 
        :return 
        '''
        for jsonpath in self.jsonPathList:
            path = os.path.join(self.jsondir,jsonpath)
            with open(path, 'r') as load_f:
                jsondata = json.load(load_f)
            height = jsondata["imageHeight"]    #获取高
            width = jsondata["imageWidth"]      #获取宽
            depth = self.depth
            imgname = os.path.splitext(jsonpath)[0]+os.path.splitext(jsondata["imagePath"])[1]  #获取图片文件名
            head = self.headstr % (imgname, width, height, depth)   #头部信息
            objstr_list = []    
            for points in jsondata["shapes"]:
                tepm = []
                tepm.append(points["label"])    #标签
                tepm.append(points["points"])   #目标位置
                objstr_list.append(tepm)
            ext = os.path.splitext(jsonpath)
            name = ext[0]+".xml"
            Newpath = os.path.join(self.xmlsavedir,name)
            self.write_xml(Newpath,head,objstr_list,self.tailstr)
 
    def convert_tqdm(self):
        '''
        :description 进行转化json ---> xml,
                    与convert相比，区别在于利用tqdm库显示进度，其他部分相同
        :param 
        :return 
        '''
        if _IPMtqdm:    
            pass
        else:
            raise Exception("显示进度需要tqdm模块,否则请调用convert()方法")
 
        with tqdm.tqdm(total=len(self.jsonPathList)) as tq:
            for jsonpath in self.jsonPathList:
                path = os.path.join(self.jsondir,jsonpath)
                with open(path, 'r') as load_f:
                    jsondata = json.load(load_f)
                height = jsondata["imageHeight"]
                width = jsondata["imageWidth"]
                depth = self.depth
                imgname = os.path.splitext(jsonpath)[0]+os.path.splitext(jsondata["imagePath"])[1]
                head = self.headstr % (imgname, width, height, depth) 
                objstr_list = []
                for points in jsondata["shapes"]:
                    tepm = []
                    tepm.append(points["label"])
                    tepm.append(points["points"])
                    objstr_list.append(tepm)
                ext = os.path.splitext(jsonpath)
                name = ext[0]+".xml"
                Newpath = os.path.join(self.xmlsavedir,name)
                self.write_xml(Newpath,head,objstr_list,self.tailstr)
                tq.update(1)
 
    def write_xml(self,Newpath, head, objs, tail)->None:
        '''
        :description 写入xml文件
        :param 
            Newpath：保存路径
            head：voc格式的头部
            objs：voc格式的目标部分
            tail：voc格式的结尾部分
        :return None
        '''
        f = open(Newpath, "w")
        f.write(head)
        for obj in objs:
            f.write(self.objstr % (obj[0], obj[1][0][0], obj[1][0][1], obj[1][1][0], obj[1][1][1]))
        f.write(tail)
        f.close()
 
if __name__ == '__main__':
 
    json_path = "Data/Label1"  # 该目录为存放json文件路径
    xml_path = "Data/labelxml1"  # 该目录为放xml文件路径
    Json_to_Voc(json_path,xml_path).convert_tqdm()