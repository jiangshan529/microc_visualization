#!/usr/bin/env python # [1]
"""\
This script contains all the functions 
used for region visualization in the paper
"Putative Looping Factor ZNF143/ZFP143 is 
an Essential Transcriptional Regulator with No Looping Function"

Author: Domenic Narducci
"""

# Package imports
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable
import cooler
import bioframe
import cooltools
from cooltools import expected_cis, expected_trans
from cooltools.lib import plotting
import cooler as clr
import h5py
import coolbox
from coolbox.api import *
from coolbox.utilities import GenomeRange
from pygenometracks import readBed, readGtf
from pygenometracks.tracks import BedTrack
import matplotlib as mpl
mpl.rcParams['pdf.fonttype']=42

# Define plotting aesthetics as global variables
HIGHLIGHT_PARAMS = {"color":"gray",
                   "alpha":0.05,
                   "border_line":False}



SPACER_HEIGHT = 0.4
DEFAULT_COLOR_LIST = ["#FF0000", "#00FA00", "#0000FF", "#A0F000"]
PRO_SEQ_TRACK_HEIGHT = 1.2
ANNOTATIONS_PARAMS = [{"height":1},
                      {"file": "/broad/boxialab/shawn/projects/genome_sequence/human/hg38/HG38_annotation_bed6.bed", # PATH TO BED FILE OF GENE ANNOTATIONS
                       "max_labels":1000,
                       "merge_transcripts":True, 
                       "gene_rows":3}]

def cat_prefix_to_list(prefix, file_list):
    """
    Helper function that concatenates a prefix to every element
    in a list. 
    """
    return [os.path.join(prefix, file) for file in file_list]

def make_region_plot(region, resolution, highlight_region_list, microc_file, microc_title,
                     chip_list_list, forward_proseq_list, reverse_proseq_list, condition_order, 
                     bed_files, bigwig_bins=3600, highlight_buffer=1000, pro_bins=None):
    
    """
    Function that makes a plot of a region with Micro-C, ChIP-seq, and Pro-seq.
    
    region: (str) string that specifies region for plotting.
    resolution: (int) resolution of micro-c map used
    highlight_region_list: List of regions of format [chr, start, end] to highlight
    microc_file: (str) file path to micro-c data
    microc_title: (str) title for micro-c
    chip_list_list: List of lists containing paths to bigwigs
    forward_proseq_list: List of paths to forward strand pro-seq files
    reverse_proseq_list: List of paths to reverse strand pro-seq files
    condition_order: List indicating order of conditions to plot. 
    """
    
    heatmap = Cool(microc_file, resolution=resolution, **MICROC_PLOTTING_PARAMS) + Title(microc_title)
    frame = heatmap
    if pro_bins is None:
        pro_bins = bigwig_bins
    def iterate_over_datasets(frame):
        i = 0 
        for chip_list in chip_list_list:
            bigwig_list = make_bigwig_list(chip_list, region, condition_order, 
                                           DEFAULT_COLOR_LIST[i%len(DEFAULT_COLOR_LIST)], bw_bins=bigwig_bins)
            i += 1
        
            for bigwig in bigwig_list:
                frame += bigwig + Spacer(SPACER_HEIGHT)
#         f_bigwig_list = make_bigwig_list(forward_proseq_list, region, condition_order, 
#                                        DEFAULT_COLOR_LIST[i%len(DEFAULT_COLOR_LIST)], bw_bins=pro_bins,  
#                                          track_height=PRO_SEQ_TRACK_HEIGHT)
#         r_bigwig_list = make_bigwig_list(reverse_proseq_list, region, len(reverse_proseq_list)*[""], 
#                                DEFAULT_COLOR_LIST[(i+1)%len(DEFAULT_COLOR_LIST)], bw_bins=pro_bins, 
#                                          track_height=PRO_SEQ_TRACK_HEIGHT)
# #         r_bigwig_list = [r_bigwig + Inverted() for r_bigwig in r_bigwig_list]
#         for f_bigwig, r_bigwig in zip(f_bigwig_list, r_bigwig_list):
#                 frame += f_bigwig + r_bigwig + Spacer(SPACER_HEIGHT)
        annotations = NewBed(*ANNOTATIONS_PARAMS)
        frame += annotations
        return frame
    
    # check if it needs a highlight
    if len(highlight_region_list) > 0:
        highlight_regions = []
        for highlight_region in highlight_region_list:
            highlight_region[1] -= highlight_buffer
            highlight_region[2] += highlight_buffer 
            highlight_regions.append(tuple(highlight_region))

        highlights = HighLights(highlight_regions, **HIGHLIGHT_PARAMS)
        with highlights:
            frame = iterate_over_datasets(frame)
    else:
        frame = iterate_over_datasets(frame)
   ### add bed motif 
    for bed_file in bed_files:
        bed_track = StrandMarkerTrack(bed_file)
        bed_track.fetch_data(region)
        frame += bed_track + Spacer(0.2)
    frame += XAxis()
    return frame

def make_bigwig_list(bigwigs, region, condition_order, color, bw_bins, track_height=3.5, autoscale=False, 
                     y_max=None,threshold_color="blue",threshold=0):
    
    """
    Helper function for `make_region_plot` that converts file paths to bigwig plotting objects.
    """
    assert len(bigwigs) % len(condition_order) == 0
    bigwig_list = []
    for bigwig, title, color, y_max, y_min in zip(bigwigs, condition_order, DEFAULT_COLOR_LIST, ymax, ymin):
        if title == "insulation":  # Adjust color for insulation track
            bigwig_track = BigWig(bigwig, number_of_bins=bw_bins, threshold_color="blue", threshold=0)
        else:
            bigwig_track = BigWig(bigwig, number_of_bins=bw_bins)
        
        track = bigwig_track + Title(title) + Color(color) + TrackHeight(track_height) + MaxValue(y_max) + MinValue(y_min)
        bigwig_list.append(track)
    if autoscale:
        bigwig_list = auto_scale_bigwigs(bigwig_list, region, y_max=y_max)
    return bigwig_list

def auto_scale_bigwigs(bigwig_list, region, y_max=None, y_min=0):
    """
    Autoscales y axis of bigwigs in bigwig list based off values in `region`.
    """
    def get_max_y_value(bigwig_list, region):
        max_y_values = []
        for bigwig in bigwig_list:
            max_y_values.append(np.amax(bigwig.fetch_plot_data(GenomeRange(region))))

        y_max = round(max(max_y_values) * 1.05)
        return y_max
    
    if y_max is None:
        if type(region) == list:
            y_max_list = [get_max_y_value(bigwig_list, single_region) for single_region in region]
            y_max = max(y_max_list)
        else:
            y_max = get_max_y_value(bigwig_list, region)
                
    return [bigwig + MaxValue(y_max) + MinValue(y_min) for bigwig in bigwig_list]

def read_cooler(cooler_path, resolution=250):
    """
    Simple function wrapper to read cooler file at a particular resolution.
    """
    if clr.fileops.is_cooler(cooler_path):
        return clr.Cooler(cooler_path)
    elif clr.fileops.is_multires_file(cooler_path):
        return clr.Cooler(cooler_path + "::resolutions/" + str(int(resolution)))

# define new bed format
class NewBed(Track):
    """
    Custom pygenometracks class that allows for control over the aesthetics of gene annotations in
    region plots. 
    """
    def __init__(self, coolbox_prop_dict, pygenometracks_prop_dict):
        super().__init__(coolbox_prop_dict)  # init 
        self.pygenometracks_object = BedTrack(pygenometracks_prop_dict)

    def fetch_data(self, gr, **kwargs):
        pass

    def plot(self, ax, gr, **kwargs):
#         x = gr.start + self.properties['offset'] * (gr.end - gr.start)
#         ax.text(x, 0, gr.chrom, fontsize=self.properties['fontsize'])
#         ax.set_xlim(gr.start, gr.end)
        self.pygenometracks_object.plot(ax, gr.chrom, gr.start, gr.end)
        ax.set_xlim([gr.start, gr.end])

        
        ##region_str = ("chr19:27,638,001-30,000,000")
# define StrandMarkerTrack for motif orientation
class StrandMarkerTrack(Track):
    def __init__(self, bed_file, **kwargs):
        super().__init__(**kwargs)
        self.bed_file = bed_file
        self.data = []

    def fetch_data(self, gr, **kwargs):
        """get region from bed"""
        self.data = []
        with open(self.bed_file, "r") as f:
            for line in f:
                fields = line.strip().split("\t")
                chrom, start, end, strand = fields[0], int(fields[1]), int(fields[2]), fields[3]
                if chrom == gr.chrom and start < gr.end and end > gr.start:
                    self.data.append((start, end, strand))
        return self.data

    def plot(self, ax, gr, **kwargs):
        """plot arrow"""
        for start, end, strand in self.data:
            mid = (start + end) / 2
            marker = ">" if strand == "+" else "<"
            ax.text(mid, 0, marker, ha="center", va="center", fontsize=10, color="blue")
        ax.set_xlim(gr.start, gr.end)
        ax.set_ylim(-1, 1)
        ax.axis("off") 
