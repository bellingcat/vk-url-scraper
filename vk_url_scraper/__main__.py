import argparse
import json

from .scraper import VkScraper
from .utils import DateTimeEncoder


def get_argument_parser():
    """
    Creates the CMD line arguments. 'python vk_url_scraper.py --help'
    """
    parser = argparse.ArgumentParser(
        description="Authenticate and scrape information from vk.com based on a URL or set of URLs."
    )

    parser.add_argument(
        "-u",
        "--username",
        action="store",
        dest="username",
        required=True,
        help="username for a valid vk.com account",
    )
    parser.add_argument(
        "-p",
        "--password",
        action="store",
        dest="password",
        required=True,
        help="password for the valid vk.com account",
    )
    parser.add_argument(
        "-t",
        "--token",
        action="store",
        dest="token",
        required=False,
        help="optional token, when passed username/password authentication will not be done - good to avoid captcha issues",
    )
    parser.add_argument(
        "-d",
        "--download",
        action=argparse.BooleanOptionalAction,
        dest="download",
        help="if set then all photos and videos will be downloaded to folder output/",
    )
    parser.add_argument(
        "--urls",
        action="store",
        dest="urls",
        nargs=argparse.REMAINDER,
        required=True,
        help="must be the last argument: any text with one or more urls to scrape",
    )
    return parser


def main():
    parser = get_argument_parser()
    args = parser.parse_args()
    vks = VkScraper(args.username, args.password, args.token)
    text = " ".join(args.urls)
    res = vks.scrape(text)
    res_json = json.dumps(res, ensure_ascii=False, indent=4, cls=DateTimeEncoder)
    print(res_json)
    if args.download:
        vks.download_media(res)


if __name__ == "__main__":
    main()
