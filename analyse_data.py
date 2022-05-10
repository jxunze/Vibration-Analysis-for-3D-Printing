import os
import numpy as np
from PIL import Image

import stl_functions
from save_to_npy import cache_processed_data
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks, argrelextrema,butter,filtfilt


build_plate_end = 1 - (79.5/577) #data obtained from E290 platform position ranges
build_plate_start = 1 - (329.5/577)
LAYER_HEIGHT = 40 * (10**-3)
BUILD_PLATE_LENGTH = 250


def butter_lowpass_filter(data, cutoff, fs, order):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y


def get_useful_region(data):
    # smoothed = np.array(savgol_filter(data, 11, 1))

    # print(np.where(np.isnan(data)))
    data[np.isnan(data)] = 0
    threshold = np.percentile(data, 65)
    smoothed = butter_lowpass_filter(data, cutoff=50, fs=500, order=5)
    hist, bin_edges = np.histogram(smoothed, bins=500)
    # plt.plot(bin_edges[1:],hist,'.-')
    # plt.plot([threshold,threshold],[0,1e6],'r--')
    # plt.vlines(threshold,0,1e6)
    # plt.show()

    # print(smoothed)
    # smoothed = data.copy()

    clipped = smoothed.copy()
    thresholded = np.ones(np.shape(smoothed))
    thresholded[smoothed < threshold] = 0

    processed_A = np.array(savgol_filter(thresholded, 21, 1))
    processed_B = np.where(processed_A > 0.2, 1, 0)
    processed_C = np.array(savgol_filter(processed_B, 21, 1))
    processed_D = np.where(processed_C > 0.2, 1, 0)

    processed_E = np.array(savgol_filter(processed_D, 21, 1))
    processed_F = np.where(processed_E > 0.2, 1, 0)

    # plt.plot(data,linewidth=1)
    # #plt.plot(smoothed+0.5,linewidth=1)
    # #plt.plot(thresholded,linewidth=1)
    # #ax = plt.plot(processed_A,linewidth=1)
    # #ax = plt.plot(processed_B,linewidth=1)
    # ax = plt.plot(processed_F,linewidth=1)
    # plt.hlines(threshold,0,1e5,zorder=100)
    # print(threshold)
    # plt.show()
    plt.figure()
    plt.plot(processed_F)
    plt.plot(data)
    plt.show()
    zero_data = list(np.where(processed_F == 0)[0])
    gaps = [[s, e] for s, e in zip(zero_data, zero_data[1:]) if s + 1 < e]
    edges = iter(zero_data[:1] + sum(gaps, []) + zero_data[-1:])
    consecutive = list(zip(edges, edges))
    for x in consecutive:
        if x[1] - x[0] < 200:
            processed_F[x[0]:x[1] + 1] = 1
    nonzero_data = list(np.where(processed_F != 0)[0])
    gaps = [[s, e] for s, e in zip(nonzero_data, nonzero_data[1:]) if s + 1 < e]
    edges = iter(nonzero_data[:1] + sum(gaps, []) + nonzero_data[-1:])
    consecutive = list(zip(edges, edges))
    essential_regions = []
    for x in consecutive:
        if x[1] - x[0] < 1500:
            processed_F[x[0]:x[1] + 1] = 0
        else:
            essential_regions.append(
                (int(x[0] + (x[1] - x[0]) * build_plate_start), int(x[0] + (x[1] - x[0]) * build_plate_end)))
    # plt.plot(smoothed)
    # plt.figure()
    # for x in essential_regions:
    #     plt.plot(data[x[0]:x[1]+1])
    np.save("essential_regions.npy", essential_regions)
    return essential_regions

def get_outliers(data):
    q3, q1 = np.percentile(data, [75 ,25])
    iqr = q3-q1
    outliers = []
    outliers = data[data>q3+10*iqr]
    return len(outliers),outliers

def remove_extreme_cases(data):
    q3, q1 = np.percentile(data, [75, 25])
    iqr = q3 - q1
    threshold = q3 + 15 * iqr
    positions_of_outliers = np.argwhere(data > threshold)
    data[data > threshold] = np.median(data)
    return data, positions_of_outliers

def plot_data(data):
    plt.figure()
    plt.imshow(data, cmap="Blues",origin='lower')
    plt.colorbar()
    plt.title("2-D Heat Map")

def plot_heatmap_and_stl(data):
    fig = plt.figure(dpi=300)
    plt.rcParams.update({'font.size': 6})
    im = Image.open('final_stl_image.png')
    CAD_shape = im.size
    data_shape = data.shape
    image_pxwidth, image_pxheight = CAD_shape[0], CAD_shape[1]
    plt.imshow(data, cmap="Blues")
    plt.colorbar()
    (plot_pxwidth, plot_pxheight) = fig.get_size_inches() * fig.dpi
    height_of_stl_print = image_pxheight/image_pxwidth * BUILD_PLATE_LENGTH
    height_of_recorded_print = data_shape[0]*LAYER_HEIGHT
    final_image_resolution = (int(plot_pxwidth),int((height_of_stl_print/height_of_recorded_print)*plot_pxheight))
    final_CAD_image = im.resize(final_image_resolution)
    plt.imshow(im,origin='upper', extent = [0, data_shape[1], 0, data_shape[0] * (height_of_stl_print / height_of_recorded_print)])
    # extent = [0, data_shape[1], 0, data_shape[0] * (height_of_stl_print / height_of_recorded_print)]
    # plt.imshow(CAD_view, origin='upper', extent=[0,CAD_shape[1], 0, data_shape[0]])

def normalise_data(data,regions_of_interest):
    data_array = []
    for x in regions_of_interest:
        data_array.append(savgol_filter(data[x[0]:x[1]], 7, 3)[::-1])
    data_reshaped = np.zeros([len(data_array), len(max(data_array, key=lambda x: len(x)))])
    for i, j in enumerate(data_array):
        # data_reshaped[i].fill(np.median(j))
        data_reshaped[i][0:len(j)] = j
    cleaned_data, outlier_positions = remove_extreme_cases(data_reshaped)
    flattened_data = cleaned_data.flatten()
    min_value, max_value = min(flattened_data), max(flattened_data)
    normalised_data = (cleaned_data-min_value)/(max_value-min_value)
    for x in outlier_positions:
        normalised_data[x[0]][x[1]] = 1

    return normalised_data


def main():
    if not os.path.isfile("df.npy"):
        cache_processed_data("putty_arduino.csv")
    data = np.load('df.npy')

    y_plots = np.abs(data[:,1:2]-np.median(data[:,1:2])).flatten()
    z_plots = np.abs(data[:,2:3]).flatten()
    x_plots = np.abs(data[:,3:]).flatten()

    if not os.path.isfile("essential_regions.npy"):
        regions_of_interest = get_useful_region(np.diff(data[:,3:],axis=0).flatten())
    else:
        regions_of_interest = np.load("essential_regions.npy")

    '''
    #plot for each axis
    plt.figure()
    for x in essential_regions[1:]:
        plt.plot(y_plots[x[0]:x[1]], linewidth=1,alpha=0.5)
    plt.figure()
    for x in essential_regions[1:]:
        plt.plot(z_plots[x[0]:x[1]], linewidth=1, alpha=0.5)
    plt.figure()
    for x in essential_regions[1:]:
        plt.plot(x_plots[x[0]:x[1]], linewidth=1, alpha=0.5)
    '''
    normalised_data_z = normalise_data(x_plots, regions_of_interest)
    # normalised_data_y = normalise_data(z_plots, regions_of_interest)
    # normalised_data_x = normalise_data(y_plots, regions_of_interest)

    stl_functions.get_stl("Overhand.stl")
    plot_heatmap_and_stl(normalised_data_z)

    plt.show()


if __name__ == "__main__":
    main()