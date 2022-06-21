# vk-url-scraper
Library to scrape data and especially media links (videos and photos) from vk.com URLs.

You can use it via the [command line](#command-line-usage) or as a [python library](#python-library-usage).

## Installation
You can install the most recent release from [pypi](https://pypi.org/project/vk-url-scraper/) via `pip install vk-url-scraper`.

To use the library you will need a valid username/password combination for vk.com. 

## Command line usage
```bash
# run this to learn more about the parameters
vk_url_scraper --help

# scrape a URL and get the JSON result in the console
vk_url_scraper -username "username here" --password "password here" --urls https://vk.com/wall12345_6789
# OR
vk_url_scraper -u "username here" -p "password here" --urls https://vk.com/wall12345_6789
# you can also have multiple urls
vk_url_scraper -u "username here" -p "password here" --urls https://vk.com/wall12345_6789 https://vk.com/photo-12345_6789 https://vk.com/video12345_6789

# you can pass a token as well to avoid always authenticating 
# and possibly getting captch prompts
vk_url_scraper -u "username" -p "password" -t "vktoken goes here" --urls https://vk.com/wall12345_6789

# save the JSON output into a file
vk_url_scraper -u "username here" -p "password here" --urls https://vk.com/wall12345_6789 > output.json

# download any photos or videos found in these URLS
# this will use or create an output/ folder and dump the files there
vk_url_scraper -u "username here" -p "password here" --download --urls https://vk.com/wall12345_6789
# or
vk_url_scraper -u "username here" -p "password here" -d --urls https://vk.com/wall12345_6789
```

## Python library usage
```python
from vk_url_scraper import VkScraper

vks = VkScraper("username", "password")

# scrape any "photo" URL
res = vks.scrape("https://vk.com/photo1_278184324?rev=1")

# scrape any "wall" URL
res = vks.scrape("https://vk.com/wall-1_398461")

# scrape any "video" URL
res = vks.scrape("https://vk.com/video-6596301_145810025")
print(res[0]["text]) # eg: -> to get the text from code
```

```python
# Every scrape* function returns a list of dict like
{
	"id": "wall_id",
	"text": "text in this post" ,
	"datetime": utc datetime of post,
	"attachments": {
		# if photo, video, link exists
		"photo": [list of urls with max quality],
		"video": [list of urls with max quality],
		"link": [list of urls with max quality],
	},
	"payload": "original JSON response converted to dict which you can parse for more data
}
```

see [docs] for all available functions. 

### TODO
* scrape album links
* scrape profile links
* docs online from sphinx

## Development
(more info in [CONTRIBUTING.md](CONTRIBUTING.md)).

1. setup dev environment with `pip install -r dev-requirements.txt` or `pipenv install -r dev-requirements.txt`
1. setup environment with `pip install -r requirements.txt` or `pipenv install -r requirements.txt`
2. To run all checks to `make run-checks` (fixes style) or individually
   1. To fix style: `black .` and `isort .` -> `flake8 .` to validate lint
   2. To do type checking: `mypy .`
   3. To test: `pytest .` (`pytest -v --color=yes --doctest-modules tests/ vk_url_scraper/` to user verbose, colors, and test docstring examples)
3. `make docs` to generate shpynx docs -> edit [config.py](docs/source/conf.py) if needed

To test the command line interface available in [__main__.py](__vk_url_scraper/__main__.py) you need to pass the `-m` option to python like so: `python -m vk_url_scraper -u "" -p "" --urls ...`


## Releasing new version
1. edit [version.py](vk_url_scraper/version.py) with proper versioning
2. run `./scripts/release.sh` to create a tag and push, alternatively
   1. `git tag vx.y.z` to tag version
   2. `git push origin vx.y.z` -> this will trigger workflow and put project on [pypi](https://pypi.org/project/vk-url-scraper/)

### Fixing a failed release

If for some reason the GitHub Actions release workflow failed with an error that needs to be fixed, you'll have to delete both the tag and corresponding release from GitHub. After you've pushed a fix, delete the tag from your local clone with

```bash
git tag -l | xargs git tag -d && git fetch -t
```

Then repeat the steps above.