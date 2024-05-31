# leaf-spectroradiometer-processing

Here are the steps if you have reflectance .sig files from SVC (the example csv and sig files are in a folder, so that the code can be replicated)

1. Convert .sig to csv (using the specIO package, the code read_plot_SVC.py in specIO folder should be used)
2. Clean the csv file (remove overlapping bands and interpolate to have 1 nm interval) using clear_noise.py in the main repository
3. Use PROSPECT code inverse in Rstudio to get the biochemical traits
