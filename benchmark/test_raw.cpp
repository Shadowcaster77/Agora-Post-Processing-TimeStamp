#include <stdio.h>
#include <complex>
#include <cstdlib> // For rand() and srand()
#include <ctime>   // For time()
#include <chrono>
#include <vector>
#include <numeric>

double average(std::vector<double> const& v) {
    if (v.empty()) return 0;

    auto const length = static_cast<float>(v.size());
    return std::accumulate(v.begin(), v.end(), 0LL) / length;
}

// Function to generate a random complex number
std::complex<double> generateRandomComplex() {
    double real = static_cast<double>(rand()) / RAND_MAX;
    double imag = static_cast<double>(rand()) / RAND_MAX;
    return std::complex<double>(real, imag);
}

// Function to generate a random complex square matrix of given size
std::vector<std::vector<std::complex<double>>> generateRandomComplexMatrix(
    int size) {
    std::vector<std::vector<std::complex<double>>> matrix(
            size, std::vector<std::complex<double>>(size));
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            matrix[i][j] = generateRandomComplex();
        }
    }
    return matrix;
}

// Function to perform complex square matrix multiplication
std::vector<std::vector<std::complex<double>>> complexMatrixMultiplication(
    const std::vector<std::vector<std::complex<double>>>& A,
    const std::vector<std::vector<std::complex<double>>>& B
) {
    int size = A.size();

    std::vector<std::vector<std::complex<double>>> result(
        size, std::vector<std::complex<double>>(size, 0.0));

    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            for (int k = 0; k < size; ++k) {
                result[i][j] += A[i][k] * B[k][j];
            }
        }
    }

    return result;
}

int main() {
    size_t n = 0;
    size_t num_occ = 0;
    std::vector<double > time_us;

    // Seed the random number generator with the current time
    srand(static_cast<unsigned>(time(0)));
    printf("Enter matrix size by width: ");
    scanf("%ld", &n);
    // printf("\nRandom generating matrix...\n");

    printf("Enter number of iterations: ");
    scanf("%ld", &num_occ);

    for (size_t i = 0; i < num_occ; i++) {
        // Init operands
        std::vector<std::vector<std::complex<double>>> A =
            generateRandomComplexMatrix(n);
        std::vector<std::vector<std::complex<double>>> B =
            generateRandomComplexMatrix(n);

        // Measure time
        auto start_time = std::chrono::high_resolution_clock::now();
        std::vector<std::vector<std::complex<double>>> C =
            complexMatrixMultiplication(A, B);
        auto end_time = std::chrono::high_resolution_clock::now();

        // Record time
        auto duration_ns =
            std::chrono::duration_cast<std::chrono::nanoseconds>(
                    end_time - start_time).count();
        time_us.push_back(duration_ns * 0.001);
    }

    printf("\nAverage time spent on C = A * B: %.3f (us)\n", average(time_us));
    // printf("List %ld occurrences: ", num_occ);
    // for (auto const& t: time_us) printf("%.3f, ", t);
    printf("\n");

    return 0;
}
