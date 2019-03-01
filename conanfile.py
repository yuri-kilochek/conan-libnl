from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.errors import ConanInvalidConfiguration
import glob, shutil, os, os.path

class LibNLConan(ConanFile):
    name = 'libnl'
    version = '3.4.0'
    license = 'LGPL-2.1'
    homepage = 'https://www.infradead.org/~tgr/libnl'
    description = ('Netlink protocol library suite is a collection of '
                   'libraries providing APIs to netlink protocol based Linux '
                   'kernel interfaces.')
    topics = 'linux', 'netlink'

    url = 'https://github.com/yuri-kilochek/conan-libnl.git'
    author = 'Yuri Kilochek <yuri.kilochek@gmail.com>'

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {
        'shared': [False, True],
        'fPIC': [False, True],
        'cli': [False, True],
    }
    default_options = {
        'shared': True,
        'fPIC': False,
        'cli': False,
    }

    def configure(self):
        if self.settings.os != 'Linux':
            raise ConanInvalidConfiguration('This is a Linux-only library.')

        if self.options.shared:
            self.options.fPIC = True

    def source(self):
        self.run('git clone --branch {tag} --depth 1 {url} .'.format(
            tag='libnl{}'.format(self.version.replace('.', '_')),
            url='git://github.com/thom311/libnl.git',
        ))

    def build(self):
        self.run('sh autogen.sh')

        autotools = AutoToolsBuildEnvironment(self)

        args = []

        if self.options.shared:
            args.append('--enable-static=no')
        else:
            args.append('--enable-shared=no')

        if 'Rel' in self.settings.build_type:
            args.append('--disable-debug')

        if not self.options.cli:
            args.append('--enable-cli=no')

        autotools.configure(args=args)

        autotools.install()

        def here(*args):
            return os.path.join(self.package_folder, *args)
        shutil.rmtree(here('share'))
        shutil.rmtree(here('lib', 'pkgconfig'))
        for path in glob.iglob(here('lib', '*.la')):
            os.remove(path)

    def package_info(self):
        self.cpp_info.includedirs = [os.path.join('include', 'libnl{}'.format(
            self.version.split('.')[0],
        ))]
        self.cpp_info.libs = tools.collect_libs(self)

