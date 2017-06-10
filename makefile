.PHONY: deploy update

# usage: make deploy m="commit message"
deploy:
	git pull --rebase
	git add .
	git commit -m "deploy: $(m)" --allow-empty
	git push
	make update

# Pushes the published folder to gh-pages to update the staging webpage.
update:
	git push origin `git subtree split --prefix viewer master`:gh-pages --force
	git subtree split --rejoin --prefix=viewer master
