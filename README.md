# vk-url-scraper
Library to scrape data and especially media links (videos and photos) from vk.com URLs.


# TODO
* docs online from sphinx

## Quick usage
`pip install vk-url-scraper` to install.


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

### Development
1. setup environment with `pip install -r requirements` or `pipenv install -r requirements`
2. To run all checks to `make run-checks` (fixes style) or individually
   1. To fix style: `black .` and `isort .` -> `flake8 .` to validate lint
   2. To do type checking: `mypy .`
   3. To test: `pytest .` (`pytest -v --color=yes --doctest-modules tests/ vk_url_scraper/` to user verbose, colors, and test docstring examples)
3. `make docs` to generate shpynx docs -> edit [config.py](docs/source/conf.py) if needed

### Releasing new version
1. edit [version.py](vk_url_scraper/version.py) with proper versioning
2. `git tag vx.y.z` to tag version
3. `git push origin vx.y.z` -> this will trigger workflow and put project on [pypi](https://pypi.org/project/vk-url-scraper/)