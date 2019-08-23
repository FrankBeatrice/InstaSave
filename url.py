import re
import sys
import requests


def clean(url):
    """Check if it's a link to a post and remove UTM code."""

    # Pattern that match a link to an Instagram post.
    pattern = "^http[s]?:\/\/www.instagram.com/p/[a-zA-Z0-9_-]{11}"
    match = re.match(pattern, url)
    # Shut down the program if the URL didn't match the pattern.
    if not match:
        sys.exit("Not a link to an Instagram post")
    # If the link had any UTM code, it's now removed.
    clean_url = match.group()

    return clean_url

def is_working(url):
    """Check if the URL is working."""

    try:
        r = requests.get(url)
    except requests.exceptions.MissingSchema:
        #raise SystemExit("Invalid URL.")
        sys.exit("Invalid URL")
    except requests.exceptions.ConnectionError:
        #raise SystemExit("Connection error!")
        sys.exit("Connection error")
    except requests.exceptions.Timeout:
        #raise SystemExit("Timeout.")
        sys.exit("Timeout")

    # If the request didn't return 200, it probably returned 404.
    # That could indicate that the link has been removed,
    # belongs to a private account or never existed.
    if r.status_code != 200:
        return False

    return True
