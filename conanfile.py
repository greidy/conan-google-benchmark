import os
from conans import ConanFile, CMake
from conans.tools import download, unzip


class GoogleBenchmarkConan(ConanFile):
    name = "google-benchmark"
    version = "1.1.0"
    settings = "arch", "build_type", "compiler", "os"
    # options = {"option1": [,], } <-- any options needed?
    generators = "cmake"
    url = "http://github.com/cpace6/conan-google-benchmark"
    source_root = "benchmark-1.1.0"
    license = "https://github.com/google/benchmark/blob/master/LICENSE"


    def source(self):
        zip_name = "v%s.zip" % self.version
        url = "https://github.com/google/benchmark/archive/%s" % zip_name
        download(url, zip_name)
        unzip(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        self.run("mkdir _build")
        configure_command = 'cd _build && cmake ../%s %s' % (self.source_root, cmake.command_line)
        self.run(configure_command)
        self.run("cd _build && cmake --build . %s" % cmake.build_config)

    def build(self):
        cmake = CMake(self.settings)
        if self.settings.os == "Windows":
            self.run("IF not exist _build mkdir _build")
        else:
            self.run("mkdir _build")
        self.run('cd _build && cmake ../%s %s' % (self.source_root, cmake.command_line))
        self.run("cd _build && cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy(pattern="*.h", dst="include", src="%s/include" % self.source_root, keep_path=True)
        self.copy(pattern="*.a", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=".", keep_path=False)

    def package_info(self):  
        self.cpp_info.libs = ["benchmark"]