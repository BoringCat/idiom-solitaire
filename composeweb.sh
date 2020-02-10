#!/bin/sh

html-minifier --collapse-whitespace --remove-comments --remove-optional-tags --remove-redundant-attributes --remove-script-type-attributes --remove-tag-whitespace --use-short-doctype --minify-css true --minify-js true --minify-urls true index.html -o web.min/index.html
uglifyjs script.js -o web.min/script.js
