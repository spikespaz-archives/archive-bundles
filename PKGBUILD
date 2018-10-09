# Maintainer: Stefano Capitani <stefanoatmanjarodotorg>
# Author: horst3180 @ deviantart 
# Contributor: ceyhunnabiyev for Breath color <https://github.com/ceyhunnabiyev>
# This pkgbuild provide Maia and Breath variant of Arc Theme 
# New soft fork at https://github.com/NicoHood/arc-theme

pkgbase=arc-theme
pkgname=('arc-themes-solid-maia'
		 'arc-themes-maia'
		 'arc-themes-breath'
		 'arc-themes-solid-breath')
_pkgname=$pkgbase
_pkgbase=arc-themes-maia
pkgver=20180715
pkgrel=4
_commit=7ff5b36c287fd50a5910a67a255a3d6bec58b679
#_gnomever=3.22
arch=('any')
_url='https://github.com/horst3180/arc-theme' #original theme
url='https://github.com/NicoHood/arc-theme' #soft fork
license=('GPL3')
depends=('sassc' 'gtk3')
makedepends=('optipng' 'inkscape' 'autoconf' 'automake' 'pkg-config' 'libcanberra' 'gnome-shell')
optdepends=('arc-maia-icon-theme: recommended icon theme'
            'gtk-engine-murrine: for gtk2 themes'
            'gnome-themes-standard: for gtk2 themes')
#source=("${pkgbase}-${pkgver}.tar.gz::https://github.com/horst3180/${_pkgname}/archive/${pkgver}.tar.gz")
#source=("${pkgbase}-${pkgver}.tar.gz::https://github.com/horst3180/${_pkgname}/archive/${_commit}.tar.gz")
source=( #"${_pkgname}-${pkgver}.tar.xz::${url}/releases/download/${pkgver}/${_pkgname}-${pkgver}.tar.xz"
        #"${_pkgname}-${pkgver}.tar.xz.sig::${url}/releases/download/${pkgver}/${_pkgname}-${pkgver}.tar.xz.asc"
        "${_pkgname}-${pkgver}.tar.xz::${url}/archive/${_commit}.tar.gz"
        'xfce-desktop-icons-view.patch')
sha256sums=('1753590f404e5a09c051935067bfea4bb4a7fe6ca7951b303398a1e0eec5a9e6'
            'e0010ad5890d77d5df2f1fd26ee21467a5787b1f9d0f737d18e054f3b25e2936')
validpgpkeys=('97312D5EB9D7AE7D0BD4307351DAE9B7C1AE9161') #Nicohood key

#ALL arc color
_BLUE=5294E2 #
_BLUE3=4DADD4 #

#All Maia color variation
_maia=16A085
_maia3=16A674

#All Breath color variation
_breath=1abc9c
_breath3=1ccdaa

prepare() {
#mv $srcdir/$_pkgname-$_commit $srcdir/$_pkgname-$pkgver
#cd $srcdir/$_pkgname-$pkgver/common/gtk-3.0
#	find . -type f -name 'gt*.scss' -exec sh -c "cat $srcdir/xfce-desktop-view-manjaro >> {}" \;
#cd $srcdir/$_pkgname-$_commit
# 	patch -p1 -i ../xfce-desktop-icons-view.patch
cd $srcdir
	cp -R "$_pkgname-$_commit" "arc-themes-maia-$pkgver"
	cp -R "$_pkgname-$_commit" "arc-themes-breath-$pkgver"
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
sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #16A085",' $srcdir/arc-themes-maia-$pkgver/common/gtk-2.0/gtkrc
sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #16A085",' $srcdir/arc-themes-maia-$pkgver/common/gtk-2.0/gtkrc
sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #16A085",' $srcdir/arc-themes-maia-$pkgver/common/gtk-2.0/gtkrc-dark
sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #16A085",' $srcdir/arc-themes-maia-$pkgver/common/gtk-2.0/gtkrc-dark
sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #16A085",' $srcdir/arc-themes-maia-$pkgver/common/gtk-2.0/gtkrc-darker
sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #16A085",' $srcdir/arc-themes-maia-$pkgver/common/gtk-2.0/gtkrc-darker
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
  ./autogen.sh --prefix=/usr --disable-unity --disable-plank
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
sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #1abc9c",' $srcdir/arc-themes-breath-$pkgver/common/gtk-2.0/gtkrc
sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #1abc9c",' $srcdir/arc-themes-breath-$pkgver/common/gtk-2.0/gtkrc
sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #1abc9c",' $srcdir/arc-themes-breath-$pkgver/common/gtk-2.0/gtkrc-dark
sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #1abc9c",' $srcdir/arc-themes-breath-$pkgver/common/gtk-2.0/gtkrc-dark
sed -i -e 's,.*gtk-color-scheme = "selected_bg_color: #5294e2".*,gtk-color-scheme = "selected_bg_color: #1abc9c",' $srcdir/arc-themes-breath-$pkgver/common/gtk-2.0/gtkrc-darker
sed -i -e 's,.*gtk-color-scheme = "link_color: #5294e2".*,gtk-color-scheme = "link_color: #1abc9c",' $srcdir/arc-themes-breath-$pkgver/common/gtk-2.0/gtkrc-darker
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
  ./autogen.sh --prefix=/usr --disable-unity --disable-plank
}

build() {
build_arc-maia
build_arc-breath
}
  
package_arc-themes-solid-maia() {
pkgdesc="A flat theme without transparent elements Manjaro Maia variant"
#optdepends=('arc-firefox-theme: Firefox theme to complete arc-theme experience')
cd $srcdir/arc-themes-maia-$pkgver
  ./configure --prefix=/usr --disable-transparency --disable-unity --disable-plank
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
  ./configure --prefix=/usr --disable-unity --disable-plank
  make DESTDIR="${pkgdir}" install
}

package_arc-themes-solid-breath() {
pkgdesc="A flat theme without transparent elements Manjaro Breath variant"
cd $srcdir/arc-themes-breath-$pkgver
  ./configure --prefix=/usr --disable-transparency --disable-unity --disable-plank
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
  ./configure --prefix=/usr --disable-unity --disable-plank
  make DESTDIR="${pkgdir}" install
}
