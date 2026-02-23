from abc import ABC, abstractmethod
from etomyte.core.server import App
from etomyte.core.exception import TemplateNotFoundError, ContentNotFoundError

class AdapterBase(ABC):

    def __init__(self
        , app:App):
        self.app = app

    @abstractmethod
    def get_content(self, path:str)->str:
        """
        Retrieve content for the given path.
        """
        pass

    @abstractmethod
    def get_template(self, path:str)->str:
        """
        Retrieve template for the given path.
        """
        pass

class CMS():
    def __init__(self
        , app:App
        , adapter:AdapterBase):
        self.app = app
        self.adapter = adapter

    def get_content(self, path:str)->str:
        ctn = self.adapter.get_content(path)
        if ctn is None:
            raise ContentNotFoundError(f"Content not found for path: {path}")
        return ctn
            
    def get_template(self, path:str)->str:
        path = path.strip("/") or "index"
        print(f"Looking for template: {path}")
        try:
            tpl = self.adapter.get_template(path)
            if tpl is None:
                if path == "index":
                    return "Index template"
                raise TemplateNotFoundError(f"Template not found for path: {path}")
            return tpl
        except TemplateNotFoundError:
            parts = [p for p in path.split("/") if p]
            parts.pop()
            path = "/".join(parts)
            return self.get_template(path)