#!/bin/bash
# Maintainer: Jacob Birkett <jacob@birkett.dev>
pkgbase='mojave-theme-maia'
pkgname=(
    'mojave-theme-maia-light'
    'mojave-theme-maia-light-alt'
    'mojave-theme-maia-dark'
    'mojave-theme-maia-dark-alt'
    'mojave-theme-maia-blackish'
    'mojave-theme-maia-blackish-alt'
)
pkgver=1
pkgrel=1
pkgdesc="A spin of vinceliuice's Mojave theme for GTK with Manjaro Maia colors and a darker variant."
arch=('any')
url="https://github.com/vinceliuice/Mojave-gtk-theme"
license=('GPL3')
depends=()
makedepends=('git' 'meson')
optdepends=()
source=("$pkgbase::git+https://github.com/vinceliuice/Mojave-gtk-theme.git")
md5sum=('SKIP')

pkgver() {
    cd "$pkgbase"
    printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

prepare() {
    cd "$pkgbase"
}

build() {
    cd "$pkgbase"
}

package() {
    cd "$pkgbase"
}
