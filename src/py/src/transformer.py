from enum import Enum 

from material_nodes import *

# class TRANSFORMATIONS(Enum):
#     SCALE=0
#     COLOR=1


class Transformer:
    def __init__(self):
        self._factory = TransformationFactory()
        self._transforms = self._load()

    def _load(self) ->dict:
        _transforms = {}
        for t in NODES:
            if TextureMapping().transforms(t):
                
                _transforms[t.value] = self._factory(t)
        return _transforms

    def __call__(self, material, value, t):

        if TextureMapping().transforms(t):
            self._transforms[t.value].run(material, value)


class Transformation:
    def __init__(self, node=NODES.BASE, **kwargs):
        self._node = node
        self._node_name = kwargs[NodeParams.name.value]
        self._out = kwargs[NodeParams.out.value]
        self._socket = kwargs[NodeParams.socket.value]

    def run(self, material, value):
        return self._run(material, value)
    
    def _get_node(self, material):
        return NodeFactory.make(self._node, material, self._node_name, self._out, self._socket)

    def _run(self, material, value):
        _node = self._get_node(material)
        self._update(_node, value)

    def _update(self, node, value):
        #node.inputs[self._input_index].default_value = value
        node.update(value)


class TransformationFactory:
    def __init__(self) -> None:
        self._mapping = TransformationConstructor()
    
    def __call__(self, transformation):
        _values = self._mapping(transformation)
        return Transformation(node=transformation, **_values)


class TransformationConstructor:
    def __init__(self) -> None:
        self._content = {
            NODES.BASE: NodeInterface.make("Image Texture", "Mix", "Color1"),
            NODES.ROUGHNESS: NodeInterface.make("Image Texture", "Principled BSDF", "Roughness"),
            NODES.DISPLACEMENT: NodeInterface.make("Image Texture", "Displacement", "Height"),
            NODES.NORMAL: NodeInterface.make("Image Texture", "Normal Map", "Color"),
            NODES.METALLIC: NodeInterface.make("Image Texture", "Principled BSDF", "Metallic"),
            NODES.ALPHA: NodeInterface.make("Image Texture", "Principled BSDF", "Alpha"),
            NODES.MIX: NodeInterface.make("Mix", "Principled BSDF", "Color2"),
            NODES.MAPPING: NodeInterface.make("Mapping", "Image Texture", "Scale"),
        }
    
    def __call__(self, transformation:int) -> tuple:
        if transformation in NODES:
            if TextureMapping().transforms(transformation):
                return self._content[transformation]