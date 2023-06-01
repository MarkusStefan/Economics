rm(list=ls())
packages <- c("tidyverse", "cansim")

package_installer <- function (list_of_packages){
  for(package in list_of_packages) {
    if(!require(package, character.only = TRUE)) {
      install.packages(package, dependencies = TRUE)
      require(package, character.only = TRUE)
    }
    else {
      next
    }
  }
}

package_installer(packages)


# retrieve data
nGDP <- get_cansim_vector(vector="v62471340",
                  start_time = "1920-01-01",
                  end_time="2023-05-01")

# preview data
nGDP %>% head()

# navigating to desired working directory
path <- "~/R/Annual_Data/Canada"
setwd(path)
getwd()

# write to csv file
# comma delimited -> use write.csv()
#write.csv(nGDP, file="v62471340.csv")

# semicolon delimited (for excel) -> use write.csv2()
write.csv2(nGDP, file="v62471340.csv")
