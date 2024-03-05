#########################
### Introduction to R ###
#########################
library(dplyr)


# Libraries: Libraries contain scripts to run more complex calculations.
# The "datasets" library is a dedicated library of example datasets.
library(datasets)
# If you can't load the library, you have to install it first.
install.packages("datasets")

# Pick an interesting dataset. See complete list of datasets here:
# We pick the USArrests dataset (Violent Crime Rates by US State) and assign a short name to it for convenience.
d = USArrests

# Viewing the dataset
d           # View the full dataset
head(d)     # View just the first few rows of a dataset
# ?head       # For help on a function, type ? in front.

dim(d)      # Dimensions of a dataset
colnames(d) # Column names of a dataset
rownames(d) # Row names of a dataset

# Indexing datasets
d[1,]              # Returns first row
d[c(1, 3),]        # Returns first and third row
d[c(3, 1),]        # Returns third row first, then first row
d[,1]              # Returns first column
d["Alabama",]      # Returns row named Alabama
d[,"Murder"]       # Returns column named Murder
d$Murder           # Returns column named Murder (shortcut)
d$Murder >= 15     # Does the row has a value of "Murder" that is greater than or equal to 15?
d[d$Murder >= 15,] # Call the rows in which the values of "Murder" are greater than or equals to 15

#Sorting datasets
sort(d$Murder)       # Sort the "Murder" column only
order(d$Murder)      # Order the indices of the "Murder" column
d[order(d$Murder),]  # Sort entire dataset in increasing order of their "Murder" values

# Summarising data
summary(d)           # Shows quantile and mean
summary(d$Murder)

# get states with assault rates of more than 300

d[d$Murder >= 15,]

# 2
d[d$Assault > 300,]

# 3
d[d$Assault < 100& d$UrbanPop > 80,] 

# 4
# get all states above 75th percentile in murder rates
percentile_75 <- quantile(d$Murder, 0.75)
# high_murder_states <- d %>% filter(Murder > percentile_75)
high_murder_states <- filter(d, Murder > percentile_75)

high_murder_states

# 5
dord <- d[order(d$Assault, decreasing = TRUE),]

dord

# 6
top_5_assault <- head(dord, 5)
top_5_assault

#########################
### Data Preparation  ###
#########################

# Combine Data
d1 = cbind(rownames(d), d[,1:2]) # Use cbind to combine columns
d2 = cbind(rownames(d), d[,3:4])

print('d1, d2')

# Change Names
rownames(d)
rownames(d) <- NULL
colnames(d1)[1] <- "State"
colnames(d2)[1] <- "State"

# Randomize
set.seed(1)  # Fix a seed for reproducibility
rand <- sample(nrow(d2))
rand
d2 <- d2[rand,]
d2half <- d2[rand[1:25],]

# Merge
merge(d1, d2) # The merge function uses the common column to merge two datasets.
merge(d1, d2half, all.x = FALSE)

# Recoding Data / Create new columns
d$MurderCat[d$Murder >= 10] <- "Slaughter House"
d$MurderCat[d$Murder < 10]  <- "Animal Shelter"
head(d)



### Note: Set your Working Directory first ###
### You can use getwd() to find out your current working directory ###

setwd("./datasets") # Sets new working directory (TYPE IN YOUR OWN)


# Download data from https://github.com/hxchua/datakueh/blob/master/datasets/mrtsg.csv
mrt <- read.csv("mrtsg.csv", header = TRUE) # Reads data

### QUIZ TIME ###


# find the amount of times each station is repeated
repeated_mrt_stns <- table(mrt$STN_NAME)

# store the result in a dataframe
repeated_mrt_stns_df <- as.data.frame(repeated_mrt_stns)

# rename columns
colnames(repeated_mrt_stns_df) <- c("Station", "Freq")

repeated_mrt_stns_df <- repeated_mrt_stns_df[order(repeated_mrt_stns_df$Freq, decreasing = TRUE),]

write.csv(repeated_mrt_stns_df, "repeated_mrt_stns.csv")


# Reading Data from the Internet
library(rvest) # May need to install a new library using install.packages('rvest')
library(ggplot2)

# The package has a function that reads the html
page <- read_html("https://en.wikipedia.org/wiki/Men%27s_100_metres_world_record_progression") 

page_tables <- html_table(page, fill = T) # The package also has a function that extracts tables from html
records <- page_tables[[5]] # Let's extract the 5th table
head(records)               #View dataset
# str(records)                #View information about dataset

# Mini Quiz
records$Date <- as.Date(records$Date, format = "%B %d, %Y") # key in the correct date format

records

# empty array drugs
drugs <- c()

# loop through records$Athlete and append index to drugs if the athelete is ben johnson, tom montgomery or justin gatlin
for (i in 1:length(records$Athlete)) {
	if (records$Athlete[i] == "Ben Johnson" | records$Athlete[i] == "Tim Montgomery" | records$Athlete[i] == "Justin Gatlin") {
		drugs <- c(drugs, i)
	}
}

drugs

# remove doping records
records <- records[-drugs,]

# Plotting
graph <- ggplot(records, aes(x = Date, y = Time)) + geom_point() + geom_line() + xlab("Year") + ylab("Time (s)")

ggsave("100m.png", graph) # Save the graph as a file


cbr_rankings <- read_html('https://codebreaker.xyz/rankings')

cbr_rankings_tables <- html_table(cbr_rankings,	trim = TRUE)

cbr_rankings_tables

write.csv(cbr_rankings_tables, "cbr_rankings.csv")


# scrape codebrbeaker problems

# cbr_problems <- read_html('https://codebreaker.xyz/problems')

# cbr_problems_tables <- html_table(cbr_problems,	trim = TRUE)

# # remove \n and \ts in column 3
# cbr_problems_tables[[1]][,3] <- gsub("\n", "", cbr_problems_tables[[1]][,3])

# cbr_problems_tables