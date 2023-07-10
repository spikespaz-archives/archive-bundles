#! /usr/bin/env nix-shell
#! nix-shell -i bash -p gitFull
# shellcheck shell=bash
set -eu

bundles_dir="$(realpath $1)"
repo_url="$2"

temp_dir='/tmp/clone-to-branch/'

for bundle_path in "$bundles_dir"/*.bundle; do
	bundle_name="$(basename "$bundle_path")"
	archive_name="${bundle_name%.bundle}"
	repo_path="$temp_dir/$archive_name"
	git clone "$bundle_path" "$repo_path"
	cd "$repo_path"
	git switch -C "$archive_name"
	git remote add archives "$repo_url"
	git push --set-upstream archives "$repo_url"
done

rm -rf "$temp_dir"
