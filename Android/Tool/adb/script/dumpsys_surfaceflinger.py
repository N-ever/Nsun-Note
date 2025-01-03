import re

from util import Log, cmd, ADB_PATH

global index
index = 0
class LayerInfo:
    def __init__(self, content) -> None:
        global index
        self.content = content
        self.type = None
        self.name = None
        self.uid = None
        self.parent = None
        self.zOrderRelativeOf = None
        self.params = {}
        self.children = set()
        self.parse_layer()
        self.index = index
        index += 1

    def parse_layer(self):
        reLayer = re.compile(r'\+\s(\S+Layer)\s\((.*)\)\suid=(\d+)\s+'
                            #  r'(Region\s\S+\s\(this=\d+\scount=\d+\)\s+)'
                            #  r'(Region\s\S+\s\(this=\d+\scount=\d+\)\s+)'
                            #  r'(Region\s\S+\s\(this=\d+\scount=\d+\)\s+)'
                             r'.*'
                             r'(layerStack[^\n]+)\s+'
                             r'parent=([^\n]+)\s+'
                             r'zOrderRelativeOf=([^\n]+)\s+'
                             r'([^\n]+)\s+'
                             , re.DOTALL)
        rst = reLayer.match(self.content)
        if rst:
            self.type = rst.group(1)
            self.name = rst.group(2)
            self.uid = rst.group(3)
            self.parent = rst.group(5)
            self.zOrderRelativeOf = rst.group(6)
            rst_params = re.findall(r'(\S+)=(.*?)(?=,\s\S+=|$)', rst.group(4), re.DOTALL)
            rst_params2 = re.findall(r'(\S+)=(.*?)(?=,\s\S+=|$)', rst.group(7), re.DOTALL)
            rst_params.extend(rst_params2)
            for params in rst_params:
                self.params[params[0]] = params[1].strip()
        else:
            Log.e('Parse layer failed: {}'.format(self.content), exit=True)


    def __str__(self) -> str:
        return 'LayerInfo(type={}, name={}, uid={}, parent={}, zOrderRelativeOf={}, params={}, children={})'.format(
            self.type, self.name, self.uid, self.parent, self.zOrderRelativeOf, self.params, self.children
        )


    def update_parent(self, layers, index):
        for layer in reversed(layers[0:index]):
            if self.parent == layer.name:
                layer.children.add(self)
                return
        for layer in reversed(layers[index:len(layers)]):
            if self.parent == layer.name:
                layer.children.add(self)
                return
        print(str(self) + ' do not find parent')

class SurfaceFlingerInfo:
    def __init__(self, content) -> None:
        self.content = content
        self.layers = []
        self.rootLayers = []
        self.parse_layers_info()

    def parse_layers_info(self):
        def update_layer_group(layerGroup):
            for index, layer in enumerate(layerGroup):
                layer.update_parent(layerGroup, index)
            self.layers.extend(layerGroup)
        reLayer = re.compile(r'\+\s\S+Layer.*?(?=\+\s\S+Layer|\Z|Offscreen\sLayers)', re.DOTALL)
        rst = reLayer.findall(self.content)
        layerGroup = []
        for layer in rst:
            layerInfo  = LayerInfo(layer)
            if layerInfo.parent == 'none':
                self.rootLayers.append(layerInfo)
                if len(layerGroup) > 0:
                    update_layer_group(layerGroup)
                    layerGroup.clear()
            layerGroup.append(layerInfo)
        update_layer_group(layerGroup)

    global count
    count = 0
    def dump_layer_tree(self):
        def dump_layer_tree_internal(layer, prefix):
            global count
            count += 1
            Log.d(prefix + layer.name + ' z: ' + layer.params['z'] + ' flags: ' + layer.params['flags'] + " " + str(count) + ' ' + str(layer.index))
            for child in layer.children:
                dump_layer_tree_internal(child, prefix + '  | ')

        for layer in self.rootLayers:
            dump_layer_tree_internal(layer, '')


def get_surfaceflinger_info():
    dumpsysCmd = ADB_PATH + ['shell', 'dumpsys', 'SurfaceFlinger']
    content = cmd(dumpsysCmd, block=True)
    # with open("/Users/evern.zhu/Downloads/surfaceflinger1.txt", 'r+') as f:
    #     content = f.read()
    return SurfaceFlingerInfo(content)

def dump_surfaceflinger():
    Log.i('Dump SurfaceFlinger Info')
    surfaceFlingerInfo = get_surfaceflinger_info()
    surfaceFlingerInfo.dump_layer_tree()
