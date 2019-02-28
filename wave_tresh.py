import copy
import math
import multiprocessing as MP
from multiprocessing import Pool
import time
import os
from PIL import Image

import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import misc
from sklearn.datasets import make_sparse_coded_signal
from sklearn.linear_model import OrthogonalMatchingPursuit
from scipy.io import loadmat
from scipy.io import savemat


res_Metric_MSE = []
res_Metric_PSNR = []
res_Metric_NCC = []
res_Metric_SSIM = []

size = 1024

#worker_number = MP.cpu_count() if MP.cpu_count() != 1 else 1
#worker_number=3

def Metric_MSE(C, S):
    return np.power(C - S, 2).sum() / C.size

def Metric_PSNR(C, S):
    MSE = Metric_MSE(C, S)

    if MSE == 0:
        PSNR = float('inf')
    else:
        PSNR = 10 * math.log10((255**2)/MSE)
    # else:
    # print MSE
    # try:
    #     PSNR = 10 * math.log10((255**2)/MSE)
    # # this is useless, but let's leave it here
    # except ZeroDivisionError:
    #     print 'HERE'
    #     PSNR = float('inf')

    return PSNR

def corr_calc(sig1, sig2):
    sig1 = sig1.astype(float)
    sig2 = sig2.astype(float)

    cov = np.mean((sig1 - sig1.mean()) * (sig2 - sig2.mean()))
    std1 = np.std(sig1)
    std2 = np.std(sig2)

    return cov / (std1 * std2)


def Metric_NCC(C, S):
    MeanC = np.mean(C)
    MeanS = np.mean(S)
    VarC = np.std(C)
    VarS = np.std(S)
    VarCS = np.multiply(C - MeanC, S - MeanS).sum() / C.size
    div = (VarC * VarS)
    if div == 0:
        return float('inf')
    return VarCS / div


def Metric_SSIM(C, S):
    MeanC = np.mean(C)
    MeanS = np.mean(S)
    VarC = np.std(C)
    VarS = np.std(S)
    metricNCC = Metric_NCC(C, S)
    if metricNCC == float('inf'):
        return metricNCC
    SSIM = metricNCC * \
           ((2 * MeanC * MeanS) / (MeanC ** 2 + MeanS ** 2)) * \
           ((2 * VarC * VarS) / (VarC ** 2 + VarS ** 2))

    if (SSIM > 1):
        return 1
    elif (SSIM < 0):
        return math.fabs(SSIM)
    else:
        return SSIM

def create_list_files(target_format_in, path_in):
    # function for creation list of files to be processed

    file_list = list()
    for root, _, files in os.walk(path_in):
        for curr_file in files:
            if target_format_in in curr_file:
                file_list.append(root + curr_file)
    return file_list





if __name__ == "__main__":


    file_list_wavetresh = create_list_files(target_format_in='.mat',
                                                path_in='D:\\B-Steg\\Modules\\wave_tresh\\images_wavelet\\')

    for i in np.arange(file_list_wavetresh.__len__()):
        matfile_list = loadmat(file_list_wavetresh[i])

        res_Metric_MSE.append([])
        res_Metric_PSNR.append([])
        res_Metric_NCC.append([])
        res_Metric_SSIM.append([])

        Metric_MSE_sAcoef = Metric_MSE(matfile_list['cover_As'], matfile_list['stego_As'])
        Metric_MSE_sHcoef = Metric_MSE(matfile_list['cover_Hs'], matfile_list['stego_Hs'])
        Metric_MSE_sVcoef = Metric_MSE(matfile_list['cover_Vs'], matfile_list['stego_Vs'])
        Metric_MSE_sDcoef = Metric_MSE(matfile_list['cover_Ds'], matfile_list['stego_Ds'])

        Metric_MSE_hAcoef = Metric_MSE(matfile_list['cover_Ah'], matfile_list['stego_Ah'])
        Metric_MSE_hHcoef = Metric_MSE(matfile_list['cover_Hh'], matfile_list['stego_Hh'])
        Metric_MSE_hVcoef = Metric_MSE(matfile_list['cover_Vh'], matfile_list['stego_Vh'])
        Metric_MSE_hDcoef = Metric_MSE(matfile_list['cover_Dh'], matfile_list['stego_Dh'])

        Metric_PSNR_sAcoef = Metric_PSNR(matfile_list['cover_As'], matfile_list['stego_As'])
        Metric_PSNR_sHcoef = Metric_PSNR(matfile_list['cover_Hs'], matfile_list['stego_Hs'])
        Metric_PSNR_sVcoef = Metric_PSNR(matfile_list['cover_Vs'], matfile_list['stego_Vs'])
        Metric_PSNR_sDcoef = Metric_PSNR(matfile_list['cover_Ds'], matfile_list['stego_Ds'])

        Metric_PSNR_hAcoef = Metric_PSNR(matfile_list['cover_Ah'], matfile_list['stego_Ah'])
        Metric_PSNR_hHcoef = Metric_PSNR(matfile_list['cover_Hh'], matfile_list['stego_Hh'])
        Metric_PSNR_hVcoef = Metric_PSNR(matfile_list['cover_Vh'], matfile_list['stego_Vh'])
        Metric_PSNR_hDcoef = Metric_PSNR(matfile_list['cover_Dh'], matfile_list['stego_Dh'])

        Metric_NCC_sAcoef = Metric_NCC(matfile_list['cover_As'], matfile_list['stego_As'])
        Metric_NCC_sHcoef = Metric_NCC(matfile_list['cover_Hs'], matfile_list['stego_Hs'])
        Metric_NCC_sVcoef = Metric_NCC(matfile_list['cover_Vs'], matfile_list['stego_Vs'])
        Metric_NCC_sDcoef = Metric_NCC(matfile_list['cover_Ds'], matfile_list['stego_Ds'])

        Metric_NCC_hAcoef = Metric_NCC(matfile_list['cover_Ah'], matfile_list['stego_Ah'])
        Metric_NCC_hHcoef = Metric_NCC(matfile_list['cover_Hh'], matfile_list['stego_Hh'])
        Metric_NCC_hVcoef = Metric_NCC(matfile_list['cover_Vh'], matfile_list['stego_Vh'])
        Metric_NCC_hDcoef = Metric_NCC(matfile_list['cover_Dh'], matfile_list['stego_Dh'])

        Metric_SSIM_sAcoef = Metric_NCC(matfile_list['cover_As'], matfile_list['stego_As'])
        Metric_SSIM_sHcoef = Metric_NCC(matfile_list['cover_Hs'], matfile_list['stego_Hs'])
        Metric_SSIM_sVcoef = Metric_NCC(matfile_list['cover_Vs'], matfile_list['stego_Vs'])
        Metric_SSIM_sDcoef = Metric_NCC(matfile_list['cover_Ds'], matfile_list['stego_Ds'])

        Metric_SSIM_hAcoef = Metric_SSIM(matfile_list['cover_Ah'], matfile_list['stego_Ah'])
        Metric_SSIM_hHcoef = Metric_SSIM(matfile_list['cover_Hh'], matfile_list['stego_Hh'])
        Metric_SSIM_hVcoef = Metric_SSIM(matfile_list['cover_Vh'], matfile_list['stego_Vh'])
        Metric_SSIM_hDcoef = Metric_SSIM(matfile_list['cover_Dh'], matfile_list['stego_Dh'])

        res_Metric_MSE[i].append(Metric_MSE_sAcoef)
        res_Metric_MSE[i].append(Metric_MSE_sHcoef)
        res_Metric_MSE[i].append(Metric_MSE_sVcoef)
        res_Metric_MSE[i].append(Metric_MSE_sDcoef)
        res_Metric_MSE[i].append(Metric_MSE_hAcoef)
        res_Metric_MSE[i].append(Metric_MSE_hHcoef)
        res_Metric_MSE[i].append(Metric_MSE_hVcoef)
        res_Metric_MSE[i].append(Metric_MSE_hDcoef)

        res_Metric_PSNR[i].append(Metric_PSNR_sAcoef)
        res_Metric_PSNR[i].append(Metric_PSNR_sHcoef)
        res_Metric_PSNR[i].append(Metric_PSNR_sVcoef)
        res_Metric_PSNR[i].append(Metric_PSNR_sDcoef)
        res_Metric_PSNR[i].append(Metric_PSNR_hAcoef)
        res_Metric_PSNR[i].append(Metric_PSNR_hHcoef)
        res_Metric_PSNR[i].append(Metric_PSNR_hVcoef)
        res_Metric_PSNR[i].append(Metric_PSNR_hDcoef)

        res_Metric_NCC[i].append(Metric_NCC_sAcoef)
        res_Metric_NCC[i].append(Metric_NCC_sHcoef)
        res_Metric_NCC[i].append(Metric_NCC_sVcoef)
        res_Metric_NCC[i].append(Metric_NCC_sDcoef)
        res_Metric_NCC[i].append(Metric_NCC_hAcoef)
        res_Metric_NCC[i].append(Metric_NCC_hHcoef)
        res_Metric_NCC[i].append(Metric_NCC_hVcoef)
        res_Metric_NCC[i].append(Metric_NCC_hDcoef)

        res_Metric_SSIM[i].append(Metric_SSIM_sAcoef)
        res_Metric_SSIM[i].append(Metric_SSIM_sHcoef)
        res_Metric_SSIM[i].append(Metric_SSIM_sVcoef)
        res_Metric_SSIM[i].append(Metric_SSIM_sDcoef)
        res_Metric_SSIM[i].append(Metric_SSIM_hAcoef)
        res_Metric_SSIM[i].append(Metric_SSIM_hHcoef)
        res_Metric_SSIM[i].append(Metric_SSIM_hVcoef)
        res_Metric_SSIM[i].append(Metric_SSIM_hDcoef)

    res_Metric_MSE = np.array(res_Metric_MSE)
    res_Metric_PSNR = np.array(res_Metric_PSNR)
    res_Metric_NCC = np.array(res_Metric_NCC)
    res_Metric_SSIM = np.array(res_Metric_SSIM)

plt.figure(1)
plt.plot(res_Metric_MSE[:,0], label="MSE sAcoef")
plt.plot(res_Metric_MSE[:,1], label="MSE sHcoef")
plt.plot(res_Metric_MSE[:,2], label="MSE sVcoef")
plt.plot(res_Metric_MSE[:,3], label="MSE sDcoef")
plt.grid()
plt.legend(loc=1)
#plt.xlabel ('payload')
plt.ylabel ('MSE')
plt.title ('Results MSE_s_thresh')

plt.figure(2)
plt.plot(res_Metric_MSE[:,4], label="MSE hAcoef")
plt.plot(res_Metric_MSE[:,5], label="MSE hHcoef")
plt.plot(res_Metric_MSE[:,6], label="MSE hVcoef")
plt.plot(res_Metric_MSE[:,7], label="MSE hDcoef")
plt.grid()
plt.legend(loc=1)
#plt.xlabel ('payload')
plt.ylabel ('MSE')
plt.title ('Results MSE_h_thresh')

plt.figure(3)
plt.plot(res_Metric_PSNR[:,0], label="PSNR sAcoef")
plt.plot(res_Metric_PSNR[:,1], label="PSNR sHcoef")
plt.plot(res_Metric_PSNR[:,2], label="PSNR sVcoef")
plt.plot(res_Metric_PSNR[:,3], label="PSNR sDcoef")
plt.grid()
plt.legend(loc=1)
#plt.xlabel ('payload')
plt.ylabel ('PSNR')
plt.title ('Results PSNR_s_thresh')

plt.figure(4)
plt.plot(res_Metric_PSNR[:,4], label="PSNR hAcoef")
plt.plot(res_Metric_PSNR[:,5], label="PSNR hHcoef")
plt.plot(res_Metric_PSNR[:,6], label="PSNR hVcoef")
plt.plot(res_Metric_PSNR[:,7], label="PSNR hDcoef")
plt.grid()
plt.legend(loc=1)
#plt.xlabel ('payload')
plt.ylabel ('PSNR')
plt.title ('Results PSNR_h_thresh')

plt.figure(5)
plt.plot(res_Metric_NCC[:,0], label="NCC sAcoef")
plt.plot(res_Metric_NCC[:,1], label="NCC sHcoef")
plt.plot(res_Metric_NCC[:,2], label="NCC sVcoef")
plt.plot(res_Metric_NCC[:,3], label="NCC sDcoef")
plt.grid()
plt.legend(loc=1)
#plt.xlabel ('payload')
plt.ylabel ('NCC')
plt.title ('Results NCC_s_thresh')

plt.figure(6)
plt.plot(res_Metric_NCC[:,4], label="NCC hAcoef")
plt.plot(res_Metric_NCC[:,5], label="NCC hHcoef")
plt.plot(res_Metric_NCC[:,6], label="NCC hVcoef")
plt.plot(res_Metric_NCC[:,7], label="NCC hDcoef")
plt.grid()
plt.legend(loc=1)
#plt.xlabel ('payload')
plt.ylabel ('NCC')
plt.title ('Results NCC_h_thresh')

plt.figure(7)
plt.plot(res_Metric_SSIM[:,0], label="SSIM sAcoef")
plt.plot(res_Metric_SSIM[:,1], label="SSIM sHcoef")
plt.plot(res_Metric_SSIM[:,2], label="SSIM sVcoef")
plt.plot(res_Metric_SSIM[:,3], label="SSIM sDcoef")
plt.grid()
plt.legend(loc=1)
#plt.xlabel ('payload')
plt.ylabel ('SSIM')
plt.title ('Results SSIM_s_thresh')

plt.figure(8)
plt.plot(res_Metric_SSIM[:,4], label="SSIM hAcoef")
plt.plot(res_Metric_SSIM[:,5], label="SSIM hHcoef")
plt.plot(res_Metric_SSIM[:,6], label="SSIM hVcoef")
plt.plot(res_Metric_SSIM[:,7], label="SSIM hDcoef")
plt.grid()
plt.legend(loc=1)
#plt.xlabel ('payload')
plt.ylabel ('SSIM')
plt.title ('Results SSIM_h_thresh')

plt.show()

print "All is OK"