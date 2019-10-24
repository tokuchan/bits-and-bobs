# -*-Python-*-
# BUILD file for arbitrary modules.

cc_library(
    name = "random_generator",
    hdrs = ["random_generator.hpp"],
    visibility = ["//visibility:public"],
)

cc_test(
    name = "random_generator_test",
    srcs = ["random_generator_test.cpp"],
    deps = [":random_generator", "//catch2"],
)
