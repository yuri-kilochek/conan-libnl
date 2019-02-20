from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.errors import ConanInvalidConfiguration

class LibNLConan(ConanFile):
    name = 'libnl'
    version = '3.2.25'
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
    }
    default_options = {
        'shared': True,
        'fPIC': False,
    }

    def configure(self):
        if self.settings.os != 'Linux':
            raise ConanInvalidConfiguration('This is a Linux-only library.')
        if self.options.shared:
            self.options.fPIC = True

    def source(self):
        self.run('git clone --branch libnl' + self.version.replace('.', '_') +
                 ' --depth 1 git://github.com/tgraf/libnl.git .')

    def build(self):
        self.run('sh autogen.sh')
        autotools = AutoToolsBuildEnvironment(self);
        autotools.configure()
        autotools.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

