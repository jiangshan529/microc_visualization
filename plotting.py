### fig1, 5kb
mcool_files =["/broad/boxialab/shawn/projects/microC/merged_new/remake_UU/HEK_WT/HEK_merge_micro1_5_UU_merged_dedup.pairs_652M_addnorm_200.mcool"]
chip_condition_bigwigs = ["/broad/boxialab/shawn/projects/microC/merged_new/remake_UU/HEK_WT/HEK_merge_micro1_5_UU_merged_dedup.pairs_652M_addnorm_5000_ins.bedgraph_5k.125000.bw",
       "/broad/boxialab/shawn/projects/hic/chip-seq/2.peak/HEK293_J_HG38_SRR1015994.bigwig",
                          "/broad/boxialab/shawn/projects/pub_data/chip-seq/hek_cpm_chip/H7_2min_6min_merge_sort_dedup_CPM.bw",
                          "/broad/boxialab/rawdata/8th_batch_1004_shawnbai/flag_chip/2.track_peak/227CVTLT3_5_0420637077_ChIP-80_S39_L005_hg38_sort_cpm.rmdup.bw",
                          "/broad/boxialab/rawdata/8th_batch_1004_shawnbai/flag_chip/2.track_peak/227CVTLT3_1_0420636994_ChIP-79_S6_L001_hg38_sort_cpm.rmdup.bw",
    
                          "/broad/boxialab/shawn/projects/pub_data/chip-seq/hek_cpm_chip/23022FL-03-01-27_S27_L001_hg38_sort_cpm.rmdup.bw",
                          "/broad/boxialab/shawn/projects/pub_data/chip-seq/hek_cpm_chip/23022FL-03-01-28_S28_L001_hg38_sort_cpm.rmdup.bw",
                          
                          "/broad/boxialab/shawn/projects/analysis/chip_Umap/bw_files/1.fastq/2.track_peak/SRR1016003_hg38_single_aligned_sort_dedup.bigwig"
                          
                           ]
condition_order = ["insulation","publicJ","H7J","flag","igG","ctcf","rad21","h3k27ac"]
DEFAULT_COLOR_LIST = ["red","#6e750e","#1fa774","#1fa774","#929591","#0485d1","#fd3c06","#960056"]
ymax=[1,0.15,0.3,0.3,0.3,2,2,2]
ymin=[-1,0,0,0,0,0,0,0]
# condition_order = ['ins', 'abcam', 'H7',"public_J","CTCF"]
# DEFAULT_COLOR_LIST = ["#1fa774","#1fa774", "#1fa774","#0485d1"]
# ymax=[1,1,1,1,20]
# ymin=[0,0,0,0,0]
# chip_condition_bigwigs = ["/broad/boxialab/shawn/projects/microC/bw_track/HCT/HCT116_J_chip_85_87_sort_dedup.bw",
#                           "/broad/boxialab/shawn/projects/microC/bw_track/HCT/227CVTLT3_2_0420637073_ChIP-55_S10_L002_hg38_sort.rmdup.bw",
#                             "/broad/boxialab/shawn/projects/microC/bw_track/HCT/HCT116_POL2A_hg38_ENCFF779RGR.bigWig",
#                          "/broad/boxialab/shawn/projects/microC/bw_track/HCT/HCT116_H3K27ac_ENCFF758DHJ.bigWig",
#                          "/broad/boxialab/shawn/projects/J/self_data/RNA-seq/HCT116/23022FL-07-01-04_S4_L008Aligned.bw"]
proseq_path = "/broad/boxialab/shawn/public_data/PRO-seq/HCT" # provide path to proseq files
proseq_forward_bigwigs = ["HCT116-PRO_merge_hg38_plus_sort.bw","HCT116-PRO_merge_hg38_plus_sort.bw"]
proseq_reverse_bigwigs = ["HCT116-PRO_merge_hg38_minus_sort.bw","HCT116-PRO_merge_hg38_plus_sort.bw"]

# # forward_proseq_list = ["/broad/boxialab/shawn/public_data/PRO-seq/HCT/HCT116-PRO_merge_hg38_plus_sort.bw",
#                       "/broad/boxialab/shawn/public_data/PRO-seq/HCT/HCT116-PRO_merge_hg38_plus_sort.bw"]
# reverse_proseq_list = ["/broad/boxialab/shawn/public_data/PRO-seq/HCT/HCT116-PRO_merge_hg38_minus_sort.bw",
#                       "/broad/boxialab/shawn/public_data/PRO-seq/HCT/HCT116-PRO_merge_hg38_plus_sort.bw"]



# chip_condition_bigwigs = cat_prefix_to_list(chip_path, chip_condition_bigwigs)
# proseq_forward_bigwigs = cat_prefix_to_list(proseq_path, proseq_forward_bigwigs)
# proseq_reverse_bigwigs = cat_prefix_to_list(proseq_path, proseq_reverse_bigwigs)

# condition_order = ['h7j', 'CTCF', 'polII',"27AC","RNA"]
# DEFAULT_COLOR_LIST = ["#1fa774", "#0485d1","#8e82fe","#960056","#fd3c06"]
# ymax=[0.7,5,10,70,70]
# ymin=[0,0,0,0,0]
bw_bins=7000
track_height=0.5
region_str = "chr8:101,199,193-103,133,192" #ovide region in format like chr15:99,921,434-100,682,822

MICROC_PLOTTING_PARAMS = {"style":"box",
                          "depth_ratio":"full",
                          "balance":True,
                          "cmap":'JuiceBoxLike',
                          "max_value":-4}

region_plot_params = {"region": region_str,
                    "resolution": 5000,
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
