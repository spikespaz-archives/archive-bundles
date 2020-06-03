# Maintainer: Stefano Capitani <stefanoatmanjarodotorg>
# Contributor: ceyhunnabiyev for Breath color <https://github.com/ceyhunnabiyev>
# This pkgbuild provide Maia and Breath variant of Arc Theme 
# New soft fork at https://github.com/NicoHood/arc-theme

# Archlinux credits
# Maintainer: NicoHood <archlinux {cat} nicohood {dog} de>
# PGP ID: 97312D5EB9D7AE7D0BD4307351DAE9B7C1AE9161
# Contributor: zach <zach {at} zach-adams {dot} com>
# Contributor: Gordian Edenhofer <gordian.edenhofer[at]yahoo[dot]de
# Contributor: Philipp Wolfer <ph.wolfer@gmail.com>

pkgbase=arc-theme
pkgname=('arc-themes-solid-maia'
		 'arc-themes-maia'
		 'arc-themes-breath'
		 'arc-themes-solid-breath')
_pkgname=$pkgbase
_pkgbase=arc-themes-maia
pkgver=20200513
pkgrel=1
arch=('any')
# Upstream url: https://github.com/horst3180/arc-theme
# Now using soft fork: https://github.com/jnsh/arc-theme/issues/18
url="https://github.com/jnsh/arc-theme"
license=('GPL3')
optdepends=('arc-icon-theme: recommended icon theme'
            'gtk-engine-murrine: for gtk2 themes'
            'gnome-themes-standard: for gtk2 themes'            )
makedepends=('sassc' 'optipng' 'inkscape')

source=("${pkgname}-${pkgver}.tar.xz::${url}/releases/download/${pkgver}/${_pkgname}-${pkgver}.tar.xz"
        "${pkgname}-${pkgver}.tar.xz.sig::${url}/releases/download/${pkgver}/${_pkgname}-${pkgver}.tar.xz.asc")
sha512sums=('ac814babf995facce72497efad7d7afb6d2eed0ad02640aeb694874681c961b136fcc4fba8350fdee715d44c26db2a336b3430c054a299285ced782ed67bbcfe'
            'SKIP')
validpgpkeys=('31743CDF250EF641E57503E5FAEDBC4FB5AA3B17')

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

build_arc-maia() {

cd $srcdir/arc-themes-maia-$pkgver
msg "Build arc-themes-maia" 
echo
msg "Create arc-themes-maia:this next bit might take a little while..."
echo
msg "Create new name : *-Maia"
echo
#Add Maia suffix (don't change this order)
find . -type f -name '*.*' -exec sed -i \
   "s/Arc/Arc-Maia/g;\
   s/Arc-Darker/Arc-Darker-Maia/g;\
  s/Arc-Dark/Arc-Dark-Maia/g" {} \;
  
cd $srcdir/arc-themes-maia-$pkgver/common/openbox
mv Arc Arc-Maia 
mv Arc-Dark Arc-Maia-Dark 
mv Arc-Darker Arc-Maia-Darker 

cd $srcdir/arc-themes-maia-$pkgver

#Change the color Blue > Maia
msg "Manjarification : Change all arc color to green maia"
echo

#override gtk2 schemas
sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #16A085",' $srcdir/arc-themes-maia-$pkgver/common/gtk-2.0/light/gtkrc
sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #16A085",' $srcdir/arc-themes-maia-$pkgver/common/gtk-2.0/light/gtkrc
sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #16A085",' $srcdir/arc-themes-maia-$pkgver/common/gtk-2.0/dark/gtkrc
sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #16A085",' $srcdir/arc-themes-maia-$pkgver/common/gtk-2.0/dark/gtkrc
sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #16A085",' $srcdir/arc-themes-maia-$pkgver/common/gtk-2.0/darker/gtkrc
sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #16A085",' $srcdir/arc-themes-maia-$pkgver/common/gtk-2.0/darker/gtkrc
msg "Done override gtk2 schemas"
echo
msg "Change Hex format"
echo

#apply maia variation
find . -type f -name '*.scss' -exec sed -i "s|$_BLUE|$_maia|Ig" {} \;
msg "done1"
echo
find . -type f -name '*.scss' -exec sed -i "s|$_BLUE3|$_maia3|Ig" {} \;
msg "done2"
echo
find . -type f -name '*.svg' -exec sed -i "s|$_BLUE|$_maia|Ig" {} \;
msg "done3"

msg "Rebuild png file : waiting"
echo

msg "Building maia-theme"
echo

  cd $srcdir/arc-themes-maia-$pkgver
  ./autogen.sh --prefix=/usr --disable-plank --with-gnome-shell=3.36 --with-cinnamon=4.6 --with-gtk3=3.24
}

build_arc-breath() {

cd $srcdir/arc-themes-breath-$pkgver
msg "Build arc-themes-breath" 
echo
msg "Create arc-themes-breath:this next bit might take a little while..."
echo
msg "Create new name : *-Breath"
echo
#Add Breath suffix (don't change this order)
find . -type f -name '*.*' -exec sed -i \
   "s/Arc/Arc-Breath/g;\
   s/Arc-Darker/Arc-Darker-Breath/g;\
  s/Arc-Dark/Arc-Dark-Breath/g" {} \;
  
cd $srcdir/arc-themes-breath-$pkgver/common/openbox
mv Arc Arc-Breath
mv Arc-Dark Arc-Breath-Dark
mv Arc-Darker Arc-Breath-Darker 

cd $srcdir/arc-themes-breath-$pkgver

#Change the color Blue > Breath
msg "Manjarification : Change all arc color to green breath"
echo

#override gtk2 schemas
sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #1abc9c",' $srcdir/arc-themes-breath-$pkgver/common/gtk-2.0/light/gtkrc
sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #1abc9c",' $srcdir/arc-themes-breath-$pkgver/common/gtk-2.0/light/gtkrc
sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #1abc9c",' $srcdir/arc-themes-breath-$pkgver/common/gtk-2.0/dark/gtkrc
sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #1abc9c",' $srcdir/arc-themes-breath-$pkgver/common/gtk-2.0/dark/gtkrc
sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #1abc9c",' $srcdir/arc-themes-breath-$pkgver/common/gtk-2.0/darker/gtkrc
sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #1abc9c",' $srcdir/arc-themes-breath-$pkgver/common/gtk-2.0/darker/gtkrc
msg "Done override gtk2 schemas"
echo
msg "Change Hex format"
echo

#apply breath variation
find . -type f -name '*.scss' -exec sed -i "s|$_BLUE|$_breath|Ig" {} \;
msg "done1"
echo
find . -type f -name '*.scss' -exec sed -i "s|$_BLUE3|$_breath3|Ig" {} \;
msg "done2"
echo
find . -type f -name '*.svg' -exec sed -i "s|$_BLUE|$_breath|Ig" {} \;
msg "done3"

echo
msg "Rebuild png file : waiting"
echo

msg "Building breath-theme"
echo

  cd $srcdir/arc-themes-breath-$pkgver
  ./autogen.sh --prefix=/usr --disable-plank --with-gnome-shell=3.36 --with-cinnamon=4.6 --with-gtk3=3.24
}

build() {
build_arc-maia
build_arc-breath
}

#https://github.com/NicoHood/arc-theme/issues/139#issuecomment-427616375

  
package_arc-themes-solid-maia() {
pkgdesc="A flat theme without transparent elements Manjaro Maia variant"
cd $srcdir/arc-themes-maia-$pkgver
  ./configure --prefix=/usr --disable-transparency --disable-plank --with-gnome-shell=3.36 --with-cinnamon=4.6 --with-gtk3=3.24
  make DESTDIR="${pkgdir}" install

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
  ./configure --prefix=/usr --disable-plank --with-gnome-shell=3.36 --with-cinnamon=4.6 --with-gtk3=3.24
  make DESTDIR="${pkgdir}" install
}

package_arc-themes-solid-breath() {
pkgdesc="A flat theme without transparent elements Manjaro Breath variant"
cd $srcdir/arc-themes-breath-$pkgver
  ./configure --prefix=/usr --disable-transparency --disable-plank --with-gnome-shell=3.36 --with-cinnamon=4.6 --with-gtk3=3.24
  make DESTDIR="${pkgdir}" install

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
  ./configure --prefix=/usr --disable-plank --with-gnome-shell=3.36 --with-cinnamon=4.6 --with-gtk3=3.24
  make DESTDIR="${pkgdir}" install
}
