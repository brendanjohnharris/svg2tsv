# Maintainer: Brendan Harris <brendanjohnharris@gmail.com>
pkgname=svg2csv
pkgver=1.0.0
pkgrel=1
pkgdesc="A command-line tool to extract points from SVG paths and save them as a matrix."
arch=('any')
url="https://github.com/brendanjohnharris/svg2tsv"
license=('MIT')
depends=('python' 'python-svgpathtools' 'python-numpy')
makedepends=('python-setuptools')
source=("$pkgname-$pkgver.tar.gz::$url/archive/v$pkgver.tar.gz")
sha256sums=('SKIP')

build() {
    cd "$srcdir/$pkgname-$pkgver"
    python setup.py build
}

package() {
    cd "$srcdir/$pkgname-$pkgver"
    python setup.py install --root="$pkgdir/" --optimize=1
}
