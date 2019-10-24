.PHONY: all, test, build

all: build test

test:
	bazel test //...

build:
	bazel build //...
