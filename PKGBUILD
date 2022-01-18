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
  # 'arc-themes-blackish-breath'
  # 'arc-themes-solid-blackish-breath'
)
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
_BASE=404552
_BG=383C4A
_HEADER_BG=2F343F
_TOOLTIP_BG=4B5162
_INSENSITIVE_BG=3E4350
_DARK_SIDEBAR_BG=353945

# All Maia color variation
_maia=16A085
_maia3=16A674

# # All Breath color variation
# _breath=1abc9c
# _breath3=1ccdaa

# All Blackish background color variation
_blackish_base=2A2A2A
_blackish_bg=252525
_blackish_header_bg=2A2A2A
_blackish_tooltip_bg=363636
_blackish_insensitive_bg=2f2f2f
_blackish_dark_sidebar_bg=252525

prepare() {
  cp -R "$_pkgname-$pkgver" "arc-themes-blackish-maia-$pkgver"
  # cp -R "$_pkgname-$pkgver" "arc-themes-blackish-breath-$pkgver"
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

  echo "Override GTK2 schemas"
  echo

  sed -i -e "s,.*gtk-color-scheme = \"selected_bg_color: #$_BLUE\".*,gtk-color-scheme = \"selected_bg_color: #$_maia\",I" $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/light/gtkrc
  sed -i -e "s,.*gtk-color-scheme = \"link_color: #$_BLUE\".*,gtk-color-scheme = \"link_color: #$_maia\",I" $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/light/gtkrc
  sed -i -e "s,.*gtk-color-scheme = \"selected_bg_color: #$_BLUE\".*,gtk-color-scheme = \"selected_bg_color: #$_maia\",I" $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/dark/gtkrc
  sed -i -e "s,.*gtk-color-scheme = \"link_color: #$_BLUE\".*,gtk-color-scheme = \"link_color: #$_maia\",I" $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/dark/gtkrc
  sed -i -e "s,.*gtk-color-scheme = \"selected_bg_color: #$_BLUE\".*,gtk-color-scheme = \"selected_bg_color: #$_maia\",I" $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/darker/gtkrc
  sed -i -e "s,.*gtk-color-scheme = \"link_color: #$_BLUE\".*,gtk-color-scheme = \"link_color: #$_maia\",I" $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/darker/gtkrc

  echo "done1"
  echo

  sed -i -e "s,.*gtk-color-scheme = \"base_color: #$_BASE\".*,gtk-color-scheme = \"base_color: #$_blackish_base\",I" $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/light/gtkrc
  sed -i -e "s,.*gtk-color-scheme = \"notebook_bg: #$_BASE\".*,gtk-color-scheme = \"notebook_bg: #$_blackish_base\",I" $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/light/gtkrc
  sed -i -e "s,.*gtk-color-scheme = \"base_color: #$_BASE\".*,gtk-color-scheme = \"base_color: #$_blackish_base\",I" $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/dark/gtkrc
  sed -i -e "s,.*gtk-color-scheme = \"notebook_bg: #$_BASE\".*,gtk-color-scheme = \"notebook_bg: #$_blackish_base\",I" $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/dark/gtkrc
  sed -i -e "s,.*gtk-color-scheme = \"base_color: #$_BASE\".*,gtk-color-scheme = \"base_color: #$_blackish_base\",I" $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/darker/gtkrc
  sed -i -e "s,.*gtk-color-scheme = \"notebook_bg: #$_BASE\".*,gtk-color-scheme = \"notebook_bg: #$_blackish_base\",I" $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/darker/gtkrc

  echo "done2"
  echo

  sed -i -e "s,.*gtk-color-scheme = \"bg_color: #$_BG\".*,gtk-color-scheme = \"bg_color: #$_blackish_bg\",I" $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/light/gtkrc
  sed -i -e "s,.*gtk-color-scheme = \"menu_bg: #$_BG\".*,gtk-color-scheme = \"menu_bg: #$_blackish_bg\",I" $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/light/gtkrc
  sed -i -e "s,.*gtk-color-scheme = \"bg_color: #$_BG\".*,gtk-color-scheme = \"bg_color: #$_blackish_bg\",I" $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/dark/gtkrc
  sed -i -e "s,.*gtk-color-scheme = \"menu_bg: #$_BG\".*,gtk-color-scheme = \"menu_bg: #$_blackish_bg\",I" $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/dark/gtkrc
  sed -i -e "s,.*gtk-color-scheme = \"bg_color: #$_BG\".*,gtk-color-scheme = \"bg_color: #$_blackish_bg\",I" $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/darker/gtkrc
  sed -i -e "s,.*gtk-color-scheme = \"menu_bg: #$_BG\".*,gtk-color-scheme = \"menu_bg: #$_blackish_bg\",I" $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/darker/gtkrc

  echo "done3"
  echo

  sed -i -e "s,.*gtk-color-scheme = \"tooltip_bg_color: #$_TOOLTIP_BG\".*,gtk-color-scheme = \"tooltip_bg_color: #$_blackish_tooltip_bg\",I" $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/light/gtkrc
  sed -i -e "s,.*gtk-color-scheme = \"tooltip_bg_color: #$_TOOLTIP_BG\".*,gtk-color-scheme = \"tooltip_bg_color: #$_blackish_tooltip_bg\",I" $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/dark/gtkrc
  sed -i -e "s,.*gtk-color-scheme = \"tooltip_bg_color: #$_TOOLTIP_BG\".*,gtk-color-scheme = \"tooltip_bg_color: #$_blackish_tooltip_bg\",I" $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/darker/gtkrc

  echo "done4"
  echo

  sed -i -e "s,.*gtk-color-scheme = \"dark_sidebar_bg: #$_DARK_SIDEBAR_BG\".*,gtk-color-scheme = \"dark_sidebar_bg: #$_blackish_dark_sidebar_bg\",I" $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/light/gtkrc
  sed -i -e "s,.*gtk-color-scheme = \"dark_sidebar_bg: #$_DARK_SIDEBAR_BG\".*,gtk-color-scheme = \"dark_sidebar_bg: #$_blackish_dark_sidebar_bg\",I" $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/dark/gtkrc
  sed -i -e "s,.*gtk-color-scheme = \"dark_sidebar_bg: #$_DARK_SIDEBAR_BG\".*,gtk-color-scheme = \"dark_sidebar_bg: #$_blackish_dark_sidebar_bg\",I" $srcdir/arc-themes-blackish-maia-$pkgver/common/gtk-2.0/darker/gtkrc

  echo "done5"
  echo

  echo "Done override GTK2 schemas"
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

  # apply blackish variation
  find . -type f -name '*.scss' -exec sed -i "s|$_BASE|$_blackish_base|Ig" {} \;

  echo "done4"
  echo

  find . -type f -name '*.scss' -exec sed -i "s|$_BG|$_blackish_bg|Ig" {} \;

  echo "done5"
  echo

  find . -type f -name '*.scss' -exec sed -i "s|$_HEADER_BG|$_blackish_header_bg|Ig" {} \;

  echo "done6"
  echo

  find . -type f -name '*.scss' -exec sed -i "s|$_TOOLTIP_BG|$_blackish_tooltip_bg|Ig" {} \;

  echo "done7"
  echo

  find . -type f -name '*.scss' -exec sed -i "s|$_INSENSITIVE_BG|$_blackish_insensitive_bg|Ig" {} \;

  echo "done8"
  echo

  find . -type f -name '*.scss' -exec sed -i "s|$_DARK_SIDEBAR_BG|$_blackish_dark_sidebar_bg|Ig" {} \;

  echo "done9"
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

# _build_arc-blackish-breath() {

#   cd "$srcdir/arc-themes-blackish-breath-$pkgver"

#   echo "Build arc-themes-blackish-breath"
#   echo
#   echo "Create arc-themes-blackish-breath: this next bit might take a little while..."
#   echo
#   echo "Create new name-blackish: *-Blackish-Breath"
#   echo

#   # Add Breath suffix (don't change this order)
#   find . -type f -name '*.*' -exec sed -i \
#     "s/Arc/Arc-Blackish-Breath/g;\
#     s/Arc-Darker/Arc-Darker-Blackish-Breath/g;\
#     s/Arc-Dark/Arc-Dark-Blackish-Breath/g" {} \;

#   # Change the color Blue > Breath
#   echo "Manjarification : Change all arc color to green breath"
#   echo

#   # override gtk2 schemas
#   sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #1abc9c",' $srcdir/arc-themes-blackish-breath-$pkgver/common/gtk-2.0/light/gtkrc
#   sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #1abc9c",' $srcdir/arc-themes-blackish-breath-$pkgver/common/gtk-2.0/light/gtkrc
#   sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #1abc9c",' $srcdir/arc-themes-blackish-breath-$pkgver/common/gtk-2.0/dark/gtkrc
#   sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #1abc9c",' $srcdir/arc-themes-blackish-breath-$pkgver/common/gtk-2.0/dark/gtkrc
#   sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #1abc9c",' $srcdir/arc-themes-blackish-breath-$pkgver/common/gtk-2.0/darker/gtkrc
#   sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #1abc9c",' $srcdir/arc-themes-blackish-breath-$pkgver/common/gtk-2.0/darker/gtkrc

#   echo "Done override gtk2 schemas"
#   echo
#   echo "Change Hex format"
#   echo

#   # apply breath variation
#   find . -type f -name '*.scss' -exec sed -i "s|$_BLUE|$_breath|Ig" {} \;

#   echo "done1"
#   echo

#   find . -type f -name '*.scss' -exec sed -i "s|$_BLUE3|$_breath3|Ig" {} \;

#   echo "done2"
#   echo

#   find . -type f -name '*.svg' -exec sed -i "s|$_BLUE|$_breath|Ig" {} \;

#   echo "done3"
#   echo

#   # apply blackish variation
#   find . -type f -name '*.scss' -exec sed -i "s|$_BASE|$_blackish_base|Ig" {} \;

#   echo "done4"
#   echo

#   find . -type f -name '*.scss' -exec sed -i "s|$_BG|$_blackish_bg|Ig" {} \;

#   echo "done5"
#   echo

#   echo "Rebuild png file: waiting"
#   echo

#   echo "Building blackish-breath-theme"
#   echo

#   meson --prefix=/usr build \
#     -Dgnome_shell_gresource=true \
#     -Dcinnamon_version="${_cinnamonver}" \
#     -Dgnome_shell_version="${_gnomeshellver}" \
#     -Dgtk4_version="${_gtk4ver}"
#   meson compile -C build

#   meson --prefix=/usr build-solid \
#     -Dtransparency=false \
#     -Dgnome_shell_gresource=true \
#     -Dcinnamon_version="${_cinnamonver}" \
#     -Dgnome_shell_version="${_gnomeshellver}" \
#     -Dgtk4_version="${_gtk4ver}"
#   meson compile -C build-solid
# }

build() {
  _build_arc-blackish-maia
  # _build_arc-blackish-breath
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

# package_arc-themes-solid-blackish-breath() {
#   pkgdesc="A flat theme without transparent elements and Blackish background Manjaro Breath variant"

#   cd arc-themes-blackish-breath-$pkgver
#   DESTDIR="$pkgdir" meson install -C build-solid

#   # Change folder name for solid version

#   # Add Breath-Solid suffix (don't change this order)
#   find "$pkgdir/usr/share/themes" -type f -name '*.*' -exec sed -i \
#     "s/Arc-Blackish-Breath/Arc-Blackish-Breath-Solid/g;\
#     s/Arc-Darker-Blackish-Breath/Arc-Blackish-Darker-Breath-Solid/g;\
#     s/Arc-Dark-Blackish-Breath/Arc-Blackish-Dark-Breath-Solid/g" {} \;
# }

# package_arc-themes-blackish-breath() {
#   pkgdesc="A flat theme with transparent elements and Blackish background Manjaro Breath variant"

#   cd arc-themes-blackish-breath-$pkgver
#   DESTDIR="$pkgdir" meson install -C build
# }
