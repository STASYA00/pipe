import bpy
from enum import Enum 

from blender_utils import *
from config import ConfigMeta
from texture import Texture

class NODES(Enum):
    BASE = 0
    ROUGHNESS = 1
    DISPLACEMENT = 2
    NORMAL = 3
    METALLIC = 4
    ALPHA = 5
    BSDF = 6
    NORMALMAP = 7
    MIX = 8
    DISPLACEMENTNODE = 9
    MAPPING = 10

class NODESTATE(Enum):
    PASSIVE=0
    ACTIVE=1
    

class TextureMapping(metaclass=ConfigMeta):
    def __init__(self):
        self._content = {
            NODES.BASE: "BASE",
            NODES.ROUGHNESS: "ROUGH",
            NODES.DISPLACEMENT: "DISP",
            NODES.NORMAL: "NRM",
            NODES.METALLIC: "MTL",
            NODES.ALPHA: "ALPHA",
        }
        self._states = {
            NODES.BASE : NODESTATE.ACTIVE,
            NODES.ROUGHNESS : NODESTATE.ACTIVE,
            NODES.DISPLACEMENT : NODESTATE.ACTIVE,
            NODES.NORMAL : NODESTATE.ACTIVE,
            NODES.METALLIC : NODESTATE.ACTIVE,
            NODES.ALPHA : NODESTATE.ACTIVE,
            NODES.BSDF : NODESTATE.PASSIVE,
            NODES.NORMALMAP : NODESTATE.PASSIVE,
            NODES.MIX : NODESTATE.ACTIVE,
            NODES.DISPLACEMENTNODE : NODESTATE.PASSIVE,
            NODES.MAPPING : NODESTATE.ACTIVE,
        }
        self._node_mapping = {
            NODES.BASE: TextureNode,
            NODES.ROUGHNESS: TextureNode,
            NODES.DISPLACEMENT: TextureNode,
            NODES.NORMAL: TextureNode,
            NODES.METALLIC: TextureNode,
            NODES.ALPHA: TextureNode,
            NODES.MIX: Node,
            NODES.MAPPING: Node,
        }
        
    def transforms(self, node):
        return self._states[node].value

    def map_node(self, node):
        return self._node_mapping[node]

    def is_texture(self, node):
        return node in self._content
        
    def suffix(self, node):
        """
        Function that gets the render properties to set in the scene.
        """
        if node in self._content:
            return self._content[node]

        

class Node:
    def __init__(self, material, category, node_name, out_node, socket):
        self.category = category
        self._node_name = node_name
        self._material = material
        self._out_node = out_node
        self._socket = socket
        self._node = self._find()

    def _find(self):
        _candidates = [x for x in self._material.node_tree.nodes if self._node_name in x.name]
        if len(_candidates)>0:
            return _candidates[0]
        
    def update(self, value):
        return self._update(value)

    def _update(self, value):
        _socket = [x for x in self._node.inputs if x.name==self._socket][0]
        _socket.default_value = value


class TextureNode(Node):
    def __init__(self, material, category, node_name, out_node, out_socket):
        Node.__init__(self, material, category, node_name, out_node, out_socket)


    def _find(self):
        _candidates = [x for x in self._material.node_tree.nodes if self._node_name in x.name]
        _out = [x for x in self._material.node_tree.nodes if self._out_node in x.name]
        if (len(_out)>0):
            for _cand in _candidates:
                _link = get_nodes_link(_cand, _out[0], self._material)
                if (_link and _link.to_socket.name == self._socket):
                    return _cand

    def _get_texture(self, value):
        return Texture(value, TextureMapping().suffix(self.category))

    def _update(self, value):
        _texture = self._get_texture(value).content
        self._node.image = _texture

class NodeParams(Enum):
    name = "name"
    out = "out"
    socket = "socket"


class NodeInterface:
    @staticmethod
    def make(name: str, out_name: str, out_socket: str):
        return {
            NodeParams.name.value: name,
            NodeParams.out.value: out_name,
            NodeParams.socket.value: out_socket,
        }



class NodeFactory:
    @staticmethod
    def make(node_type, material, name, out_node, out_socket):
        # material, node_type, _name, _out_node, _out_socket
        return TextureMapping().map_node(node_type)(material, node_type, name, out_node, out_socket)


