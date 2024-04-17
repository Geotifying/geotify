Contributing
!! Contribute to Geotify !! With your help, geotify can grow further.

Geotify defines the following convention for cleaner maintenance.

In general, Geotify is built on top of the folium project.

When submitting a pull request :

All existing tests should pass. Please make sure that the test suite passes, both locally and on GitHub Actions. Status on GHA will be visible on a pull request. GHA are automatically enabled on your own fork as well. To trigger a check, make a PR to your own fork.

New features must be tested and pass pull requests.

make sure it contains a note describing the changes in the CHANGELOG.md file.

Geotify supports Python 3.9+.

Code Convention
Please follows isort, black, flake8, mypy for contribute.
Everybody can set up [pre-commit hooks] to automatically by installing 'pre-commit': $ python -m pip install pre-commit
From the root of the Geotify repository, you should then install pre-commit:

$ pre-commit install
Commit Convention
The message type is basically written in lowercase letters as shown below.

feat: Add new features
fix: bug fix
docs: Change document content
style: Formatting, missing semicolons, no code changes, etc.
refactor : code refactoring
test: Write test code
chore: Build modifications, package manager settings, no operational code changes, etc.
Subject must not use periods or special symbols. And you shouldn't use the past tense either. The body should be written in as much detail as possible and clearly explain what was done and why.
