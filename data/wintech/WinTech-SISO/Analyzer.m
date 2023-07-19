clear;
close all;
clc;

tokenList = [5 10 15 20 25 30];
percent = 0.95;
snrDelta = 1;
polar = "H";
mcsList = [
    "16QAM-"+polar+"-333-csv" ...
    "16QAM-"+polar+"-500-csv" ...
    "16QAM-"+polar+"-666-csv" ...
    "64QAM-"+polar+"-333-csv" ...
    "64QAM-"+polar+"-500-csv" ...
    "64QAM-"+polar+"-666-csv"];

snrList = NaN(length(mcsList), length(tokenList));
evmList = NaN(length(mcsList), length(tokenList));
berList = NaN(length(mcsList), length(tokenList));
for mcsIdx = 1: length(mcsList)
    mcs = mcsList(mcsIdx);
    
%     figure(11);
%     hold on;
    for tokenIdx = 1: length(tokenList)
        token = tokenList(tokenIdx);
    
        folder = mcs+"/" + token + "/";
        if exist(folder+"log-ulsnr-BS.csv", 'file')
            csv = csvread(folder+"log-ulsnr-BS.csv");
            snrTemp = csv(1: end-1, 2);
        else
            continue;
        end
        if exist(folder+"log-evm-BS.csv", 'file')
            csv = csvread(folder+"log-evm-BS.csv");
            evmTemp = csv(:, 2);
        else
            continue;
        end
        if exist(folder+"log-ber-BS.csv", 'file')
            csv = csvread(folder+"log-ber-BS.csv");
            berTemp = csv(:, 2);
        else
            continue;
        end
        dataNum = min([length(snrTemp) length(evmTemp) length(berTemp)]);
        snrTemp = snrTemp(1: dataNum);
        evmTemp = evmTemp(1: dataNum);
        berTemp = berTemp(1: dataNum);
    
        snr = median(snrTemp);
        snrList(mcsIdx, tokenIdx) = snr;
        index = find(abs(snrTemp-snr)<=snrDelta);
        dataNum = length(index);

        snr = snrTemp(index);
        snrList(mcsIdx, tokenIdx) = mean(snr);
        evm = sqrt(sort(evmTemp(index))/100)*100;
        evmList(mcsIdx, tokenIdx) = mean(evm(1: round(percent*dataNum)));
        ber = sort(berTemp(index));
        berList(mcsIdx, tokenIdx) = mean(ber(1: round(percent*dataNum)));
    end
end

figure(1);
hold on;
for mcsIdx = 1: length(mcsList)
    plot(snrList(mcsIdx, :), evmList(mcsIdx, :), '+-', 'LineWidth', 2);
end
legend(mcsList);
saveas(gca, "SISO_"+polar+"_EVM.png");

figure(2);
hold on;
for mcsIdx = 1: length(mcsList)
    plot(snrList(mcsIdx, :), berList(mcsIdx, :), '+-', 'LineWidth', 2);
end
legend(mcsList);
saveas(gca, "SISO_"+polar+"_BER.png");

save("result_SISO_"+polar+".mat", "snrList", "evmList", "berList");