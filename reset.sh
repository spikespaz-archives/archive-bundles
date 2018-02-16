#!/bin/sh

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Removing work directory..."
rm -rf "${BASE_DIR}/work"
echo "Removing deploy directory..."
rm -rf "${BASE_DIR}/deploy"
echo "Removing stage SKIP files..."
rm "${BASE_DIR}/*/SKIP"
