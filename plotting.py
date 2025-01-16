

# 数据配置
mcool_files = ["/broad/boxialab/shawn/projects/microC/merge_publication_1.7B/hct/hct_wt_merge_all_1.48B_UU_dedup.pairs_50bp.mcool"]
chip_condition_bigwigs = [
    "/broad/boxialab/shawn/projects/microC/merge_publication_1.7B/hct/hct_wt_ins_125000_5k_rm3.125000.bw",
    "/broad/boxialab/shawn/projects/microC/merge_publication_1.7B/hek/hek_wt_1.7b_win25_rm3.125000.bw",
    "/broad/boxialab/shawn/projects/microC/merge_publication_1.7B/hct/hct_wt_ins_200res_5000_rm3.5000.bw",
    "/broad/boxialab/shawn/projects/microC/merge_publication_1.7B/hek/hct_wt_ins_200bp_5000_rm3.5000.bw",
    "/broad/boxialab/shawn/projects/analysis/chip_Umap/bw_files/1.fastq/2.track_peak/H7_2min_6min_merge_sort_dedup_CPM.bigwig",
    "/broad/boxialab/shawn/projects/analysis/chip_Umap/bw_files/HCT/fastq/2.track_peak/HCT116_J_chip_85_87_sort_dedup.bw",
    "/broad/boxialab/shawn/projects/analysis/chip_Umap/bw_files/1.fastq/2.track_peak/hek_znf_merge_sort_dedup.bigwig",
    "/broad/boxialab/shawn/projects/analysis/chip_Umap/bw_files/1.fastq/2.track_peak/23022FL-03-01-27_S27_L001_hg38_sort_cpm.rmdup.bigwig",
    "/broad/boxialab/shawn/projects/analysis/chip_Umap/bw_files/HCT/fastq/2.track_peak/227CVTLT3_2_0420637073_ChIP-55_S10_L002_hg38_sort.rmdup.bw",
    "/broad/boxialab/shawn/projects/analysis/chip_Umap/bw_files/1.fastq/2.track_peak/23022FL-03-01-28_S28_L001_hg38_sort_cpm.rmdup.bigwig",
    "/broad/boxialab/shawn/projects/analysis/chip_Umap/bw_files/HCT/fastq/2.track_peak/227CVTLT3_3_0420637074_ChIP-56_S20_L003_hg38_sort.rmdup.bw",
    "/broad/boxialab/shawn/projects/analysis/chip_Umap/bw_files/1.fastq/2.track_peak/SRR1016003_hg38_single_aligned_sort_dedup.bigwig",
    "/broad/boxialab/shawn/projects/analysis/chip_Umap/bw_files/HCT/fastq/2.track_peak/hct_h3k27ac_ENCFF623IJZ_hg38_sort_cpm.rmdup.bw",
    "/broad/boxialab/shawn/projects/pub_analysis/flag_ko_chip/227CVTLT3_1_0420636994_ChIP-79_S6_L001_hg38_sort_cpm.rmdup.bw"
]

# 添加两个 BED 文件
bed_files = [
    "/broad/boxialab/shawn/projects/analysis/ctcf_motif/hek_CTCF_motifs_fpr0.1.bed",
    "/broad/boxialab/shawn/projects/analysis/ctcf_motif/hct_CTCF_motifs_fpr0.1.bed"
]

condition_order = ["insulation", "insulation", "insulation", "insulation", "hek_H7J", "hct_H7J", "hek_znf", "hek_ctcf", "hct_ctcf", "hek_rad21", "hct_rad21", "hek_27ac", "hct_27ac", "hek_igg"]
DEFAULT_COLOR_LIST = ["red", "red", "red", "red", "#1fa774", "#1fa774", "#0014A8", "#0485d1", "#0485d1", "#fd3c06", "#fd3c06", "#960056", "#960056", "grey"]
ymax = [1, 1, 1, 1, 0.5, 0.5, 2, 5, 5, 3, 3, 2, 2, 1]
ymin = [-1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
proseq_path = "/broad/boxialab/shawn/public_data/PRO-seq/HCT" # provide path to proseq files
proseq_forward_bigwigs = ["HCT116-PRO_merge_hg38_plus_sort.bw","HCT116-PRO_merge_hg38_plus_sort.bw"]
proseq_reverse_bigwigs = ["HCT116-PRO_merge_hg38_minus_sort.bw","HCT116-PRO_merge_hg38_plus_sort.bw"]



bw_bins=7000
track_height=0.5


region_str = ("19:27,638,001-30,000,000")

chrom, positions = region_str.split(":")
start, end = map(int, positions.replace(",", "").split("-"))
region_gr = GenomeRange(f"chr{chrom}", start, end)  

MICROC_PLOTTING_PARAMS = {"style":"box",
                          "depth_ratio":"full",
                          "balance":True,
                          "cmap":'fall',
                          "max_value":-6,
                         "min_value":-8}

region_plot_params = {"region": region_gr,
                    "resolution": 5000,
                    "highlight_region_list": [["chr1",154_955_735,154_994_524]], 
                    "microc_file": mcool_files[0],
                    "microc_title": "Micro-C",
                    "chip_list_list": [chip_condition_bigwigs],
                    "forward_proseq_list": proseq_forward_bigwigs,
                    "reverse_proseq_list": proseq_reverse_bigwigs,
                     "condition_order": condition_order,
                     "bed_files":bed_files}

frame = make_region_plot(**region_plot_params)
fig1 = frame.plot(region_str)
fig1
