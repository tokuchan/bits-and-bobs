#define CATCH_CONFIG_MAIN
#include "arbitrary/random_generator.hpp"
// Arbitrary Libraries
// Accelerando Libraries
// Boost Libraries
// System Libraries
#include "catch2/catch.hpp"
// Standard Libraries

namespace accelerando::arbitrary::random_generator::tests {
TEST_CASE("random_generator smoke test") {
  GIVEN("A random_generator type") {
    WHEN("We instantiate a random_generator") {
      random_generator<> rg;
      THEN("We should be able to get a key from it") {
        unsigned int seed{rg.get_seed()};
        REQUIRE(seed == rg.get_seed());
      }
    }
  }
}
} // namespace accelerando::arbitrary::random_generator::tests
