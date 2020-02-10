#!/bin/sh

html-minifier\
    --collapse-whitespace\
    --remove-comments\
    --remove-optional-tags\
    --remove-redundant-attributes\
    --remove-script-type-attributes\
    --remove-tag-whitespace\
    --use-short-doctype\
    --minify-css true\
    --minify-js true\
    --minify-urls true index.html -o web.min/index.html
cp script.js style.css github.svg web.min
sed -i 's/> />/g;
s/ </</g;
s/disabled="disabled"/disabled/g;
s/id="connecting"/id="ci"/g;
s/id="disconnect"/id="dc"/g;
s/id="isconnect"/id="ic"/g;
s/id="connect"/id="c"/g;
s/id="mode"/id="m"/g;
s/id="submit"/id="s"/g;
s/id="idiom"/id="i"/g;
s/id="list"/id="l"/g;
s/id="length"/id="le"/g;
s/<\/button><\/div><\/div><\/div>$//;
' web.min/index.html

sed -i 's/#disconnect/#dc/g;
s/#connecting/#ci/g;
s/#isconnect/#ic/g;
s/#connect/#c/g;
s/#mode/#m/g;
s/#submit/#s/g;
s/#idiom/#i/g;
s/#list/#l/g;
s/#length/#le/g;
' web.min/script.js