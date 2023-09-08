import re

from util import Log, cmd, ADB_PATH

class LayerInfo:
    def __init__(self, content) -> None:
        self.content = content
        self.type = None
        self.name = None
        self.uid = None
        self.parent = None
        self.zOrderRelativeOf = None
        self.params = {}
        self.children = set()
        self.parse_layer()

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


    def update_children(self, layers):
        for layer in layers:
            if layer.parent == self.name:
                self.children.add(layer)
                # layer.update_children(layers)


class SurfaceFlingerInfo:
    def __init__(self, content) -> None:
        self.content = content
        self.layers = []
        self.rootLayers = []
        self.parse_layers_info()

    def parse_layers_info(self):
        def update_layer_group(layerGroup):
            for layer in layerGroup:
                layer.update_children(layerGroup)
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


    def dump_layer_tree(self):
        def dump_layer_tree_internal(layer, prefix):
            Log.d(prefix + layer.name)
            for child in layer.children:
                dump_layer_tree_internal(child, prefix + '  | ')

        for layer in self.rootLayers:
            dump_layer_tree_internal(layer, '')


def get_surfaceflinger_info():
    dumpsysCmd = ADB_PATH + ['shell', 'dumpsys', 'SurfaceFlinger']
    content = cmd(dumpsysCmd, block=True)
    return SurfaceFlingerInfo(content)

def dump_surfaceflinger():
    Log.i('Dump SurfaceFlinger Info')
    surfaceFlingerInfo = get_surfaceflinger_info()
    surfaceFlingerInfo.dump_layer_tree()
