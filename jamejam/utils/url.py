def prepare_urls(base_url: str, start: int, end: int) -> list:
    """Prepare urls for fetching data from the API.

    Args:
        base_url (str): Base url of the API.
        start (int): Start of the range of dynamic ids.
        end (int): End of the range of dynamic ids.

    Returns:
        list: List of urls to fetch data from.
    """
    dynamic_id_range = range(start, end)
    urls = [f"{base_url}{i}" for i in dynamic_id_range]
    return urls
