clc; 
clear all;

Input_folder = 'D:\B-Steg\Modules\wave_tresh\images_stego\'; % folder with stego images
Output_folder = 'D:\B-Steg\Modules\wave_tresh\images_wavelet\';
% load cover image
%cover = imread(fullfile( '..','..','images_cover', '0.jpg'));
   D = dir([Input_folder '*.mat']);
   Inputs = {D.name}';
   Outputs = Inputs; % preallocate
   for k = 1:length(Inputs)
       fprintf('DWT using matlab code');
       MEXstart = tic;
       load([Input_folder Inputs{k}]);
       %% Run embedding simulation
       %[stego, ~] = HUGO_like(cover, payload, params);
       %stego=uint8(stego);
       [cover_A,cover_H,cover_V,cover_D] = dwt2(cover,'db1','mode','sym'); % дискретное двумерное вейвлет преобразование
       [stego_A,stego_H,stego_V,stego_D] = dwt2(stego,'db1','mode','sym');
       
       cover_As=wthresh(cover_A, 's', 0.1);  % м€гкий порог коефициентов изображени€ контейнера 
       cover_Hs=wthresh(cover_H, 's', 0.1);
       cover_Vs=wthresh(cover_V, 's', 0.1);
       cover_Ds=wthresh(cover_D, 's', 0.1);
       
       stego_As=wthresh(stego_A, 's', 0.1);   % м€гкий порог коефициентов стего-изображени€ 
       stego_Hs=wthresh(stego_H, 's', 0.1);
       stego_Vs=wthresh(stego_V, 's', 0.1);
       stego_Ds=wthresh(stego_D, 's', 0.1);
       
       cover_Ah=wthresh(cover_A, 'h', 0.1);  % жесткий порог коефициентов изображени€ контейнера 
       cover_Hh=wthresh(cover_H, 'h', 0.1);
       cover_Vh=wthresh(cover_V, 'h', 0.1);
       cover_Dh=wthresh(cover_D, 'h', 0.1);
       
       stego_Ah=wthresh(stego_A, 'h', 0.1);   % жесткий порог коефициентов стего-изображени€ 
       stego_Hh=wthresh(stego_H, 'h', 0.1);
       stego_Vh=wthresh(stego_V, 'h', 0.1);
       stego_Dh=wthresh(stego_D, 'h', 0.1);
           
       
       save([Output_folder Outputs{k}],'cover','cover_As','cover_Hs','cover_Vs','cover_Ds','cover_Ah','cover_Hh','cover_Vh','cover_Dh','stego','stego_As','stego_Hs','stego_Vs','stego_Ds','stego_Ah','stego_Hh','stego_Vh','stego_Dh','-mat')
       MEXend = toc(MEXstart);
       fprintf('\n\nDWT Image finished in %.2f seconds', MEXend);
       fprintf(' - DONE');
   end