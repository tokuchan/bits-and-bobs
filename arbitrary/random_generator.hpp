#pragma once
// Arbitrary Libraries
// Accelerando Libraries
// Boost Libraries
// System Libraries
// Standard Libraries
#include <random>

namespace accelerando::arbitrary::random_generator {
namespace details {
struct random_generator_traits {
  using generator_type = std::mt19937;
  using seed_type = unsigned int;
  using value_type = unsigned int;
};

template <typename RandomGeneratorTraits>
class random_generator_generator_policy {
  /// @name Member Types
  /// @{
public:
  using generator_type = typename RandomGeneratorTraits::generator_type;
  using seed_type = typename RandomGeneratorTraits::seed_type;
  using value_type = typename RandomGeneratorTraits::value_type;
  /// @}

public:
  static seed_type random_seed() { return std::random_device{}(); }

  static generator_type make_random_generator_generator(seed_type seed) {
    return std::mt19937{seed};
  }
};

template <typename RandomGeneratorTraits = random_generator_traits,
          template <typename> typename RandomGeneratorGeneratorPolicy =
              random_generator_generator_policy>
class random_generator {
  /// @name Member Types
  /// @{
public:
  using generator_type = typename RandomGeneratorTraits::generator_type;
  using seed_type = typename RandomGeneratorTraits::seed_type;
  using value_type = typename RandomGeneratorTraits::value_type;
  using generator_policy =
      RandomGeneratorGeneratorPolicy<RandomGeneratorTraits>;
  /// @}

private:
  seed_type seed;
  generator_type prng;

  /// @name Special Members
  /// @{
public:
  random_generator()
      : seed{generator_policy::random_seed()},
        prng{generator_policy::make_random_generator_generator(seed)} {}

  random_generator(seed_type seed)
      : seed{seed}, prng{generator_policy::make_random_generator_generator(
                        seed)} {}

  random_generator(random_generator const &other)
      : seed{static_cast<seed_type>(other())},
        prng{generator_policy::make_random_generator(seed)} {}

  random_generator(random_generator &&) = default;

  random_generator &operator=(random_generator const &other) {
    seed = static_cast<seed_type>(other());
    prng = generator_policy::make_random_generator(seed);
    return *this;
  }

  random_generator &operator=(random_generator &&) = default;
  /// @}

public:
  value_type operator()() { return static_cast<value_type>(prng()); }

  seed_type get_seed() const { return seed; }

  std::ostream &operator<<(std::ostream &os) {
    os << seed;
    return os;
  }
};
} // namespace details
using details::random_generator;
} // namespace accelerando::arbitrary::random_generator
