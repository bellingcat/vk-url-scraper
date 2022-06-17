import re
from collections import defaultdict
from datetime import datetime
from typing import List

import requests
import vk_api  # used to get api_token after authentication


class VkScraper:
    """VkScraper class that allows to authenticate and scrape URLs.

    All `scrape*` functions return a payload like:

    .. highlight:: python
    .. code-block:: python

        {
            "id": "wall_id",
            "text": "text in this post" ,
            "datetime": datetime of post,
            "attachments": {
                # only present values will appear, can be empty dict
                "photo": [list of urls with max quality],
                "video": [list of urls with max quality],
                "link": [list of urls with max quality],
            },
            "payload": {"more": "original JSON response as dict which you can parse for more data"}
        }
    """
    WALL_PATTERN = re.compile(r"(wall.{0,1}\d+_\d+)")
    PHOTO_PATTERN = re.compile(r"(photo.{0,1}\d+_\d+)")
    VIDEO_PATTERN = re.compile(r"(video.{0,1}\d+_\d+)")

    def __init__(self, username: str, password: str) -> None:
        """Initializes the scraper.

        This function receives a username and password and performs authentication on vk.com to then call api endpoints

        Parameters
        ----------
        username : str
            Username on vk.com, can be a phone number or email
        password : str
            Matching password on vk.com
        """
        self.session = vk_api.VkApi(username, password)
        self.session.auth(token_only=True)

    def scrape(self, url: str) -> List:
        """Scrapes a URL for multiple possibilities of inner links such as wall, video, photo, ...

        Parameters
        ----------
        url : str
            The URL to parse and analyze content from, typically shared from vk.com feature
            or copy-pasted from the browser

        Returns
        -------
        a list of dict as specified in the class documentation.
        """
        return self.scrape_walls(url) + self.scrape_photos(url) + self.scrape_videos(url)

    def scrape_walls(self, url: str) -> List:
        """Scrapes a URL for multiple wall data

        Parameters
        ----------
        url : str
            The URL to parse - should contain something like "...wall1212_3434..."

        Returns
        -------
        a list of dict as specified in the class documentation.
        """
        wall_ids = self.WALL_PATTERN.findall(url)
        return self.scrape_wall_ids(wall_ids)

    def scrape_wall_ids(self, wall_ids: List[str], copy_history_depth: int = 2) -> List[dict]:
        """
        Receives a list of wall ids like wall123123_1231 see `api docs <https://dev.vk.com/method/wall.getById>`__

        Parameters
        ----------
        wall_ids : List[str]
            list with valid wall ids like "wall123123_1231"
        copy_history_depth : int
            see `api docs <https://dev.vk.com/method/wall.getById>`__

        Returns
        -------
        a list of dict as specified in the class documentation.
        """
        if not len(wall_ids):
            return []
        wall_ids = [wall_id.replace("wall", "") for wall_id in wall_ids]
        # docs: https://dev.vk.com/method/wall.getById
        headers = {
            "access_token": self.session.token["access_token"],
            "posts": ",".join(wall_ids),
            "extended": "1",
            "copy_history_depth": str(copy_history_depth),
            "v": self.session.api_version,
        }
        req = requests.get("https://api.vk.com/method/wall.getById", headers)
        api_res = req.json()
        res = []
        for item in api_res.get("response", {}).get("items", []):
            attachments_json = item.get("attachments", []) + sum(
                [x.get("attachments", []) for x in item.get("copy_history", [])], []
            )
            attachments = defaultdict(list)
            for a in attachments_json:
                try:
                    first_type = a["type"]
                    attachment = a[first_type]
                    if first_type == "video":
                        attachments["video"].extend(
                            self.scrape_videos(f'video{attachment["owner_id"]}_{attachment["id"]}')[
                                0
                            ]
                            .get("attachments", {})
                            .get("video", [""])
                        )
                        continue
                    if first_type == "link":
                        attachments["link"].append(attachment["url"])
                        if "photo" in attachment:
                            attachment = attachment["photo"]
                            first_type = "photo"
                        elif "video" in attachment:
                            attachment = attachment["video"]
                            attachments["video"].extend(
                                self.scrape_videos(
                                    f'video{attachment["owner_id"]}_{attachment["id"]}'
                                )[0]
                                .get("attachments", {})
                                .get("video", [""])
                            )
                            continue
                        else:
                            continue

                    if "thumb" in attachment:
                        attachment = attachment["thumb"]
                    if "sizes" in attachment:
                        try:
                            attachments[first_type].append(attachment["sizes"][-1]["url"])
                        except Exception as e:
                            print(f"could not get image from attachment: {e}")
                except Exception as e:
                    print(f"Unexpected error in attachment={a}: {e}")

            res.append(
                {
                    "id": f'wall{item["owner_id"]}_{item["id"]}',
                    "text": item.get("text", ""),
                    "datetime": datetime.utcfromtimestamp(item.get("date", 0)),
                    "attachments": dict(attachments),
                    "payload": item,
                }
            )
        return res

    def scrape_videos(self, url: str) -> List[dict]:
        """Scrapes a URL for multiple video data

        Parameters
        ----------
        url : str
            The URL to parse - should contain something like "...video1212_3434..."

        Returns
        -------
        a list of dict as specified in the class documentation.
        """
        video_ids = self.VIDEO_PATTERN.findall(url)
        return self.scrape_video_ids(video_ids)

    def scrape_video_ids(self, video_ids: List[str]) -> List[dict]:
        """
        Receives a list of video ids like video123123_1231 see `api docs <https://dev.vk.com/method/video.get>`__

        Parameters
        ----------
        video_ids : List[str]
            list with valid video ids like "video123123_1231"
            
        Returns
        -------
        a list of dict as specified in the class documentation.
        """
        if not len(video_ids):
            return []
        video_ids = [video_id.replace("video", "") for video_id in video_ids]

        headers = {
            "access_token": self.session.token["access_token"],
            "videos": ",".join(video_ids),
            "extended": "1",
            "v": self.session.api_version,
        }
        req = requests.get("https://api.vk.com/method/video.get", headers)

        api_res = req.json()
        res = []
        for item in api_res.get("response", {}).get("items", []):
            res.append(
                {
                    "id": f'video{item["owner_id"]}_{item["id"]}',
                    "text": item.get("title", ""),
                    "datetime": datetime.utcfromtimestamp(item.get("date", 0)),
                    "attachments": {
                        "video": [item.get("player", "")],
                    },
                    "payload": item,
                }
            )
        return res

    def scrape_photos(self, url: str) -> List[dict]:
        """Scrapes a URL for multiple photo data

        Parameters
        ----------
        url : str
            The URL to parse - should contain something like "...photo1212_3434..."

        Returns
        -------
        a list of dict as specified in the class documentation.
        """
        photo_ids = self.PHOTO_PATTERN.findall(url)
        return self.scrape_photo_ids(photo_ids)

    def scrape_photo_ids(self, photo_ids: List[str]) -> List[dict]:
        """
        Receives a list of photo ids like photo123123_1231 see `api docs <https://dev.vk.com/method/photos.getById>`__

        Parameters
        ----------
        photo_ids : List[str]
            list with valid photo ids like "photo123123_1231"
            
        Returns
        -------
        a list of dict as specified in the class documentation.
        """
        if not len(photo_ids):
            return []
        photo_ids = [photo_id.replace("photo", "") for photo_id in photo_ids]

        headers = {
            "access_token": self.session.token["access_token"],
            "photos": ",".join(photo_ids),
            "extended": "1",
            "v": self.session.api_version,
        }
        req = requests.get("https://api.vk.com/method/photos.getById", headers)

        api_res = req.json()
        res = []
        for item in api_res.get("response", []):
            res.append(
                {
                    "id": f'photo{item["owner_id"]}_{item["id"]}',
                    "text": item.get("text", ""),
                    "datetime": datetime.utcfromtimestamp(item.get("date", 0)),
                    "attachments": {"photo": [item["orig_photo"]["url"]]},
                    "payload": item,
                }
            )
        return res
