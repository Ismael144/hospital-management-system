#!/usr/bin/bash

waitress-serve --listen=127.0.0.1:5000 hms:wsgi.application