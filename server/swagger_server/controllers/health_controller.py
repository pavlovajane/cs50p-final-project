from http import HTTPStatus

def health_get():  # noqa: E501
    """Get a status of the API - 200 - OK or 500 - something is not working
     # noqa: E501
    :rtype: None
    """
    return HTTPStatus.OK