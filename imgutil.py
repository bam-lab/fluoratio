# Copyright 2018 Johanan Idicula

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import matplotlib as mpl
from copy import deepcopy

import numpy as np
from scipy import ndimage as ndi
from skimage import exposure, filters, io, measure, morphology, segmentation
from skimage.filters.rank import mean
from skimage import img_as_float


# TODO: pick blob closest to bottom right corner for analysis
def mask_gen(img_filepath):
    # Open image
    img = io.imread(img_filepath)
    converted_img = img_as_float(img)
    # bilateral smoothing to preserve borders
    img_smooth = mean(converted_img, morphology.disk(10))
    # Equalize histogram of input image
    img_histeq = exposure.equalize_adapthist(img_smooth)
    # Highpass filter for image
    img_otsu = img_histeq >= filters.threshold_otsu(img_histeq)
    # generate mask
    # edges = feature.canny(filters.gaussian(img_histeq),
    #                       sigma=1,
    #                       # low_threshold=0.01*((2**16)-1),
    #                       # high_threshold=0.1*((2**16)-1)
    #                       )
    # mask = ndi.binary_fill_holes(edges)
    # mask = morphology.binary_dilation(mask)
    # mask = ndi.binary_fill_holes(mask)
    # mask = morphology.binary_opening(mask)
    # mask = ndi.binary_fill_holes(mask)
    final_mask = ndi.binary_fill_holes(img_otsu)
    # remove blobs touching border
    cleared_mask = segmentation.clear_border(final_mask)
    label_mask = img_labeler(cleared_mask)
    mask_centroids = centroids(label_mask)
    # TODO: test blob removal
    distances = []
    for centroid in mask_centroids:
        distances.append(ruler(*centroid, len(img)-1, len(img)-1))
    # Minimum distance centroid from bottom right
    try:
        min_idx = distances.index(min(distances))
        # print("southeast-most centroid index: " + str(min_idx))
        # remove labeled regions in for loop
        for idx, region in enumerate(measure.regionprops(label_mask)):
            if idx != min_idx:
                for region_coord in region.coords:
                    x = region_coord[0]
                    y = region_coord[1]
                    cleared_mask[x, y] = 0
    except ValueError:
        raise ValueError("Couldn't segment", img_filepath)
    return (img, img_smooth, img_otsu, final_mask, cleared_mask)


def img_writer(filename, img):
    io.imsave(filename + '.png', img)


def bit_conversion(input_img, current_bit_depth, new_bit_depth):
    factor = new_bit_depth/current_bit_depth
    converted = deepcopy(input_img)
    for idx, row in enumerate(input_img):
        for jdx, column in enumerate(input_img):
            converted[idx, jdx] = round(input_img[idx, jdx] * factor)
    return converted


def mask_segmenter(mask, img_filepath):
    first_px = mask[0, 0]
    assert type(first_px) is np.bool_, "input mask is not binary: %r" % mask
    img = io.imread(img_filepath)
    masked_img = deepcopy(img)
    masked_img[mask] = 0        # zeros the pixels where mask is True
    masked_segment = deepcopy(img)
    masked_segment[~mask] = 0   # zeros pixels where mask is False
    masked_img_sum = masked_img.sum()
    masked_segment_sum = masked_segment.sum()
    return masked_img, masked_img_sum, masked_segment, masked_segment_sum


def img_labeler(mask):
    label_img = measure.label(mask)
    return label_img            # Labeled array with an int for each blob


def centroids(label_img):
    centroids = []
    for region in measure.regionprops(label_img):
        centroids.append(region.centroid)
    return centroids            # list of (row, col) tuples


def area_measure(label_img):
    for region in measure.regionprops(label_img):
        mask_area = region.area
    return mask_area


def aspect_ratio(label_img):
    for region in measure.regionprops(label_img):
        major_axis = float(region.major_axis_length)
        minor_axis = float(region.minor_axis_length)
        try:
            aspect_ratio = major_axis / minor_axis
        except ZeroDivisionError:
            aspect_ratio = 0
    return aspect_ratio


def mask_test(img_filepath):
    (img, img_smooth, img_otsu, mask, cleared_mask) = mask_gen(img_filepath)
    print(str(img_filepath.split("/")[-1]))
    print("img low contrast: " + str(exposure.is_low_contrast(img)))
    print("img_histeq low contrast: " +
          str(exposure.is_low_contrast(img_otsu)))
    print("img_otsu low contrast: " + str(exposure.is_low_contrast(img_otsu)))
    # Generate plot
    fig, (ax1, ax2, ax3, ax4, ax5) = mpl.pyplot.subplots(1,
                                                         5,
                                                         figsize=(9, 3),
                                                         sharex=True,
                                                         sharey=True)
    # Display input image
    ax1.imshow(img, cmap=mpl.pyplot.cm.gray)
    ax1.axis("off")
    ax1.set_title("orig", fontsize=12)

    # Display input image
    ax2.imshow(img_smooth, cmap=mpl.pyplot.cm.gray)
    ax2.axis("off")
    ax2.set_title("histeq", fontsize=12)

    # Display histeq image
    ax3.imshow(img_otsu, cmap=mpl.pyplot.cm.gray)
    ax3.axis("off")
    ax3.set_title("otsu", fontsize=12)

    # Display otsu image
    ax4.imshow(mask, cmap=mpl.pyplot.cm.gray)
    ax4.axis("off")
    ax4.set_title("mask", fontsize=12)
    # Display mask
    ax5.imshow(cleared_mask, cmap=mpl.pyplot.cm.gray)
    ax5.axis("off")
    ax5.set_title("cleared", fontsize=12)

    filename = str(str(img_filepath.split("/")[-1]).split(".")[-2])
    fig.savefig("Results/" + filename + "plot.png")
    mpl.pyplot.close('all')
    # mpl.pyplot.show()


def ruler(y1, x1, y2, x2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5


def test():
    for i in range(1, 13):
        position_num = str('{:03d}'.format(i))
        # test_filepath_ch00 = ("/Users/johanan/prog/test/"
        #                       "Mark_and_Find_001/Position" + position_num +
        #                       "/Position" + position_num + "_t35_ch00.tif")
        test_filepath_ch00 = ("/home/jidicula/johanan/prog/test/"
                              "Mark_and_Find_001/Position" + position_num +
                              "/Position" + position_num + "_t35_ch00.tif")
        mask_test(test_filepath_ch00)
        # test_filepath_ch01 = ("/Users/johanan/prog/test/"
        #                       "Mark_and_Find_001/Position" + position_num +
        #                       "/Position" + position_num + "_t35_ch01.tif")
        test_filepath_ch01 = ("/home/jidicula/johanan/prog/test/"
                              "Mark_and_Find_001/Position" + position_num +
                              "/Position" + position_num + "_t35_ch01.tif")
        mask_test(test_filepath_ch01)
        # test_img_filepath = ("/Users/johanan/prog/test/Mark_and_Find_001/"
        #                      "Position008/Position008_t35_ch00.tif")
        # mask_test(test_img_filepath)
