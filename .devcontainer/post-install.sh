#!/bin/bash
set -ex

# Git configuration
git config --global --add safe.directory /workspaces/sfmc_scraper
git config --global user.name "Paweł Grabiński" 
git config --global user.email "pawelrgrabinski@gmail.com"
git config --global core.editor "code --wait"
