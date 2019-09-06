import uuid
from hashlib import blake2b


def start_at_shortcode_media(func):
    """Return dict with direct access to the shortcode_media key."""

    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        # Return data from this position in the dict.
        return data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]

    return wrapper


def unique_filename(func):
    """Return filename with an unique id appended to it's end."""

    def wrapper(*args, **kwargs):
        filename = func(*args, **kwargs)
        # Convert the random UUID to bytes.
        id = str.encode(str(uuid.uuid4()))
        # Convert the id to a 10 character long string.
        hash = blake2b(digest_size=10, key=id).hexdigest()
        # Separate the file extension from the name.
        filename = [filename[:-4], filename[-3:]]
        # Append the hash at the end of the name.
        filename[0] += "_" + hash
        # Merge the name and the file extension.
        filename = ".".join(filename)
        return filename

    return wrapper
