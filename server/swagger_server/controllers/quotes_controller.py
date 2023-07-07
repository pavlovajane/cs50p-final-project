import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.quote import Quote  # noqa: E501
from swagger_server.models.quotes import Quotes  # noqa: E501
from swagger_server import util


def quotes_random_get():  # noqa: E501
    """Get a random quote

     # noqa: E501


    :rtype: Quote
    """
    return 'do some magic!'


def quotes_search_get(text=None):  # noqa: E501
    """Get a quote or quotes by quote&#x27;s part

     # noqa: E501

    :param text: Text to search quote(s) for
    :type text: str

    :rtype: Quotes
    """
    return 'do some magic!'
