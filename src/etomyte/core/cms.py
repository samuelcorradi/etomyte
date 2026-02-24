from abc import ABC, abstractmethod
import re
from git_repo.src.etomyte.core.app import Server
from etomyte.core.exception import TemplateNotFoundError, ContentNotFoundError

class AdapterBase(ABC):

    def __init__(self
        , app:App):
        self.app = app

    @abstractmethod
    def get_snippet(self, path:str)->str:
        """
        Retrieve snippet for the given path.
        """
        pass

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

    def exec_snippet(self, code:str, params:dict)->str:
        """
        """
        local_vars = {**params, "app": self.app}
        exec(code, {}, local_vars)
        return local_vars.get("result")
    
    def process_snippets(self, text:str) -> str:
        """
        """
        pattern = re.compile(r"\[\[([^\]]+)\]\]")
        def _replace(match: re.Match)->str:
            full = match.group(1).strip()
            name, params = full, {}
            if "?" in full:
                name, param_str = full.split("?", 1)
                params = {
                    k: v
                    for part in param_str.split(",")
                    if "=" in part
                    for k, v in [part.split("=", 1)]
                }
            code = self.get_snippet(name)
            result = self.exec_snippet(code, params)
            if result is None:
                result = match.group(0)
            return result
        return pattern.sub(_replace, text)

    def get_snippet(self, name:str)->str:
        code = self.adapter.get_snippet(name)
        if code is None:
            raise ContentNotFoundError(f"Snippet not found for name: {name}")
        return code

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