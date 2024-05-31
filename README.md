# leaf-spectroradiometer-processing

Here are the steps if you have reflectance .sig files from SVC (the example csv and sig files are in a folder, so that the code can be replicated)

1. Convert .sig to csv (using the specIO package)
2. Clean the csv file (remove overlapping bands and interpolate to ahve 1 nm interval)
3. Use PROSPECT code inverse in Rstudio to get the biochemical traits
