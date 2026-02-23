class TemplateNotFoundError(Exception):
    """
    Raised when a template file is not found.
    """
    pass

class ContentNotFoundError(Exception):
    """
    Raised when a content file is not found.
    """
    pass