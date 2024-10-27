import json
from abc import ABC, abstractmethod
from xml.etree import ElementTree


class DisplayMethod(ABC):
    @abstractmethod
    def display(self, content: str) -> None:
        pass


class ConsoleDisplay(DisplayMethod):
    def display(self, content: str) -> None:
        print(content)


class ReverseDisplay(DisplayMethod):
    def display(self, content: str) -> None:
        print(content[::-1])


class PrintMethod(ABC):
    @abstractmethod
    def print(self, title: str, content: str) -> None:
        pass


class ConsolePrint(PrintMethod):
    def print(self, title: str, content: str) -> None:
        print(f"Printing the book: {title}...")
        print(content)


class ReversePrint(PrintMethod):
    def print(self, title: str, content: str) -> None:
        print(f"Printing the book in reverse: {title}...")
        print(content[::-1])


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


class Book:
    def __init__(self, title: str, content: str) -> None:
        self.title = title
        self.content = content

    def display(self, method: DisplayMethod) -> None:
        method.display(self.content)

    def print_book(self, method: PrintMethod) -> None:
        method.print(self.title, self.content)

    def serialize(self, method: SerializationMethod) -> str:
        return method.serialize(self.title, self.content)


def main(book: Book, commands: list[tuple[str, str]]) -> None | str:
    display_methods = {
        "console": ConsoleDisplay(), "reverse": ReverseDisplay(),
    }
    print_methods = {
        "console": ConsolePrint(), "reverse": ReversePrint(),
    }
    serialization_methods = {
        "json": JSONSerialization(), "xml": XMLSerialization(),
    }

    for cmd, method_type in commands:
        if cmd == "display":
            display_method = display_methods.get(method_type)
            if display_method:
                book.display(display_method)
            else:
                print(f"Unknown display type: {method_type}")
        elif cmd == "print":
            print_method = print_methods.get(method_type)
            if print_method:
                book.print_book(print_method)
            else:
                print(f"Unknown print type: {method_type}")
        elif cmd == "serialize":
            serialization_method = serialization_methods.get(method_type)
            if serialization_method:
                return book.serialize(serialization_method)
            else:
                print(f"Unknown serialize type: {method_type}")


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(main(sample_book, [("display", "reverse"), ("serialize", "xml")]))
