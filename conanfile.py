from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, cmake_layout, CMakeDeps
from conan.errors import ConanInvalidConfiguration

class upZenohTransportRecipe(ConanFile):
    name = "up-transport-zenoh-cpp"

    # Optional metadata
    license = "Apache-2.0"
    author = "Contributors to the Eclipse Foundation <uprotocol-dev@eclipse.org>"
    url = "https://github.com/eclipse-uprotocol/up-transport-zenoh-cpp"
    description = "This library provides a Zenoh-based uProtocol transport for C++ uEntities"
    topics = ("automotive", "iot", "uprotocol", "messaging")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "backend": ["zenoh-pico", "zenoh-tmp"],
    }

    default_options = {
        "backend": "zenoh-tmp",
    }

    def requirements(self):
        if "zenoh-tmp" == self.options.backend:
            self.requires("zenohcpp/1.0.0-rc5")
            self.requires("zenohc/1.0.0-rc5")
        elif "zenoh-pico" == self.options.backend:
            self.requires("zenoh-cpp/1.0.0-rc5", options={"backend":"zenoh-pico"})
            self.requires("zenoh-pico/1.0.0-rc5")
        else:
            raise ConanInvalidConfiguration(f"Zenoh backend: {self.options.backend} is not supported")
        self.requires("up-core-api/[~1.6, include_prerelease]")
        self.requires("up-cpp/[^1.0.1]")
        self.requires("spdlog/[~1.13]")
        self.requires("protobuf/[~3.21]")
        self.test_requires("gtest/1.14.0")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        if "zenoh-tmp" == self.options.backend:
            tc.cache_variables["WITH_ZENOH_PICO"] = False
            tc.cache_variables["WITH_ZENOH_C"] = False
        elif "zenoh-pico" == self.options.backend:
            tc.cache_variables["WITH_ZENOH_PICO"] = True
            tc.cache_variables["WITH_ZENOH_C"] = False
        else:
            raise ConanInvalidConfiguration(f"Zenoh backend: {self.options.backend} is not supported")
        tc.generate()
