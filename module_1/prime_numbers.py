import cProfile
import pstats
from pstats import SortKey


def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def sum_of_primes_naive(numbers):
    """Calculate the sum of prime numbers in a list using a naive approach."""
    total = 0
    for number in numbers:
        if is_prime(number):
            total += number
    return total


def sum_of_primes_optimized(numbers):
    """Calculate the sum of prime numbers using a sieve approach."""
    if not numbers:
        return 0

    # Find the maximum number to create an appropriate sieve
    max_num = max(numbers)

    # Create a sieve (True means potentially prime)
    sieve = [True] * (max_num + 1)
    sieve[0] = sieve[1] = False

    # Apply the sieve
    for i in range(2, int(max_num**0.5) + 1):
        if sieve[i]:
            # Mark all multiples as non-prime
            for j in range(i * i, max_num + 1, i):
                sieve[j] = False

    # Sum the primes in our input list
    return sum(num for num in numbers if sieve[num])


# Create test data
numbers = list(range(1, 10000))

# Run the profiler for both implementations
print("Profiling naive implementation:")
cProfile.run("sum_of_primes_naive(numbers)", "naive_stats")
p1 = pstats.Stats("naive_stats")
p1.sort_stats(SortKey.TIME).print_stats(5)

print("\nProfiling optimized implementation:")
cProfile.run("sum_of_primes_optimized(numbers)", "optimized_stats")
p2 = pstats.Stats("optimized_stats")
p2.sort_stats(SortKey.TIME).print_stats(5)

# Compare results to ensure they match
result1 = sum_of_primes_naive(numbers)
result2 = sum_of_primes_optimized(numbers)
print(f"\nResults match: {result1 == result2}")
print(f"Sum of primes: {result1}")
