#!/bin/bash

rm -fr bin/django* bin/test* parts develop-eggs .installed.cfg
bin/buildout -vv buildout:install-from-cache=false
