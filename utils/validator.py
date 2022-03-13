from urllib.parse import urlparse

import validators


def is_valid_link(url: str) -> bool:
    """Check if a link (url) is valid, making sure that a proper protocol
    (e.g http or https) and domain exist.

    Args:
        url (string): The string to make the check on.

    Returns:
        bool: True if the link is valid, False otherwise.
    """
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https")


def check_procedures(url_to_crawl: str, max_workers: int) -> bool:
    """
        - Checks and validations before starting the crawler.
        - Print validations and useful information to guide user.

    Args:
        url_to_crawl (string): The url to scrap.
        max_workers (int): The maximum number of workers.
        console (Console): The console object.

    Extra:
        - Print check/validation errors to the console if they exist.

    Returns:
        bool: True if the checks passes
    """
    is_free_to_go = True

    if not validators.url(url_to_crawl):
        print(
            " [+] [ERROR] The supplied url is not a valid URL. URL validation spec: https://gist.github.com/dperini/729294"
        )
        print(" [+] [+] Supplied value: {}".format(url_to_crawl))
        is_free_to_go = False
    else:
        print("      ✅ URL is valid")

    if is_free_to_go:
        print(f"      ✅ As requested, {max_workers} workers could be used.")
    else:
        print("🚨 Please fix above errors and try again")

    return is_free_to_go
