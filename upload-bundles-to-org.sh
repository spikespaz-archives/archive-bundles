#! /usr/bin/env nix-shell
#! nix-shell -i bash -p gitFull gh
# shellcheck shell=bash
set -eu

bundles_dir="$(realpath $1)"
repo_owner="$2"

temp_dir='/tmp/clone-to-branch/'

for bundle_path in "$bundles_dir"/*.bundle; do
	bundle_name="$(basename "$bundle_path")"
	archive_name="${bundle_name%.bundle}"
	repo_name="${archive_name##*.}"
	repo_path="$temp_dir/$archive_name"
	git clone "$bundle_path" "$repo_path"
	pushd "$repo_path"
	git remote remove origin
	gh repo create "$repo_owner/$repo_name" --public --push --source .
	gh repo archive "$repo_owner/$repo_name" --yes
	popd
done

rm -rf "$temp_dir"
