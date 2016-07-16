#!/usr/bin/env sh

# Note that you should source this script rather than executing it, so it can 
# terminate your script if it finds uncommitted work.

# Make sure we're in a git repository.
if [ ! git rev-parse --show-toplevel &> /dev/null ]; then
    >&2 echo "Aborting: not in a git repository"
    exit 1
fi

# Make sure there aren't any uncommited changes.
if [ git ls-files --modified --deleted --others --exclude-standard &> /dev/null ]; then
    >&2 echo "Aborting: there are uncommitted changes in the working dir"
    >&2 git status
    exit 1
fi

# Log the current origin URL and commit hash.
git config --get remote.origin.url
git rev-parse HEAD
