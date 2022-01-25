#!/bin/bash
# Maintainer: Jacob Birkett <jacob@birkett.dev>
pkgbase='mojave-theme-maia'
pkgname=(
    "$pkgbase-light"
    "$pkgbase-light-solid"
    "$pkgbase-light-alt"
    "$pkgbase-light-alt-solid"
    "$pkgbase-dark"
    "$pkgbase-dark-solid"
    "$pkgbase-dark-alt"
    "$pkgbase-dark-alt-solid"
    "$pkgbase-blackish"
    "$pkgbase-blackish-solid"
    "$pkgbase-blackish-alt"
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

package_mojave-theme-maia-light() {
    cp "$srcdir/$pkgbase" "$srcdir/$pkgbase-light"
    cd "$srcdir/$pkgbase-light"
}

package_mojave-theme-maia-light-solid() {
    cp "$srcdir/$pkgbase" "$srcdir/$pkgbase-light-solid"
    cd "$srcdir/$pkgbase-light-solid"
}

package_mojave-theme-maia-light-alt() {
    cp "$srcdir/$pkgbase" "$srcdir/$pkgbase-light-alt"
    cd "$srcdir/$pkgbase-light-alt"
}

package_mojave-theme-maia-light-alt-solid() {
    cp "$srcdir/$pkgbase" "$srcdir/$pkgbase-light-alt-solid"
    cd "$srcdir/$pkgbase-light-alt-solid"
}

package_mojave-theme-maia-dark() {
    cp "$srcdir/$pkgbase" "$srcdir/$pkgbase-dark"
    cd "$srcdir/$pkgbase-dark"
}

package_mojave-theme-maia-dark-solid() {
    cp "$srcdir/$pkgbase" "$srcdir/$pkgbase-dark-solid"
    cd "$srcdir/$pkgbase-dark-solid"
}

package_mojave-theme-maia-dark-alt() {
    cp "$srcdir/$pkgbase" "$srcdir/$pkgbase-dark-alt"
    cd "$srcdir/$pkgbase-dark-alt"
}

package_mojave-theme-maia-dark-alt-solid() {
    cp "$srcdir/$pkgbase" "$srcdir/$pkgbase-dark-alt-solid"
    cd "$srcdir/$pkgbase-dark-alt-solid"
}

package_mojave-theme-maia-blackish() {
    cp "$srcdir/$pkgbase" "$srcdir/$pkgbase-blackish"
    cd "$srcdir/$pkgbase-blackish"
}

package_mojave-theme-maia-blackish-solid() {
    cp "$srcdir/$pkgbase" "$srcdir/$pkgbase-blackish-solid"
    cd "$srcdir/$pkgbase-blackish-solid"
}

package_mojave-theme-maia-blackish-alt() {
    cp "$srcdir/$pkgbase" "$srcdir/$pkgbase-blackish-alt"
    cd "$srcdir/$pkgbase-blackish-alt"
}

package_mojave-theme-maia-blackish-alt-solid() {
    cp "$srcdir/$pkgbase" "$srcdir/$pkgbase-blackish-alt-solid"
    cd "$srcdir/$pkgbase-blackish-alt-solid"
}
