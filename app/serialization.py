import json
from abc import ABC, abstractmethod
from xml.etree import ElementTree


class SerializationMethod(ABC):
    @abstractmethod
    def serialize(self, title: str, content: str) -> str:
        pass


class JSONSerialization(SerializationMethod):
    def serialize(self, title: str, content: str) -> str:
        return json.dumps({"title": title, "content": content})


class XMLSerialization(SerializationMethod):
    def serialize(self, title: str, content: str) -> str:
        root = ElementTree.Element("book")
        title_elem = ElementTree.SubElement(root, "title")
        title_elem.text = title
        content_elem = ElementTree.SubElement(root, "content")
        content_elem.text = content
        return ElementTree.tostring(root, encoding="unicode")
