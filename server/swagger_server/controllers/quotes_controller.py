from swagger_server.dependencies import dependency_resolver
from swagger_server.services.quotes_service import QuotesService 
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.quote import Quote  # noqa: E501
from swagger_server.models.quotes import Quotes  # noqa: E501
from swagger_server import util
import connexion


def quotes_random_get():  # noqa: E501
    """Get a random quote

     # noqa: E501


    :rtype: Quote
    """
    quotes_service: QuotesService = dependency_resolver.resolve(QuotesService)
    return quotes_service.get_random_quote()


def quotes_search_get(text=None):  # noqa: E501
    """Get a quote or quotes by quote&#x27;s part

     # noqa: E501

    :param text: Text to search quote(s) for
    :type text: str

    :rtype: Quotes
    """
    quptes_service: QuotesService = dependency_resolver.resolve(QuotesService)
    return quptes_service.find_quote(text)
