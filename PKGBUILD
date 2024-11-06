# Maintainer: Brendan Harris <brendanjohnharris@gmail.com>
pkgname=svg2tsv
pkgver=1.1.0
pkgrel=1
pkgdesc="A command-line tool to extract points from SVG paths and save them as a TSV matrix."
arch=('any')
url="https://github.com/brendanjohnharris/svg2tsv"
license=('MIT')
depends=('python' 'python-svgpathtools' 'python-numpy' 'python-svgwrite')
makedepends=('python-setuptools')
source=("$pkgname-$pkgver.tar.gz::https://github.com/brendanjohnharris/svg2tsv/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('SKIP') # Replace 'SKIP' with the actual checksum for security

build() {
    cd "$srcdir/$pkgname-$pkgver"
    python setup.py build
}

package() {
    cd "$srcdir/$pkgname-$pkgver"
    python setup.py install --root="$pkgdir/" --optimize=1
}
