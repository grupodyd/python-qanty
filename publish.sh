#!/usr/bin/env bash
set -euo pipefail

if [[ -n "$(git status --porcelain)" ]]; then
    echo "Error: working tree is dirty — commit or stash changes first" >&2
    exit 1
fi

LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
if [[ -z "$LAST_TAG" ]]; then
    COMMITS=$(git log --format="%s%n%b")
else
    COMMITS=$(git log "${LAST_TAG}..HEAD" --format="%s%n%b")
fi

if [[ -z "$COMMITS" ]]; then
    echo "Error: no commits since last release ($LAST_TAG)" >&2
    exit 1
fi

BUMP="patch"
while IFS= read -r line; do
    if echo "$line" | grep -qiE "BREAKING[[:space:]]CHANGE|^[a-z]+(\([^)]+\))?!:"; then
        BUMP="major"
        break
    elif echo "$line" | grep -qiE "^feat(\([^)]+\))?:"; then
        [[ "$BUMP" != "major" ]] && BUMP="minor"
    fi
done <<< "$COMMITS"

echo "Commits since ${LAST_TAG:-beginning}:"
if [[ -z "$LAST_TAG" ]]; then
    git log --oneline
else
    git log "${LAST_TAG}..HEAD" --oneline
fi
echo ""
echo "Detected bump: $BUMP"

CURRENT=$(grep 'current_version' .bumpversion.cfg | awk -F' = ' '{print $2}')
echo "Current version: $CURRENT"
echo ""
read -rp "Proceed? [y/N] " CONFIRM
[[ "${CONFIRM,,}" == "y" ]] || { echo "Aborted."; exit 0; }

./venv/bin/bumpversion "$BUMP"

NEW_VERSION=$(grep 'current_version' .bumpversion.cfg | awk -F' = ' '{print $2}')
TAG="v${NEW_VERSION}"

git add setup.py qanty/version.py .bumpversion.cfg
git commit -m "RELEASE ${NEW_VERSION}"
git tag "$TAG"
git push origin main
git push origin "$TAG"

echo ""
echo "Tag $TAG pushed. Go to GitHub and publish the release to trigger PyPI upload."
