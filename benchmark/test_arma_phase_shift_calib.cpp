#include <stdio.h>
#include <armadillo>
#include <chrono>
#include <vector>

int main() {
    // size_t spatial_streams_num = 1;
    // size_t client_ul_pilot_symbols = 2;
    // size_t num_subcarrier = 768;
    // size_t num_ul_sym = 41;
    size_t spatial_streams_num = 16;
    size_t client_ul_pilot_symbols = 2;
    size_t num_subcarrier = 1200;
    size_t num_ul_sym = 13;

    size_t counter = 0;
    size_t duration_ns = 0;

    arma::arma_rng::set_seed_random();
    arma::cx_fmat mat_equaled(spatial_streams_num, 1, arma::fill::randu); // only test within [0, 1]
    arma::cx_fmat pilot_corr_mat(spatial_streams_num,
                                 client_ul_pilot_symbols,
                                 arma::fill::randu); // only test within [0, 1]

    for (size_t symbol_idx_ul = 0; symbol_idx_ul < num_ul_sym; ++symbol_idx_ul){
        for (size_t cur_sc_id = 0; cur_sc_id < num_subcarrier; ++cur_sc_id){
            if (symbol_idx_ul < client_ul_pilot_symbols) {  // Calc new phase shift
                pilot_corr_mat.randu(); // only test within [0, 1]
            }
            else if (client_ul_pilot_symbols > 0) {
                arma::fmat theta_mat = arma::arg(pilot_corr_mat);
            auto start_time = std::chrono::high_resolution_clock::now();
                arma::fmat theta_inc =
                    arma::zeros<arma::fmat>(spatial_streams_num, 1);
                for (size_t s = 1; s < client_ul_pilot_symbols; s++) {
                    arma::fmat theta_diff = theta_mat.col(s) - theta_mat.col(s - 1);
                    theta_inc += theta_diff;
                }
                theta_inc /= (float)std::max(
                    1, static_cast<int>(client_ul_pilot_symbols - 1));
    auto end_time = std::chrono::high_resolution_clock::now();
    duration_ns += std::chrono::duration_cast<std::chrono::nanoseconds>(end_time - start_time).count();
                arma::fmat cur_theta = theta_mat.col(0) + (symbol_idx_ul * theta_inc);
                arma::cx_fmat mat_phase_correct =
                    arma::zeros<arma::cx_fmat>(size(cur_theta));
                mat_phase_correct.set_real(cos(-cur_theta));
                mat_phase_correct.set_imag(sin(-cur_theta));
                mat_equaled %= mat_phase_correct;

            }
            ++counter;
        }
    }

    
    printf("Time spent on phase shift calib: %.2f (ms)\n", duration_ns * 10e-6);
    printf("Number of tasks: %.ld\n", counter);

    return 0;
}
