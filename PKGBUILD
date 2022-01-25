#!/bin/bash
# Maintainer: Jacob Birkett <jacob@birkett.dev>
pkgbase='mojave-theme-maia'
pkgname=(
    "$pkgbase-light"
    "$pkgbase-dark"
    "$pkgbase-blackish"
    "$pkgbase-light-alt"
    "$pkgbase-dark-alt"
    "$pkgbase-blackish-alt"
    "$pkgbase-light-solid"
    "$pkgbase-dark-solid"
    "$pkgbase-blackish-solid"
    "$pkgbase-light-alt-solid"
    "$pkgbase-dark-alt-solid"
    "$pkgbase-blackish-alt-solid"
)
pkgver=1
pkgrel=1
pkgdesc="A spin of vinceliuice's Mojave theme for GTK with Manjaro Maia colors and a darker variant."
arch=('any')
url='https://github.com/vinceliuice/Mojave-gtk-theme'
license=('GPL3')
depends=()
makedepends=('git' 'meson')
optdepends=(
    'mcmojave-cursors: matching cursor theme'
    'mcmojave-circle-icon-theme: matching icon theme'
)
source=("$pkgbase::git+https://github.com/vinceliuice/Mojave-gtk-theme.git")
md5sum=('SKIP')

pkgver() {
    cd "$srcdir/$pkgbase"
    printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

prepare() {
    cd "$srcdir/$pkgbase"
}

build() {
    cd "$srcdir/$pkgbase"
}

package() {
    cd "$srcdir/$pkgbase"
}
