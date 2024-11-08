#include <stdio.h>
#include <armadillo>
#include <chrono>
#include <vector>

static inline size_t read_nano_sec(
        std::chrono::_V2::system_clock::time_point t0,
        std::chrono::_V2::system_clock::time_point t1) {
    return std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count();
}

int main() {
    size_t spatial_streams_num = 1;
    size_t client_ul_pilot_symbols = 2;
    size_t num_subcarrier = 768;
    size_t num_ul_sym = 16;
    // size_t spatial_streams_num = 16;
    // size_t client_ul_pilot_symbols = 2;
    // size_t num_subcarrier = 1200;
    // size_t num_ul_sym = 13;

    size_t counter = 0;
    // size_t duration_ns = 0;
    size_t duration_ns[6] = {0};

    arma::arma_rng::set_seed_random();
    arma::cx_fmat mat_equaled(spatial_streams_num, 1, arma::fill::randu); // only test within [0, 1]
    arma::cx_fmat pilot_corr_mat(spatial_streams_num,
                                 client_ul_pilot_symbols,
                                 arma::fill::randn); // only test within [0, 1]
    arma::fmat theta_mat;
    arma::fmat theta_inc;

    auto start = std::chrono::high_resolution_clock::now();

    for (size_t symbol_idx_ul = 0; symbol_idx_ul < num_ul_sym; ++symbol_idx_ul){
        for (size_t cur_sc_id = 0; cur_sc_id < num_subcarrier; ++cur_sc_id){
            if (symbol_idx_ul < client_ul_pilot_symbols) {  // Calc new phase shift
                auto time_0 = std::chrono::high_resolution_clock::now();
                pilot_corr_mat.randn(); // only test within [0, 1]
                auto time_1 = std::chrono::high_resolution_clock::now();
                duration_ns[0] += read_nano_sec(time_0, time_1);
            }
            else if (symbol_idx_ul == client_ul_pilot_symbols && cur_sc_id == 0) {
                    auto time_2 = std::chrono::high_resolution_clock::now();
                theta_mat = arma::arg(pilot_corr_mat);
                    auto time_3 = std::chrono::high_resolution_clock::now();
                    duration_ns[1] += read_nano_sec(time_2, time_3);
                    time_3 = std::chrono::high_resolution_clock::now();
                theta_inc =
                    arma::zeros<arma::fmat>(spatial_streams_num, 1);
                for (size_t s = 1; s < client_ul_pilot_symbols; s++) {
                    arma::fmat theta_diff = theta_mat.col(s) - theta_mat.col(s - 1);
                    theta_inc += theta_diff;
                }
                theta_inc /= (float)std::max(
                    1, static_cast<int>(client_ul_pilot_symbols - 1));
                    auto time_4 = std::chrono::high_resolution_clock::now();
                    duration_ns[2] += read_nano_sec(time_3, time_4);
            }
            else if (symbol_idx_ul >= client_ul_pilot_symbols) {
                    auto time_4 = std::chrono::high_resolution_clock::now();
                arma::fmat cur_theta = theta_mat.col(0) + (symbol_idx_ul * theta_inc);
                    auto time_5 = std::chrono::high_resolution_clock::now();
                    duration_ns[3] += read_nano_sec(time_4, time_5);
                    time_5 = std::chrono::high_resolution_clock::now();
                arma::cx_fmat mat_phase_correct =
                    arma::zeros<arma::cx_fmat>(size(cur_theta));
                mat_phase_correct.set_real(cos(-cur_theta));
                mat_phase_correct.set_imag(sin(-cur_theta));
                    auto time_6 = std::chrono::high_resolution_clock::now();
                    duration_ns[4] += read_nano_sec(time_5, time_6);
                    time_6 = std::chrono::high_resolution_clock::now();
                mat_equaled %= mat_phase_correct;
                    auto time_7 = std::chrono::high_resolution_clock::now();
                    duration_ns[5] += read_nano_sec(time_6, time_7);
            }
            ++counter;
        }
    }

    auto end = std::chrono::high_resolution_clock::now();

    for (size_t i = 0; i < 6; ++i) {
        printf("Time spent on phase shift calib part [%ld]: %.2f (ms)\n",
            i, duration_ns[i] * 10e-6);
    }
    printf("Number of tasks: %.ld\n", counter);
    auto total_ns =
        std::chrono::duration_cast<std::chrono::nanoseconds>(
            end - start).count();
    printf("Total time: %.2f (ms)\n", total_ns * 10e-6);
    
    return 0;
}
