import requests


class BookPageError(requests.HTTPError):
    """Raised when the page with book ID cannot be found"""
    pass


class DownloadBookError(requests.HTTPError):
    """Raised when there is no download link for book"""
    pass


class CategoryPageError(requests.HTTPError):
    """Raised when the paginaton page in category cannot be found"""
    pass