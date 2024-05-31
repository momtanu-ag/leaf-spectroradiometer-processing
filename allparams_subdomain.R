library(zoo)
library(prospect)
library(dplyr)
devtools::install_gitlab('jbferet/prospect')

setwd("F:/svc/2023/Westwind/2023_May_westwind/new_files_cleaning/2023_05_24_westwind/csv/test")
Refl_tmp<- read.csv("2023_may_westwind_spectra_interpolated.csv", check.names = FALSE)
Refl_tmp <- Refl_tmp / 100

#trans_tmp<- read.csv("trans_interpolate_input.csv", check.names = FALSE)

lambda <- 400:2500

# ref: Feret et al., (RSE 2020)

SubData<- FitSpectralData(SpecPROSPECT=SpecPROSPECT,lambda=lambda,Refl =Refl_tmp, Tran = NULL,
                              UserDomain = c(lambda[1],lambda[length(lambda)]),UL_Bounds = TRUE)
SubSpecPROSPECT = SubData$SpecPROSPECT
Sublambda      = SubData$lambda
SubRefl         = SubData$Refl
#SubTran        = SubData$Tran

# Estimate all parameters for PROSPECT-D using R only
Parms2Estimate  = c("CHL", "CAR", "ANT", "EWT", "PROT", "CBC", "N")
#InitValues <- data.frame(CHL=40, CAR=8, ANT=0.1, BROWN=0, EWT=0.01, LMA=0.01, N=1.5, PROT = 0.002)
InitValues <- data.frame(CHL=40, CAR=8, ANT=0.1, BROWN=0, EWT=0.01, N=1.5, PROT = 0.002, CBC = 0.008)
print('PROSPECT inversion using optimal spectral setting and prior N')
ParmEst2 <- Invert_PROSPECT_OPT(SpecPROSPECT = SubSpecPROSPECT, lambda=Sublambda, Refl = SubRefl, 
                                Tran = NULL, PROSPECT_version = 'PRO',
                                Parms2Estimate = Parms2Estimate, InitValues = InitValues)
CHL <- CAR <- ANT <- EWT <- PROT <- Nstruct<- CBC<- list()

for (i in 1:ncol(SubRefl)){
  print(i)
  #ParmEst2 <- Invert_PROSPECT(SubSpecPROSPECT,Refl = SubRefl[,i],
                         #Tran = SubTran[,i],PROSPECT_version = 'PRO',
                         #Parms2Estimate = Parms2Estimate)
  
  ParmEst2 <- Invert_PROSPECT(SubSpecPROSPECT,Refl = SubRefl[,i],
                              Tran = NULL,PROSPECT_version = 'PRO',
                              Parms2Estimate = Parms2Estimate)
CHL[i] <- ParmEst2$CHL
CAR[i] <- ParmEst2$CAR
ANT[i] <- ParmEst2$ANT
EWT[i] <- ParmEst2$EWT
#LMA_R_OPT6292[i] <- ParmEst2$LMA
PROT[i]  <- ParmEst2$PROT
Nstruct[i] <- ParmEst2$N
CBC[i] <- ParmEst2$CBC}
package2 = as.data.frame(cbind(CHL, CAR, ANT, EWT, PROT, Nstruct, CBC))
package3 = plyr::adply(package2,1,unlist,.id = NULL)
write.csv(package3,"F:/svc/2023/Westwind/2023_May_westwind/new_files_cleaning/2023_05_24_westwind/csv/test/2023_05_24_westwind_Prospectpro_optimal.csv")
