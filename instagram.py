import json
import random
import requests
from datetime import datetime
from bs4 import BeautifulSoup


def random_user_agent():
    """Read in all possible user agents from a file and pick one."""

    filename = "useragents.txt"

    with open(filename, 'r') as f:
        # Read the file and split it's lines into a list of user agents.
        lines = f.read().splitlines()
        # Randomly pick one user agent from the list.
        user_agent = random.choice(lines)

    f.close()

    return user_agent


class PostScraper:

    def __init__(self):
        self.headers = {"User-Agent": random_user_agent()}

    def download(self, url):
        """Download files to disk."""

        data = self._get_post_data(url)
        post_urls = data[0]
        post_type = data[1]

        # Post with a video file.
        if post_type == "GraphVideo":
            self._download_file(post_urls)
        # Post with a image file.
        elif post_type == "GraphImage":
            self._download_file(post_urls)
        # Post with multiple files, either images and/or videos.
        elif post_type == "GraphSidecar":
            for url in post_urls:
                self._download_file(url)

    def _get_post_data(self, url):
        """Returns the file URLs and the post type."""

        # Get the page's HTML code and parse it with BeautifulSoup to find the type
        # of the post.
        html = requests.get(url, headers=self.headers).text
        soup = BeautifulSoup(html, 'html.parser')
        data = json.loads(soup.select("script[type='text/javascript']")[3].text[21:-1])
        post_type = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["__typename"]

        # Post with a video file.
        if post_type == "GraphVideo":
            image_url = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["video_url"]
        # Post with a image file.
        elif post_type == "GraphImage":
            image_url = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["display_url"]
        # Post with multiple files, either images and/or videos.
        elif post_type == "GraphSidecar":
            edges = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"]
            # Differentiate between images and videos in multi-content posts.
            # Get urls with .jpg for images and .mp4 for videos.
            image_url = [edge["node"]["video_url"] if edge["node"]["__typename"] == "GraphVideo" else edge["node"]["display_url"] for edge in edges]

        return image_url, post_type

    def _download_file(self, url):
        """Get the content from the url, pick a name for the file and save it."""

        r = requests.get(url, headers=self.headers)
        filename = self._pick_filename(r.headers)
        self._save(r.content, filename)

    def _pick_filename(self, headers):
        """Give the file a unique name."""

        # Get the date the post was uploaded.
        d = datetime.strptime(headers.get('last-modified'), "%a, %d %b %Y %H:%M:%S %Z")
        # Format the date and time and use it in the filename.
        filename = d.strftime("%Y%m%d_%H%M%S_")
        # Add a unique string to the filename to prevent conflicting names.
        filename += headers.get('x-enc-origin-req-handler')
        # Add file extension based on the contents type.
        if headers.get('content-type') == "video/mp4":
            filename += ".mp4"
        else:
            filename += ".jpg"

        return filename

    def _save(self, content, filename):
        """Write content to file."""

        with open(filename, 'wb') as f:
            f.write(content)
        f.close()
