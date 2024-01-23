.PHONY : docs
docs :
	rm -rf docs/build/
	sphinx-autobuild -b html --watch vk_url_scraper/ docs/source/ docs/build/

.PHONY : run-checks
run-checks :
	# do with --check to not change files
	# isort --check .
	# black --check .
	# do like this to fix files
	isort .
	black .
	flake8 .
	mypy .
	CUDA_VISIBLE_DEVICES='' pytest -v --color=yes .
