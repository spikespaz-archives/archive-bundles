# Maintainer: Stefano Capitani <stefanoatmanjarodotorg>
# Contributor: ceyhunnabiyev for Breath color <https://github.com/ceyhunnabiyev>
# This pkgbuild provide Maia and Breath variant of Arc Theme 

# Maintainer: NicoHood <archlinux {cat} nicohood {dog} de>
# PGP ID: 97312D5EB9D7AE7D0BD4307351DAE9B7C1AE9161
# Contributor: zach <zach {at} zach-adams {dot} com>
# Contributor: Gordian Edenhofer <gordian.edenhofer[at]yahoo[dot]de
# Contributor: Philipp Wolfer <ph.wolfer@gmail.com>

pkgbase=arc-themes-maia
pkgname=('arc-themes-solid-maia'
         'arc-themes-maia'
         'arc-themes-breath'
         'arc-themes-solid-breath')
_pkgname=arc-theme
pkgver=20211018
pkgrel=2
arch=('any')
# Upstream url: https://github.com/horst3180/arc-theme
# Now using soft fork: https://github.com/jnsh/arc-theme/issues/18
url="https://github.com/jnsh/arc-theme"
license=('GPL3')
optdepends=('arc-icon-theme: recommended icon theme'
            'gtk-engine-murrine: for gtk2 themes'
            'gnome-themes-standard: for gtk2 themes')
makedepends=('meson' 'sassc' 'inkscape' 'gtk4')

source=("${pkgbase}-${pkgver}.tar.xz::${url}/releases/download/${pkgver}/${_pkgname}-${pkgver}.tar.xz")
#        "${pkgbase}-${pkgver}.tar.xz.sig::${url}/releases/download/${pkgver}/${_pkgname}-${pkgver}.tar.xz.asc")
sha512sums=('da46efc0e38efb7f1d0cd9a5d2c4e8f00f3b8d408ec50c54d89ef67fc3bb5ea253b5fb890b0cb8e82cafebd44a599d0de2369272ed88da73dd979052b130bd55')
#validpgpkeys=('31743CDF250EF641E57503E5FAEDBC4FB5AA3B17') # Joonas Henriksson <joonas.henriksson@gmail.com> @pgp.mit.edu

#ALL arc color
_BLUE=5294E2 
_BLUE3=4DADD4 

#All Maia color variation
_maia=16A085
_maia3=16A674

#All Breath color variation
_breath=1abc9c
_breath3=1ccdaa

prepare() {
cd $srcdir
	cp -R "$_pkgname-$pkgver" "arc-themes-maia-$pkgver"
	cp -R "$_pkgname-$pkgver" "arc-themes-breath-$pkgver"
}	

# Latest stable Arch package versions
_cinnamonver=5.0
_gnomeshellver=40
_gtk3ver=3.24
_gtk4ver=4.4

build_arc-maia() {

cd $srcdir/arc-themes-maia-$pkgver
echo "Build arc-themes-maia" 
echo
echo "Create arc-themes-maia:this next bit might take a little while..."
echo
echo "Create new name : *-Maia"
echo
#Add Maia suffix (don't change this order)
find . -type f -name '*.*' -exec sed -i \
   "s/Arc/Arc-Maia/g;\
   s/Arc-Darker/Arc-Darker-Maia/g;\
  s/Arc-Dark/Arc-Dark-Maia/g" {} \;

cd $srcdir/arc-themes-maia-$pkgver

#Change the color Blue > Maia
echo "Manjarification : Change all arc color to green maia"
echo

#override gtk2 schemas
sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #16A085",' $srcdir/arc-themes-maia-$pkgver/common/gtk-2.0/light/gtkrc
sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #16A085",' $srcdir/arc-themes-maia-$pkgver/common/gtk-2.0/light/gtkrc
sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #16A085",' $srcdir/arc-themes-maia-$pkgver/common/gtk-2.0/dark/gtkrc
sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #16A085",' $srcdir/arc-themes-maia-$pkgver/common/gtk-2.0/dark/gtkrc
sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #16A085",' $srcdir/arc-themes-maia-$pkgver/common/gtk-2.0/darker/gtkrc
sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #16A085",' $srcdir/arc-themes-maia-$pkgver/common/gtk-2.0/darker/gtkrc
echo "Done override gtk2 schemas"
echo
echo "Change Hex format"
echo

#apply maia variation
find . -type f -name '*.scss' -exec sed -i "s|$_BLUE|$_maia|Ig" {} \;
echo "done1"
echo
find . -type f -name '*.scss' -exec sed -i "s|$_BLUE3|$_maia3|Ig" {} \;
echo "done2"
echo
find . -type f -name '*.svg' -exec sed -i "s|$_BLUE|$_maia|Ig" {} \;
echo "done3"

echo "Rebuild png file : waiting"
echo

echo "Building maia-theme"
echo

  cd $srcdir/arc-themes-maia-$pkgver
  meson --prefix=/usr build \
      -Dgnome_shell_gresource=true \
      -Dcinnamon_version="${_cinnamonver}" \
      -Dgnome_shell_version="${_gnomeshellver}" \
      -Dgtk3_version="${_gtk3ver}" \
      -Dgtk4_version="${_gtk4ver}"
    meson compile -C build

    meson --prefix=/usr build-solid \
      -Dtransparency=false \
      -Dgnome_shell_gresource=true \
      -Dcinnamon_version="${_cinnamonver}" \
      -Dgnome_shell_version="${_gnomeshellver}" \
      -Dgtk3_version="${_gtk3ver}" \
      -Dgtk4_version="${_gtk4ver}"
    meson compile -C build-solid
}

build_arc-breath() {

cd $srcdir/arc-themes-breath-$pkgver
echo "Build arc-themes-breath" 
echo
echo "Create arc-themes-breath:this next bit might take a little while..."
echo
echo "Create new name : *-Breath"
echo
#Add Breath suffix (don't change this order)
find . -type f -name '*.*' -exec sed -i \
   "s/Arc/Arc-Breath/g;\
   s/Arc-Darker/Arc-Darker-Breath/g;\
  s/Arc-Dark/Arc-Dark-Breath/g" {} \;

cd $srcdir/arc-themes-breath-$pkgver

#Change the color Blue > Breath
echo "Manjarification : Change all arc color to green breath"
echo

#override gtk2 schemas
sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #1abc9c",' $srcdir/arc-themes-breath-$pkgver/common/gtk-2.0/light/gtkrc
sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #1abc9c",' $srcdir/arc-themes-breath-$pkgver/common/gtk-2.0/light/gtkrc
sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #1abc9c",' $srcdir/arc-themes-breath-$pkgver/common/gtk-2.0/dark/gtkrc
sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #1abc9c",' $srcdir/arc-themes-breath-$pkgver/common/gtk-2.0/dark/gtkrc
sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #1abc9c",' $srcdir/arc-themes-breath-$pkgver/common/gtk-2.0/darker/gtkrc
sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #1abc9c",' $srcdir/arc-themes-breath-$pkgver/common/gtk-2.0/darker/gtkrc
echo "Done override gtk2 schemas"
echo
echo "Change Hex format"
echo

#apply breath variation
find . -type f -name '*.scss' -exec sed -i "s|$_BLUE|$_breath|Ig" {} \;
echo "done1"
echo
find . -type f -name '*.scss' -exec sed -i "s|$_BLUE3|$_breath3|Ig" {} \;
echo "done2"
echo
find . -type f -name '*.svg' -exec sed -i "s|$_BLUE|$_breath|Ig" {} \;
echo "done3"

echo
echo "Rebuild png file : waiting"
echo

echo "Building breath-theme"
echo

  cd $srcdir/arc-themes-breath-$pkgver
  meson --prefix=/usr build \
      -Dgnome_shell_gresource=true \
      -Dcinnamon_version="${_cinnamonver}" \
      -Dgnome_shell_version="${_gnomeshellver}" \
      -Dgtk3_version="${_gtk3ver}" \
      -Dgtk4_version="${_gtk4ver}"
    meson compile -C build

    meson --prefix=/usr build-solid \
      -Dtransparency=false \
      -Dgnome_shell_gresource=true \
      -Dcinnamon_version="${_cinnamonver}" \
      -Dgnome_shell_version="${_gnomeshellver}" \
      -Dgtk3_version="${_gtk3ver}" \
      -Dgtk4_version="${_gtk4ver}"
    meson compile -C build-solid
}

build() {
build_arc-maia
build_arc-breath
}
 
package_arc-themes-solid-maia() {
pkgdesc="A flat theme without transparent elements Manjaro Maia variant"
cd $srcdir/arc-themes-maia-$pkgver
	DESTDIR="$pkgdir" meson install -C build-solid

#Change folder name for solid version 

cd $pkgdir/usr/share/themes

#Add Maia-Solid suffix (don't change this order)
find . -type f -name '*.*' -exec sed -i \
   "s/Arc-Maia/Arc-Maia-Solid/g;\
   s/Arc-Darker-Maia/Arc-Darker-Maia-Solid/g;\
  s/Arc-Dark-Maia/Arc-Dark-Maia-Solid/g" {} \;
}

package_arc-themes-maia() {
pkgdesc="A flat theme with transparent elements Manjaro Maia variant"  
cd $srcdir/arc-themes-maia-$pkgver
	DESTDIR="$pkgdir" meson install -C build
}

package_arc-themes-solid-breath() {
pkgdesc="A flat theme without transparent elements Manjaro Breath variant"
cd $srcdir/arc-themes-breath-$pkgver
	DESTDIR="$pkgdir" meson install -C build-solid

#Change folder name for solid version
cd $pkgdir/usr/share/themes

#Add Breath-Solid suffix (don't change this order)
find . -type f -name '*.*' -exec sed -i \
   "s/Arc-Breath/Arc-Breath-Solid/g;\
   s/Arc-Darker-Breath/Arc-Darker-Breath-Solid/g;\
  s/Arc-Dark-Breath/Arc-Dark-Breath-Solid/g" {} \;
}

package_arc-themes-breath() {
pkgdesc="A flat theme with transparent elements Manjaro Breath variant" 
cd $srcdir/arc-themes-breath-$pkgver
	DESTDIR="$pkgdir" meson install -C build
}
