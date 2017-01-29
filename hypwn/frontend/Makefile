$(shell pwd > ~/mkdir.log ; mkdir -pv dist dist/js dist/css libs/js >> ~/mkdir.log)

.PHONY: all html js css

all: html js css

html: html/index.html
	cp -v $^ dist/

js: $(shell find js -type f | xargs) libs/js/jquery.js
	cat libs/js/* js/main.js > dist/js/hypwn.js

css: $(shell find css -type f | xargs)
	cat css/* > dist/css/hypwn.css

libs/js/jquery.js:
	curl https://code.jquery.com/jquery-3.1.1.js > $@
