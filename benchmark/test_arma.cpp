#include <stdio.h>
#include <armadillo>
#include <chrono>
#include <vector>

double average(std::vector<double> const& v) {
    if (v.empty()) return 0;

    auto const length = static_cast<float>(v.size());
    return std::accumulate(v.begin(), v.end(), 0LL) / length;
}

int main() {
    size_t n = 0;
    size_t num_occ = 0;
    std::vector<double > time_us;

    arma::arma_rng::set_seed_random();
    printf("Enter matrix size by width: ");
    scanf("%ld", &n);
    // printf("\nRandom generating matrix...\n");

    printf("Enter number of iterations: ");
    scanf("%ld", &num_occ);

    for (size_t i = 0; i < num_occ; i++) {
        // Init operands
        arma::cx_mat A = arma::cx_mat(n, n, arma::fill::randu);
        arma::cx_mat B = arma::cx_mat(n, n, arma::fill::randu);

        // Measure time
        auto start_time = std::chrono::high_resolution_clock::now();
        arma::cx_mat C = A * B;
        auto end_time = std::chrono::high_resolution_clock::now();

        // Record time
        auto duration_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(end_time - start_time).count();
        time_us.push_back(duration_ns * 0.001);

        // C.print();
    }
    
    printf("\nAverage time spent on C (A * B): %.3f (us)\n", average(time_us));
    printf("List %ld occurrences: ", num_occ);
    for (auto const& t: time_us) printf("%.3f, ", t);
    printf("\n");

    return 0;
}
