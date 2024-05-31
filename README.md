# leaf-spectroradiometer-processing

Here are the steps if you ahve reflecatnce .sig files from SVC

1. Convert .sig to csv (using the specIO package)
2. Clean the csv file (remove overlapping bands and interpolate to ahve 1 nm interval)
3. Use PROSPECT code inverse in Rstudio to get the biochemical traits
