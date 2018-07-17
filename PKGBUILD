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
pkgrel=1
#_commit=4b75f33ff2cfedb6ba0809cf877deb2d2831e6c3
#_gnomever=3.22
arch=('any')
_url='https://github.com/horst3180/arc-theme' #original theme
url='https://github.com/NicoHood/arc-theme' #soft fork
license=('GPL3')
depends=('sassc' 'gtk3')
makedepends=('optipng' 'inkscape' 'autoconf' 'automake' 'pkg-config' 'libcanberra')
optdepends=('arc-maia-icon-theme: recommended icon theme'
            'gtk-engine-murrine: for gtk2 themes'
            'gnome-themes-standard: for gtk2 themes')
#source=("${pkgbase}-${pkgver}.tar.gz::https://github.com/horst3180/${_pkgname}/archive/${pkgver}.tar.gz")
#source=("${pkgbase}-${pkgver}.tar.gz::https://github.com/horst3180/${_pkgname}/archive/${_commit}.tar.gz")
source=("${_pkgname}-${pkgver}.tar.xz::${url}/releases/download/${pkgver}/${_pkgname}-${pkgver}.tar.xz"
        "${_pkgname}-${pkgver}.tar.xz.sig::${url}/releases/download/${pkgver}/${_pkgname}-${pkgver}.tar.xz.asc")
sha256sums=('a8119f6afa91628a73d8d6d68a953522b8ebe1efee303f9bc15d1ba4b5108f35'
            'SKIP')
validpgpkeys=('97312D5EB9D7AE7D0BD4307351DAE9B7C1AE9161') #Nicohood key

#ALL arc color
_blue=5294e2 
_BLUE=5294E2
_blue1=2679db
_BLUE1=2679DB
_blue2=1e61b0
_BLUE2=1E61B0
_blue3=4dadd4
_BLUE3=4DADD4
_blue4=76c0de
_BLUE4=76C0DE
_blue5=2e96c0
_BLUE5=2E96C0
_blue6='82, 148, 226'
_blue7='65, 137, 223'
_blue8=a9caf1
_BLUE8=A9CAF1
_blue9=97bfee
_BLUE9=97BFEE
_blue10=577ba7
_BLUE10=577BA7
_blue11=7eafe9
_BLUE11=7EAFE9
_blue12=4a85cb
_BLUE12=4A85CB
_blue13='38, 121, 219'
_blue14=639fe5
_BLUE14=639FE5
_blue15=4189df
_BLUE15=4189DF
_blue16='11, 57, 103, 0.95'
_blue17='11, 57, 103, 0.8'
_blue18='0, 0, 255, 0.2'

#All Maia color variation
_maia=16A085
_maia1=0B9D67
_maia2=19E89C
_maia3=16A674
_maia4=20E6A1
_maia5=2BC18D
_maia6='43, 193, 141'
_maia7='11, 57, 103'
_maia8=00FDAF
_maia9=00FDAF
_maia10=2AC18D
_maia11=0B9D67
_maia12=0ACE7E
_maia13='11, 57, 103'
_maia14=0ACE7E
_maia15=2BC18D
_maia16='11, 103, 57, 0.95'
_maia17='11, 103, 57, 0.8'
_maia18='22, 160, 133, 0.9'

#All Breath color variation
_breath=1abc9c
_breath1=148f77
_breath2=18ab8e
_breath3=1ccdaa
_breath4=22e1bb
_breath5=19b797
_breath6='26, 188, 156'
_breath7='11, 57, 103'
_breath8=00fcc9  
_breath9=00f7c5
_breath10=009964
_breath11=28e1bd
_breath12=1ccdaa
_breath13='11, 103, 57'
_breath14=62e9cf
_breath15=40e5c4    
_breath16='11, 103, 57, 0.95'
_breath17='11, 103, 57, 0.8'
_breath18='26, 188, 156, 0.9' 

prepare() {
cd $srcdir
	#cp -R "$_pkgname-$_commit" "$_pkgname-$pkgver"
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
#change rgb color format
find . -type f -name '*.*' -exec sed -i "s|$_blue6|$_maia6|g" {} \;
msg "done1"
find . -type f -name '*.*' -exec sed -i "s|$_blue7|$_maia7|g" {} \;
msg "done2"
find . -type f -name '*.*' -exec sed -i "s|$_blue13|$_maia13|g" {} \;
msg "done3"
find . -type f -name '*.*' -exec sed -i "s|$_blue16|$_maia16|g" {} \;
msg "done4"
find . -type f -name '*.*' -exec sed -i "s|$_blue17|$_maia17|g" {} \;
msg "done5"
find . -type f -name '*.*' -exec sed -i "s|$_blue18|$_maia18|g" {} \;
msg "done6"

#transform in lowercase in uppercase 
find . -type f -name '*.*' -exec sed -i "s|$_blue|$_BLUE|g" {} \;
msg "done7"
find . -type f -name '*.*' -exec sed -i "s|$_blue1|$_BLUE1|g" {} \;
msg "done8"
find . -type f -name '*.*' -exec sed -i "s|$_blue2|$_BLUE2|g" {} \;
msg "done9"
find . -type f -name '*.*' -exec sed -i "s|$_blue3|$_BLUE3|g" {} \;
msg "done10"
find . -type f -name '*.*' -exec sed -i "s|$_blue4|$_BLUE4|g" {} \;
msg "done11"
find . -type f -name '*.*' -exec sed -i "s|$_blue5|$_BLUE5|g" {} \;
msg "done12"
find . -type f -name '*.*' -exec sed -i "s|$_blue8|$_BLUE8|g" {} \;
msg "done13"
find . -type f -name '*.*' -exec sed -i "s|$_blue9|$_BLUE9|g" {} \;
msg "done14"
find . -type f -name '*.*' -exec sed -i "s|$_blue10|$_BLUE10|g" {} \;
msg "done15"
find . -type f -name '*.*' -exec sed -i "s|$_blue11|$_BLUE11|g" {} \;
msg "done16"
find . -type f -name '*.*' -exec sed -i "s|$_blue12|$_BLUE12|g" {} \;
msg "done17"
find . -type f -name '*.*' -exec sed -i "s|$_blue14|$_BLUE14|g" {} \;
msg "done18"
find . -type f -name '*.*' -exec sed -i "s|$_blue15|$_BLUE15|g" {} \;
msg "done19"

#apply maia variation
find . -type f -name '*.*' -exec sed -i "s|$_BLUE|$_maia|g" {} \;
msg "done20"
find . -type f -name '*.*' -exec sed -i "s|$_BLUE1|$_maia1|g" {} \;
msg "done21"
find . -type f -name '*.*' -exec sed -i "s|$_BLUE2|$_maia2|g" {} \;
msg "done22"
find . -type f -name '*.*' -exec sed -i "s|$_BLUE3|$_maia3|g" {} \;
msg "done23"
find . -type f -name '*.*' -exec sed -i "s|$_BLUE4|$_maia4|g" {} \;
msg "done24"
find . -type f -name '*.*' -exec sed -i "s|$_BLUE5|$_maia5|g" {} \;
msg "done25"
find . -type f -name '*.*' -exec sed -i "s|$_BLUE8|$_maia8|g" {} \;
msg "done26"
find . -type f -name '*.*' -exec sed -i "s|$_BLUE9|$_maia9|g" {} \;
msg "done27"
find . -type f -name '*.*' -exec sed -i "s|$_BLUE10|$_maia10|g" {} \;
msg "done28"
find . -type f -name '*.*' -exec sed -i "s|$_BLUE11|$_maia11|g" {} \;
msg "done29"
find . -type f -name '*.*' -exec sed -i "s|$_BLUE12|$_maia12|g" {} \;
msg "done30"
find . -type f -name '*.*' -exec sed -i "s|$_BLUE14|$_maia14|g" {} \;
msg "done31"
find . -type f -name '*.*' -exec sed -i "s|$_BLUE15|$_maia15|g" {} \;
msg "done32"
echo

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
#change rgb color format
find . -type f -name '*.*' -exec sed -i "s|$_blue6|$_breath6|g" {} \;
msg "done1"
find . -type f -name '*.*' -exec sed -i "s|$_blue7|$_breath7|g" {} \;
msg "done2"
find . -type f -name '*.*' -exec sed -i "s|$_blue13|$_breath13|g" {} \;
msg "done3"
find . -type f -name '*.*' -exec sed -i "s|$_blue16|$_breath16|g" {} \;
msg "done4"
find . -type f -name '*.*' -exec sed -i "s|$_blue17|$_breath17|g" {} \;
msg "done5"
find . -type f -name '*.*' -exec sed -i "s|$_blue18|$_breath18|g" {} \;
msg "done6"

#transform in lowercase in uppercase 
find . -type f -name '*.*' -exec sed -i "s|$_blue|$_BLUE|g" {} \;
msg "done7"
find . -type f -name '*.*' -exec sed -i "s|$_blue1|$_BLUE1|g" {} \;
msg "done8"
find . -type f -name '*.*' -exec sed -i "s|$_blue2|$_BLUE2|g" {} \;
msg "done9"
find . -type f -name '*.*' -exec sed -i "s|$_blue3|$_BLUE3|g" {} \;
msg "done10"
find . -type f -name '*.*' -exec sed -i "s|$_blue4|$_BLUE4|g" {} \;
msg "done11"
find . -type f -name '*.*' -exec sed -i "s|$_blue5|$_BLUE5|g" {} \;
msg "done12"
find . -type f -name '*.*' -exec sed -i "s|$_blue8|$_BLUE8|g" {} \;
msg "done13"
find . -type f -name '*.*' -exec sed -i "s|$_blue9|$_BLUE9|g" {} \;
msg "done14"
find . -type f -name '*.*' -exec sed -i "s|$_blue10|$_BLUE10|g" {} \;
msg "done15"
find . -type f -name '*.*' -exec sed -i "s|$_blue11|$_BLUE11|g" {} \;
msg "done16"
find . -type f -name '*.*' -exec sed -i "s|$_blue12|$_BLUE12|g" {} \;
msg "done17"
find . -type f -name '*.*' -exec sed -i "s|$_blue14|$_BLUE14|g" {} \;
msg "done18"
find . -type f -name '*.*' -exec sed -i "s|$_blue15|$_BLUE15|g" {} \;
msg "done19"

#apply breath variation
find . -type f -name '*.*' -exec sed -i "s|$_BLUE|$_breath|g" {} \;
msg "done20"
find . -type f -name '*.*' -exec sed -i "s|$_BLUE1|$_breath1|g" {} \;
msg "done21"
find . -type f -name '*.*' -exec sed -i "s|$_BLUE2|$_breath2|g" {} \;
msg "done22"
find . -type f -name '*.*' -exec sed -i "s|$_BLUE3|$_breath3|g" {} \;
msg "done23"
find . -type f -name '*.*' -exec sed -i "s|$_BLUE4|$_breath4|g" {} \;
msg "done24"
find . -type f -name '*.*' -exec sed -i "s|$_BLUE5|$_breath5|g" {} \;
msg "done25"
find . -type f -name '*.*' -exec sed -i "s|$_BLUE8|$_breath8|g" {} \;
msg "done26"
find . -type f -name '*.*' -exec sed -i "s|$_BLUE9|$_breath9|g" {} \;
msg "done27"
find . -type f -name '*.*' -exec sed -i "s|$_BLUE10|$_breath10|g" {} \;
msg "done28"
find . -type f -name '*.*' -exec sed -i "s|$_BLUE11|$_breath11|g" {} \;
msg "done29"
find . -type f -name '*.*' -exec sed -i "s|$_BLUE12|$_breath12|g" {} \;
msg "done30"
find . -type f -name '*.*' -exec sed -i "s|$_BLUE14|$_breath14|g" {} \;
msg "done31"
find . -type f -name '*.*' -exec sed -i "s|$_BLUE15|$_breath15|g" {} \;
msg "done32"
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
