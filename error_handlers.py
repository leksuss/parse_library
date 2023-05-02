import requests


class BookPageError(requests.HTTPError):
    """Raised when the page with book ID cannot be found"""
    pass


class DownloadBookError(requests.HTTPError):
    """Raised when there is no download link for book"""
    pass


class ChapterPageError(requests.HTTPError):
    """Raised when the paginaton page in chapter cannot be found"""
    pass