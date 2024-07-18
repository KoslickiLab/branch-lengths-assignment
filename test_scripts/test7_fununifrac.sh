#obtain KEGG tree
#complete later. Refer to extraction repo

#obtain PW distance.

cd /data/wjw5274/branch-lengths-assignment/FunUniFrac/fununifrac
python compute_edges.py -e ../../data/fununifrac_data/kegg_trees/kegg_ko00001_no_edge_lengths_filtered.txt -d ../../data/fununifrac_data/pw_distance_files/KOs_sketched_scaled_10_k_5 --distance -r 1000 -o ../../data/fununifrac_data/kegg_trees -b ko00001

#compute pairwise fununifrac distances
#cpu server
#cd /data/shared_data/wjw5274/FunUniFrac/fununifrac
#python compute_fununifrac.py -e /data/wjw5274/branch-lengths-assignment/data/fununifrac_data/kegg_trees/kegg_ko00001_assigned_bu.txt -fd ./reproducibility/data/skin_vs_gut -fp *.csv -o ./reproducibility/data/skin_vs_gut -i pw_distance_bu -b ko00001



python compute_fununifrac.py -e /data/wjw5274/branch-lengths-assignment/data/fununifrac_data/kegg_trees/kegg_ko00001_assigned_bu.txt -fd ../../data/fununifrac_data/body_sites/gather -fp *.csv -o ../../data/fununifrac_data/body_sites -i pw_distance_bu -b ko00001
python plot_from_df.py -df ../data/fununifrac_data/body_sites/fununifrac_out_pw_distance_bu.main.npy -l ../data/fununifrac_data/body_sites/fununifrac_out_pw_distance_bu.main.basis.npy -meta ../data/fununifrac_data/body_sites/filtered_simple_metadata.csv -o ../data/plots/body_sites_pcoa.png -t pcoa
python compute_fununifrac.py -e /data/wjw5274/branch-lengths-assignment/data/fununifrac_data/kegg_trees/kegg_ko00001_assigned_nnls_temp.txt -fd ../../data/fununifrac_data/body_sites/gather -fp *.csv -o ../../data/fununifrac_data/body_sites -i pw_distance_nnls -b ko00001
python plot_from_df.py -df ../data/fununifrac_data/body_sites/fununifrac_out_pw_distance_nnls.main.npy -l ../data/fununifrac_data/body_sites/fununifrac_out_pw_distance_nnls.main.basis.npy -meta ../data/fununifrac_data/body_sites/filtered_simple_metadata.csv -o ../data/plots/body_sites_pcoa_nnls.png -t pcoa


#compare recomputed pw distances
#bu
python compare_pw_dist.py -r -e1 ../data/fununifrac_data/kegg_trees/kegg_ko00001_assigned_bu.txt -t "Pw distance recomputed from bottom-up tree" -o ../data/plots/bu_vs_ref_pw_dist.png -c seagreen
#nnls
python compare_pw_dist.py -r -e1 ../data/fununifrac_data/kegg_trees/kegg_ko00001_assigned_nnls_temp.txt -t "Pw distance recomputed from NNLS tree" -o ../data/plots/nnls_vs_ref_pw_dist.png -c seagreen
#两个对比
python compare_pw_dist.py -o ../data/plots/compare_nnls_bu_pw_dist.png -e1 ../data/fununifrac_data/kegg_trees/kegg_ko00001_assigned_nnls_temp.txt -c orange


#analysis
python compare_pw_dist.py -o ../data/plots/compare_pw_dist.png


#download data
python hmgdb_downloader.py -i /data/wjw5274/branch-lengths-assignment/data/fununifrac_data/body_sites/metadata_gut_skin_oral_vaginal.csv -o /data/wjw5274/branch-lengths-assignment/data/fununifrac_data/body_sites


python data_prep.py
bash preprocess.sh #get file_paths.csv
conda activate sourmash
bash gather.sh
#sketch 1000

#average
python compute_average_sample.py -fd ../../data/fununifrac_data/body_sites/gather -fp *.csv -o ../../data/fununifrac_data/body_sites/average_samples.tsv -m ../../data/fununifrac_data/body_sites/filtered_simple_metadata.csv -c HMgDB_sample_site_1 -id library_id

python plot_diffab.py -df /Users/wjw5274/PycharmProjects/pythonProject/branch_lengths_assignment/data/fununifrac_data/body_sites/gut_skin_average.tsv -e /Users/wjw5274/PycharmProjects/pythonProject/branch_lengths_assignment/data/fununifrac_data/kegg_trees/kegg_ko00001_assigned_bu.txt -o /Users/wjw5274/PycharmProjects/pythonProject/branch_lengths_assignment/data/fununifrac_data/body_sites -i average_gut_skin_diffab -thresh 0.0005

#python plot_diffab.py -df ../../data/fununifrac_data/body_sites/average_samples.tsv -e ../../data/fununifrac_data/kegg_trees/kegg_ko00001_assigned_bu.txt -o ../../data/fununifrac_data/body_sites -i average_body_sites
python plot_diffab.py -df /Users/wjw5274/PycharmProjects/pythonProject/branch_lengths_assignment/data/fununifrac_data/body_sites/gut_skin_average.tsv -e /Users/wjw5274/PycharmProjects/pythonProject/branch_lengths_assignment/data/fununifrac_data/kegg_trees/kegg_ko00001_assigned_bu.txt -o /Users/wjw5274/PycharmProjects/pythonProject/branch_lengths_assignment/data/fununifrac_data/body_sites -i average_gut_skin_diffab -thresh 0.0005
python plot_diffab.py -df /Users/wjw5274/PycharmProjects/pythonProject/branch_lengths_assignment/data/fununifrac_data/body_sites/oral_gut_average.tsv -e /Users/wjw5274/PycharmProjects/pythonProject/branch_lengths_assignment/data/fununifrac_data/kegg_trees/kegg_ko00001_assigned_bu.txt -o /Users/wjw5274/PycharmProjects/pythonProject/branch_lengths_assignment/data/fununifrac_data/body_sites -i average_gut_oral_diffab -thresh 0.0005
python plot_diffab.py -df /Users/wjw5274/PycharmProjects/pythonProject/branch_lengths_assignment/data/fununifrac_data/body_sites/oral_skin_average.tsv -e /Users/wjw5274/PycharmProjects/pythonProject/branch_lengths_assignment/data/fununifrac_data/kegg_trees/kegg_ko00001_assigned_bu.txt -o /Users/wjw5274/PycharmProjects/pythonProject/branch_lengths_assignment/data/fununifrac_data/body_sites -i average_skin_oral_diffab -thresh 0.0005

#clean version
#gather_clean
python compute_average_sample.py -fd ../../data/fununifrac_data/body_sites/gather_clean -fp *.csv -o ../../data/fununifrac_data/body_sites/average_samples_clean.tsv -m ../../data/fununifrac_data/body_sites/filtered_simple_metadata.csv -c HMgDB_sample_site_1 -id library_id
python plot_diffab.py -df /Users/wjw5274/PycharmProjects/pythonProject/branch_lengths_assignment/data/fununifrac_data/body_sites/average_gut_skin_clean.tsv -e /Users/wjw5274/PycharmProjects/pythonProject/branch_lengths_assignment/data/fununifrac_data/kegg_trees/kegg_ko00001_assigned_bu.txt -o /Users/wjw5274/PycharmProjects/pythonProject/branch_lengths_assignment/data/fununifrac_data/body_sites -i clean_average_gut_skin_diffab -thresh 0.0005
python plot_diffab.py -df /Users/wjw5274/PycharmProjects/pythonProject/branch_lengths_assignment/data/fununifrac_data/body_sites/average_gut_oral_clean.tsv -e /Users/wjw5274/PycharmProjects/pythonProject/branch_lengths_assignment/data/fununifrac_data/kegg_trees/kegg_ko00001_assigned_bu.txt -o /Users/wjw5274/PycharmProjects/pythonProject/branch_lengths_assignment/data/fununifrac_data/body_sites -i clean_average_gut_oral_diffab -thresh 0.0005
python plot_diffab.py -df /Users/wjw5274/PycharmProjects/pythonProject/branch_lengths_assignment/data/fununifrac_data/body_sites/average_oral_skin_clean.tsv -e /Users/wjw5274/PycharmProjects/pythonProject/branch_lengths_assignment/data/fununifrac_data/kegg_trees/kegg_ko00001_assigned_bu.txt -o /Users/wjw5274/PycharmProjects/pythonProject/branch_lengths_assignment/data/fununifrac_data/body_sites -i clean_average_skin_oral_diffab -thresh 0.0005


#motus
#installation
conda install -c bioconda motus
