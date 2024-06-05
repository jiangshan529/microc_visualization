mcool_files =["/broad/boxialab/shawn/projects/microC/merged_new/HCT/HCT_WT_new_merged.pairs_dedup_941M_600.mcool"]
chip_condition_bigwigs = ["/broad/boxialab/shawn/projects/pub_data/chip-seq/hek_cpm_chip/H7_2min_6min_merge_sort_dedup_CPM.bw",
                          "/broad/boxialab/shawn/projects/pub_data/chip-seq/hek_cpm_chip/23022FL-03-01-27_S27_L001_hg38_sort_cpm.rmdup.bw",
                         "/broad/boxialab/shawn/projects/hic/chip-seq/2.peak/HEK293T_polII2A[43075.bw]_cistrome_hg38.bigwig",
                         "/broad/boxialab/shawn/projects/hic/chip-seq/2.peak/HEK293T-H3K27ac-hg38.bigwig",
                          "/broad/boxialab/shawn/projects/J/RNA-seq/HEK/1.mapping/23022FL-03-01-33_S33_L001Aligned.bw"]
condition_order = ['h7j', 'CTCF', 'polII',"27AC",'RNA']
DEFAULT_COLOR_LIST = ["#1fa774", "#0485d1","#8e82fe", "#960056","#fd3c06"]
ymax=[3,10,0.7,10,10,10]
ymin=[0,0,0,0,0]
bw_bins=7000
track_height=1.6




region_str = "17:72,306,437-72,933,650" # provide region in format like chr15:99,921,434-100,682,822

MICROC_PLOTTING_PARAMS = {"style":"matrix",
                          "transform":"log2",
                          "depth_ratio":"full",
                          "balance":True,
                          "cmap":'Reds',
                          "max_value":10^-3}

region_plot_params = {"region": region_str,
                    "resolution": 600,
                    "highlight_region_list": [["chr1",154_955_735,154_994_524]], 
                    "microc_file": mcool_files[0],
                    "microc_title": "Micro-C",
                    "chip_list_list": [chip_condition_bigwigs],
                    "forward_proseq_list": proseq_forward_bigwigs,
                    "reverse_proseq_list": proseq_reverse_bigwigs,
                     "condition_order": condition_order}

frame = make_region_plot(**region_plot_params)
fig1 = frame.plot(region_str)
fig1
fig.savefig("/broad/boxialab/shawn/projects/pub_analysis/test_antibodies/test_antibody_chip.pdf", format='pdf')
