import os
from conans import ConanFile, tools, CMake
from conans.errors import ConanInvalidConfiguration
from conans.tools import Version


class WinceCrtConan(ConanFile):
    name = "wince-crt"
    version = "1.0"
    description = "package for fix wince build"
    url = "https://github.com/Arenoros/wince-crt"
    homepage = "https://github.com/Arenoros/wince-crt"
    topics = ("conan", "wince")
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        tools.rmdir(self._source_subfolder)
        git = tools.Git(folder=self._source_subfolder)
        git.clone("https://github.com/Arenoros/wince-crt.git", 'master')

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure()
        return cmake

    def build(self):
        # TODO: GYP is not supported by MSVC 16
        self.cmake = self._configure_cmake()
        self.cmake.build()

    def package(self):
        self.cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        