clear;
close all;
clc;

tokenList = ["5" "10" "13" "15" "20" "25" "30"];
percent = 0.95;
snrDelta = 1;
polar = "H";
mcsList = [
    "16QAM-333" ...
    "16QAM-500" ...
    "16QAM-666" ...
    "64QAM-333" ...
    "64QAM-500" ...
    "64QAM-666"];

snrList = NaN(length(mcsList), length(tokenList));
snrAll = NaN(length(mcsList), length(tokenList), 20000);
evmList = NaN(length(mcsList), length(tokenList));
evmAll = NaN(length(mcsList), length(tokenList), 20000);
berList = NaN(length(mcsList), length(tokenList));
berAll = NaN(length(mcsList), length(tokenList), 20000);
if polar == "H"
    column = 2;
else
    column = 3;
end
for mcsIdx = 1: length(mcsList)
    mcs = mcsList(mcsIdx);
    
%     figure(11);
%     hold on;
    for tokenIdx = 1: length(tokenList)
        token = tokenList(tokenIdx);
    
        folder = mcs+"/" + token + "/";
        if exist(folder+"log-ulsnr-BS.csv", 'file')
            csv = csvread(folder+"log-ulsnr-BS.csv");
            snrTemp = csv(1: end-1, column);
        else
            continue;
        end
        if exist(folder+"log-evm-BS.csv", 'file')
            csv = csvread(folder+"log-evm-BS.csv");
            evmTemp = csv(:, column);
        else
            continue;
        end
        if exist(folder+"log-ber-BS.csv", 'file')
            csv = csvread(folder+"log-ber-BS.csv");
            berTemp = csv(:, column);
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
        snrAll(mcsIdx, tokenIdx, 1: dataNum) = snr;
        evm = sqrt(sort(evmTemp(index))/100)*100;
        evmList(mcsIdx, tokenIdx) = mean(evm(1: round(percent*dataNum)));
        evmAll(mcsIdx, tokenIdx, 1: dataNum) = evm;
        ber = sort(berTemp(index));
        berList(mcsIdx, tokenIdx) = mean(ber(1: round(percent*dataNum)));
        berAll(mcsIdx, tokenIdx, 1: dataNum) = ber;
    end
end

figure(1);
hold on;
for mcsIdx = 1: length(mcsList)
    plot(snrList(mcsIdx, :), evmList(mcsIdx, :), '+-', 'LineWidth', 2);
end
legend(mcsList);
saveas(gca, "MIMO_"+polar+"_EVM.png");

figure(2);
hold on;
for mcsIdx = 1: length(mcsList)
    plot(snrList(mcsIdx, :), berList(mcsIdx, :), '+-', 'LineWidth', 2);
end
legend(mcsList);
saveas(gca, "MIMO_"+polar+"_BER.png");

for mcsIdx = 1: length(mcsList)
    mcs = mcsList(mcsIdx);

    figure(11);
    hold off;
    for tokenIdx = 1: length(tokenList)
        cdfplot(evmAll(mcsIdx, tokenIdx, :));
        hold on;
    end
    legend(tokenList);
    xlim([0 200]);
    saveas(gcf, "MIMO_CDF_"+polar+"_"+mcs+"_EVM.png");

    figure(12);
    hold off;
    for tokenIdx = 1: length(tokenList)
        cdfplot(berAll(mcsIdx, tokenIdx, :));
        hold on;
    end
    legend(tokenList);
    xlim([0 0.5]);
    saveas(gcf, "MIMO_CDF_"+polar+"_"+mcs+"_BER.png");
end

save("result_MIMO_"+polar+".mat", "snrList", "evmList", "berList");