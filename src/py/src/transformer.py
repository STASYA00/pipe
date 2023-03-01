from enum import Enum 

class TRANSFORMATIONS(Enum):
    SCALE=0
    COLOR=1


class Transformer:
    def __init__(self):
        self._factory = TransformationFactory()
        self._transforms = self._load()

    def _load(self):
        _transforms = []
        for t in TRANSFORMATIONS:
            _transforms.append(self._factory(t))
        return _transforms

    def __call__(self, material, value, t):
        self._transforms[t.value].run(material, value)


class Transformation:
    def __init__(self, node_name="Generic", input_index=0):
        self._node_name = node_name
        self._input_index = input_index

    def run(self, material, value):
        return self._run(material, value)
    
    def _get_node(self, material):
        _nodes = [x for x in material.node_tree.nodes if self._node_name in x.name]
        if len(_nodes)>0:
            return _nodes[0]

    def _run(self, material, value):
        _node = self._get_node(material)
        self._update(_node, value)

    def _update(self, node, value):
        node.inputs[self._input_index].default_value = value


class TransformationFactory:
    def __init__(self) -> None:
        self._mapping = TransformationConstructor()
    
    def __call__(self, transformation):
        _values = self._mapping(transformation)
        return Transformation(_values[0], _values[1])


class TransformationConstructor:
    def __init__(self) -> None:
        self._content = {
            TRANSFORMATIONS.SCALE: ("Mapping", 3),
            TRANSFORMATIONS.COLOR: ("Mix", 7)
        }
    
    def __call__(self, transformation:int) -> tuple:
        if transformation in TRANSFORMATIONS:
            return self._content[transformation]