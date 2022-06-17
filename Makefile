.PHONY : docs
docs :
	rm -rf docs/build/
	sphinx-autobuild -b html --watch vk_url_scraper/ docs/source/ docs/build/

.PHONY : run-checks
run-checks :
	isort --check .
	black --check .
	flake8 .
	mypy .
	CUDA_VISIBLE_DEVICES='' pytest -v --color=yes --doctest-modules tests/ vk_url_scraper/
