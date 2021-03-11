pkg load control
pkg load signal
clear;
clf;

format long;
pi = 3.14159265358979;


% Sampling Rate
Fs = 48000;

% IEC specified frequencies
iec_f = [10, 12.5, 16, 20, 25, 31.5, 40, 50, 63, 80, ...
         100, 125, 160, 200, 250, 315, 400, 500, 630, 800, ...
         1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, ...
         10000, 12500, 16000, 20000];

% IEC Class 1 tolerances (top/bottom)
iec_c1_t_dB = [+3.5, +3.0, +2.5, +2.5, +2.5, +2.0, +1.5, +1.5, +1.5, +1.5, ...
               +1.5, +1.5, +1.5, +1.5, +1.4, +1.4, +1.4, +1.4, +1.4, +1.4, ...
               +1.1, +1.4, +1.4, +1.6, +1.6, +1.6, +1.6, +2.1, +2.1, +2.1, ...
               +2.6, +3.0, +3.5, +4.0];
iec_c1_b_dB = [-inf, -inf, -4.5, -2.5, -2.5, -2.0, -1.5, -1.5, -1.5, -1.5, ...
               -1.5, -1.5, -1.5, -1.5, -1.4, -1.4, -1.4, -1.4, -1.4, -1.4, ...
               -1.1, -1.4, -1.4, -1.6, -1.6, -1.6, -1.6, -2.1, -2.6, -3.1, ...
               -3.6, -6.0,  -17, -inf];

% IEC Class 2 tolerances (top/bottom)
iec_c2_t_dB = [+5.5, +5.5, +5.5, +3.5, +3.5, +3.5, +2.5, +2.5, +2.5, +2.5, ...
               +2.0, +2.0, +2.0, +2.0, +1.9, +1.9, +1.9, +1.9, +1.9, +1.9, ...
               +1.4, +1.9, +2.6, +2.6, +3.1, +3.1, +3.6, +4.1, +5.1, +5.6, ...
               +6.0, +6.0, +6.0, +6.0];
iec_c2_b_dB = [-inf, -inf, -inf, -3.5, -3.5, -3.5, -2.5, -2.5, -2.5, -2.5, ...
               -2.0, -2.0, -2.0, -2.0, -1.9, -1.9, -1.9, -1.9, -1.9, -1.9, ...
               -1.4, -1.9, -2.6, -2.6, -3.1, -3.1, -3.6, -4.1, -5.1, -5.6, ...
               -inf, -inf, -inf, -inf];

% Values visually estimated from datasheet
ds_dB = [ -inf,  -inf,  -inf,   -7.5,  -6,  -4.9,  -3.5,  -2.6,  -2,  -1.2, ...
          -0.4,  -0.2,  -0.1,    0,     0,     0,     0,     0,     0,     0, ...
            0,      0,     0,  0,     0,     0.1,   0.2,     0.5,  0.8,  1, ...
          1,  0.5,  -2,  -5.1];

% These value are selected and adjusted for better curve fit
ds_l_w  = [   20,  31.5,    50,  500];
ds_l_dB = [   -7.5,  -4.9,  -2.5,     0];

% Low frequency filter design
% Convert Hz in rad/s and normalize for Fs
ds_l_wn = ds_l_w.*((2*pi)/Fs);
% Convert plot decibels to magnitude
ds_l_mag = arrayfun(@db2mag, ds_l_dB);
% Estimate coefficients
[ds_l_B, ds_l_A] = invfreqz(ds_l_mag, ds_l_wn, 2, 2);
% Stabilize and normalize the filter
ds_B = polystab(ds_l_B) * norm(ds_l_B) / norm(polystab(ds_l_B));
ds_A = polystab(ds_l_A) * norm(ds_l_A) / norm(polystab(ds_l_A));
ds_H = freqz(ds_B, ds_A, iec_f, Fs);

% Equalizer filter, i.e. inverse from estimated transfer filter
% Swap A and B coefficients, and normalize to ds_B(1)
eq_B = ds_A./ds_B(1)
eq_A = ds_B./ds_B(1)
% eq_B = 1.001240684967618  -1.996936108836719   0.995703101823296
% eq_A = 1.000000000000000  -1.997675693595923   0.997677044195944
eq_H = freqz(eq_B, eq_A, iec_f, Fs);
% Check for poles ouside unit circle
roots(eq_B)
roots(eq_A)


clf;
semilogx(iec_f, ds_dB, 'g;Knowles SPH0645LM4H-B (approx.);');
hold on;
title("Knowles SPH0645LM4H-B Adjusted Frequency Response");
grid minor;
xlabel('Frequency (Hz)');
xlim([10, 24000]);
ylabel('Amplitude (dB)');
ylim([-20, 20]);
legend ('boxoff');
legend ('location', 'northwest');
semilogx(iec_f, iec_c1_t_dB, '--r;IEC 61672-1:2013 Class 1 tolerance;');
semilogx(iec_f, iec_c1_b_dB, '--r');
semilogx(iec_f, iec_c2_t_dB, 'r;IEC 61672-1:2013 Class 2 tolerance;');
semilogx(iec_f, iec_c2_b_dB, 'r');
semilogx(iec_f, 20*log10(abs(ds_H)), '--c;IIR filter frequency response;');
semilogx(iec_f, (ds_dB + 20*log10(abs(eq_H))), 'b;Adjusted frequency response;', 'linewidth', 1);
hold off;

[sos, gain] = tf2sos(eq_B, eq_A)
