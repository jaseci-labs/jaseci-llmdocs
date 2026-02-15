#!/usr/bin/env bash
# Detects jaclang major.minor version changes and archives old release artifacts.
#
# Usage:
#   ./scripts/version_check.sh          # fetch version from GitHub
#   ./scripts/version_check.sh 0.11     # override version (for testing)
#
# On version change:
#   1. Moves jac-llmdocs.md + validation.json to release/<old_version>/
#   2. Updates release/VERSION to new version
#   3. Exits 0 (version changed) or 1 (no change)

set -euo pipefail

RELEASE_DIR="$(cd "$(dirname "$0")/../release" && pwd)"
VERSION_FILE="$RELEASE_DIR/VERSION"

# Get current stored version
if [ -f "$VERSION_FILE" ]; then
    current_version=$(tr -d '[:space:]' < "$VERSION_FILE")
else
    current_version=""
fi

# Get upstream jaclang version
if [ -n "${1:-}" ]; then
    upstream_full="$1"
else
    upstream_full=$(curl -sf https://raw.githubusercontent.com/jaseci-labs/jaseci/main/jac/pyproject.toml \
        | grep '^version' | head -1 | sed 's/.*"\(.*\)"/\1/')
    if [ -z "$upstream_full" ]; then
        echo "ERROR: Failed to fetch jaclang version" >&2
        exit 2
    fi
fi

# Extract major.minor
upstream_version=$(echo "$upstream_full" | cut -d. -f1,2)

echo "Current: ${current_version:-<none>}"
echo "Upstream: $upstream_version (full: $upstream_full)"

# No change
if [ "$current_version" = "$upstream_version" ]; then
    echo "No version change detected."
    exit 1
fi

# Version changed -- archive old artifacts
if [ -n "$current_version" ] && [ -f "$RELEASE_DIR/jac-llmdocs.md" ]; then
    archive_dir="$RELEASE_DIR/$current_version"
    mkdir -p "$archive_dir"
    cp "$RELEASE_DIR/jac-llmdocs.md" "$archive_dir/jac-llmdocs.md"
    [ -f "$RELEASE_DIR/jac-llmdocs.validation.json" ] && \
        cp "$RELEASE_DIR/jac-llmdocs.validation.json" "$archive_dir/jac-llmdocs.validation.json"
    echo "Archived release/$current_version/jac-llmdocs.md"
fi

# Update VERSION
echo "$upstream_version" > "$VERSION_FILE"
echo "Updated VERSION: $current_version -> $upstream_version"
exit 0
