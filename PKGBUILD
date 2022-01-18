# Maintainer: Jacob Birkett <jacob@birkettdotdev>
# Contributor: ceyhunnabiyev for Breath color <https://github.com/ceyhunnabiyev>

# Maintainer: Stefano Capitani <stefanoatmanjarodotorg>
# Maintainer: NicoHood <archlinux {cat} nicohood {dog} de>
# Contributor: zach <zach {at} zach-adams {dot} com>
# Contributor: Gordian Edenhofer <gordian.edenhofer[at]yahoo[dot]de
# Contributor: Philipp Wolfer <ph.wolfer@gmail.com>

# This PKGBUILD provides Maia and Breath variant of Arc Theme

pkgbase=arc-themes-blackish-maia
pkgname=('arc-themes-solid-blackish-maia'
  'arc-themes-blackish-maia'
  'arc-themes-blackish-breath'
  'arc-themes-solid-blackish-breath')
_pkgname=arc-theme
pkgver=20220105
pkgrel=1
arch=('any')
# Upstream url: https://github.com/horst3180/arc-theme
# Now using soft fork: https://github.com/jnsh/arc-theme/issues/18
url="https://github.com/jnsh/arc-theme"
license=('GPL3')
optdepends=('arc-icon-theme: recommended icon theme'
  'gtk-engine-murrine: for gtk2 themes'
  'gnome-themes-standard: for gtk2 themes')
makedepends=('meson' 'sassc' 'inkscape')
options=('!strip')
source=("${pkgbase}-${pkgver}.tar.xz::${url}/releases/download/${pkgver}/${_pkgname}-${pkgver}.tar.xz")
sha256sums=('325ce5aedc6e1a67759e79a623308529d823f000f9d948ded2400ca0dae5520c')

# Latest stable Arch package versions
_cinnamonver=5.2
_gnomeshellver=41
_gtk4ver=4.6

# ALL arc color
_BLUE=5294E2
_BLUE3=4DADD4

# All Maia color variation
_maia=16A085
_maia3=16A674

# All Breath color variation
_breath=1abc9c
_breath3=1ccdaa

# All Blackish background color variation
_blackish_base=2A2A2A
_blackish_bg=252525

prepare() {
  cp -R "$_pkgname-$pkgver" "arc-themes-blackish-maia-$pkgver"
  cp -R "$_pkgname-$pkgver" "arc-themes-blackish-breath-$pkgver"
}

_build_arc-blackish-maia() {
  cd "$pkgbase-$pkgver"

  echo "Build arc-themes-blackish-maia"
  echo
  echo "Create arc-themes-blackish-maia: this next bit might take a little while..."
  echo
  echo "Create new name: *-Blackish-Maia"
  echo

  # Add Maia suffix (don't change this order)
  find . -type f -name '*.*' -exec sed -i \
    "s/Arc/Arc-Blackish-Maia/g;\
    s/Arc-Darker/Arc-Darker-Blackish-Maia/g;\
    s/Arc-Dark/Arc-Dark-Blackish-Maia/g" {} \;

  # Change the color Blue > Maia
  echo "Manjarification : Change all arc color to green maia"
  echo

  # override gtk2 schemas
  sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #16A085",' $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/light/gtkrc
  sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #16A085",' $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/light/gtkrc
  sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #16A085",' $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/dark/gtkrc
  sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #16A085",' $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/dark/gtkrc
  sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #16A085",' $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/darker/gtkrc
  sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #16A085",' $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/darker/gtkrc

  echo "Done override gtk2 schemas"
  echo
  echo "Change Hex format"
  echo

  # apply maia variation
  find . -type f -name '*.scss' -exec sed -i "s|$_BLUE|$_maia|Ig" {} \;

  echo "done1"
  echo

  find . -type f -name '*.scss' -exec sed -i "s|$_BLUE3|$_maia3|Ig" {} \;

  echo "done2"
  echo

  find . -type f -name '*.svg' -exec sed -i "s|$_BLUE|$_maia|Ig" {} \;

  echo "done3"
  echo

  echo "Rebuild png file: waiting"
  echo

  echo "Building blackish-maia-theme"
  echo

  meson --prefix=/usr build \
    -Dgnome_shell_gresource=true \
    -Dcinnamon_version="${_cinnamonver}" \
    -Dgnome_shell_version="${_gnomeshellver}" \
    -Dgtk4_version="${_gtk4ver}"
  meson compile -C build

  meson --prefix=/usr build-solid \
    -Dtransparency=false \
    -Dgnome_shell_gresource=true \
    -Dcinnamon_version="${_cinnamonver}" \
    -Dgnome_shell_version="${_gnomeshellver}" \
    -Dgtk4_version="${_gtk4ver}"
  meson compile -C build-solid
}

_build_arc-blackish-breath() {

  cd "$srcdir/arc-themes-blackish-breath-$pkgver"

  echo "Build arc-themes-blackish-breath"
  echo
  echo "Create arc-themes-blackish-breath: this next bit might take a little while..."
  echo
  echo "Create new name-blackish: *-Blackish-Breath"
  echo

  # Add Breath suffix (don't change this order)
  find . -type f -name '*.*' -exec sed -i \
    "s/Arc/Arc-Blackish-Breath/g;\
    s/Arc-Darker/Arc-Darker-Blackish-Breath/g;\
    s/Arc-Dark/Arc-Dark-Blackish-Breath/g" {} \;

  # Change the color Blue > Breath
  echo "Manjarification : Change all arc color to green breath"
  echo

  # override gtk2 schemas
  sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #1abc9c",' $srcdir/arc-themes-blackish-breath-$pkgver/common/gtk-2.0/light/gtkrc
  sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #1abc9c",' $srcdir/arc-themes-blackish-breath-$pkgver/common/gtk-2.0/light/gtkrc
  sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #1abc9c",' $srcdir/arc-themes-blackish-breath-$pkgver/common/gtk-2.0/dark/gtkrc
  sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #1abc9c",' $srcdir/arc-themes-blackish-breath-$pkgver/common/gtk-2.0/dark/gtkrc
  sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #1abc9c",' $srcdir/arc-themes-blackish-breath-$pkgver/common/gtk-2.0/darker/gtkrc
  sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #1abc9c",' $srcdir/arc-themes-blackish-breath-$pkgver/common/gtk-2.0/darker/gtkrc

  echo "Done override gtk2 schemas"
  echo
  echo "Change Hex format"
  echo

  # apply breath variation
  find . -type f -name '*.scss' -exec sed -i "s|$_BLUE|$_breath|Ig" {} \;

  echo "done1"
  echo

  find . -type f -name '*.scss' -exec sed -i "s|$_BLUE3|$_breath3|Ig" {} \;

  echo "done2"
  echo

  find . -type f -name '*.svg' -exec sed -i "s|$_BLUE|$_breath|Ig" {} \;

  echo "done3"
  echo

  echo "Rebuild png file: waiting"
  echo

  echo "Building blackish-breath-theme"
  echo

  meson --prefix=/usr build \
    -Dgnome_shell_gresource=true \
    -Dcinnamon_version="${_cinnamonver}" \
    -Dgnome_shell_version="${_gnomeshellver}" \
    -Dgtk4_version="${_gtk4ver}"
  meson compile -C build

  meson --prefix=/usr build-solid \
    -Dtransparency=false \
    -Dgnome_shell_gresource=true \
    -Dcinnamon_version="${_cinnamonver}" \
    -Dgnome_shell_version="${_gnomeshellver}" \
    -Dgtk4_version="${_gtk4ver}"
  meson compile -C build-solid
}

build() {
  _build_arc-blackish-maia
  _build_arc-blackish-breath
}

package_arc-themes-solid-blackish-maia() {
  pkgdesc="A flat theme without transparent elements and Blackish background Manjaro Maia variant"

  cd "$pkgbase-$pkgver"
  DESTDIR="$pkgdir" meson install -C build-solid

  # Change folder name for solid version

  # Add Maia-Solid suffix (don't change this order)
  find "$pkgdir/usr/share/themes" -type f -name '*.*' -exec sed -i \
    "s/Arc-Blackish-Maia/Arc-Blackish-Maia-Solid/g;\
    s/Arc-Darker-Blackish-Maia/Arc-Darker-Blackish-Maia-Solid/g;\
    s/Arc-Dark-Blackish-Maia/Arc-Dark-Blackish-Maia-Solid/g" {} \;
}

package_arc-themes-blackish-maia() {
  pkgdesc="A flat theme with transparent elements and Blackish background Manjaro Maia variant"

  cd "$pkgbase-$pkgver"
  DESTDIR="$pkgdir" meson install -C build
}

package_arc-themes-solid-blackish-breath() {
  pkgdesc="A flat theme without transparent elements and Blackish background Manjaro Breath variant"

  cd arc-themes-blackish-breath-$pkgver
  DESTDIR="$pkgdir" meson install -C build-solid

  # Change folder name for solid version

  # Add Breath-Solid suffix (don't change this order)
  find "$pkgdir/usr/share/themes" -type f -name '*.*' -exec sed -i \
    "s/Arc-Blackish-Breath/Arc-Blackish-Breath-Solid/g;\
    s/Arc-Darker-Blackish-Breath/Arc-Blackish-Darker-Breath-Solid/g;\
    s/Arc-Dark-Blackish-Breath/Arc-Blackish-Dark-Breath-Solid/g" {} \;
}

package_arc-themes-blackish-breath() {
  pkgdesc="A flat theme with transparent elements and Blackish background Manjaro Breath variant"

  cd arc-themes-blackish-breath-$pkgver
  DESTDIR="$pkgdir" meson install -C build
}
