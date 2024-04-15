#Project 1 - Use Data Science dataset to make conclusions regarding salary

#Import dataset
r_project_data <- read.csv("~/School/DSE5002/Week_5/Project/r project data.csv")

#libraries used
library(dplyr)
library(scales)
library(ggplot2)
library(lubridate)
library(stringr)

#Examine summary statistics
summary(r_project_data)

head(r_project_data)

#Determine if "NA" values exist - None exist and this is good. No treatment needed.
print("Position of missing values")
which(is.na(r_project_data))

print("Count of total missing values")
sum(is.na(r_project_data))


#Initial data wrangling

#Rename column 1 to row_id
colnames(r_project_data)[1] <- c("row_id")

#Code below converts from int data type to eventual chr to better use in plots
#later
r_project_data$work_year <- ymd(paste0(r_project_data$work_year, "0101"))
r_project_data$work_year <- format(r_project_data$work_year, "%Y")

#View project head to make sure all looks appropriate
head(r_project_data)

#begin data aggregation and initial analysis and plots

#Box Plot of Salary
ggplot(r_project_data, aes(group=work_year)) + 
  geom_boxplot(aes(x=work_year
                  ,y=salary_in_usd))+
  scale_y_continuous(labels = dollar_format(prefix = "$", 
                                            big.mark = ",", decimal.mark = "." 
                                            ,accuracy = 1)) +
  labs(x='Year'
       ,y='Salary'
       ,title='Data Science Salary By Year')
#Notes/Findings: Lots of outliers, median is the better measure when analyzing 
#salary



#Data wrangling and Median Salary Per Year By Experience Level
#Average and median salary by work year and experience in USD
year_experience_group <- r_project_data %>%
  group_by(work_year, experience_level) %>%
  summarise(average_salary_usd=mean(salary_in_usd)
            ,median_salary_usd=median(salary_in_usd)) %>%
  arrange(experience_level)


#Set experience level as factors to re-order for plot below
year_experience_group$experience_level <- factor(year_experience_group$experience_level
                                                 ,levels = c("EN", "MI"
                                                              ,"SE", "EX"))

#Median Salary Per Year By Experience Level
ggplot(year_experience_group, aes(x=work_year, y=median_salary_usd 
                                  ,fill=experience_level)) +
  geom_col(position="dodge") +
  geom_label(aes(label=dollar(median_salary_usd, prefix = "$" 
                              ,big.mark = ",", decimal.mark = "." 
                              ,accuracy = 1)) 
             ,size=3, vjust = 0.5, position=position_dodge(0.9)
             ,fontface="bold")+
  scale_y_continuous(labels = dollar_format(prefix = "$" 
                                            ,big.mark = ",", decimal.mark = "." 
                                            ,accuracy = 1)) +
  labs(x='Year'
       ,y='Median Salary'
       ,fill='Experience Level'
       ,title = 'Median Salary Per Year by Experience Level')
#Notes/Findings - As expected, the highest salaries are paid with the most experience.
#However,the gap between salaries given the experience has narrowed.



#Another, closer look at Senior Level salaries boxplot
#Filter data to only SE level
salary_experience_level <- r_project_data %>%
  filter(experience_level=="SE")

#Boxplot showing Senior level salary by year
ggplot(salary_experience_level, aes(group=work_year)) + 
  geom_boxplot(aes(x=work_year
                   ,y=salary_in_usd))+
  scale_y_continuous(labels = dollar_format(prefix = "$", 
                                            big.mark = ",", decimal.mark = "." 
                                            ,accuracy = 1)) +
  labs(x='Year'
       ,y='Salary of Senior Level'
       ,title='Senior Level Salary By Year')

#Summary stats 
summary(salary_experience_level)
#Notes/Findings: Some outliers in 2022, however was able to take a closer look
#At summary statistics using a boxplot.



#Count of The Data by Experience Level
#Wrangle/group data to sum experience level
count_position_experience <- r_project_data %>%
  group_by(experience_level) %>%
  reframe(count_experience=(sum(str_count(experience_level))))

#Convert experience level to factor to re-order for plot below
count_position_experience$experience_level <- factor(count_position_experience$experience_level
                                    , levels = c("EN", "MI"
                                                 ,"SE", "EX"))

#Plot Count of Experience Level
ggplot(count_position_experience) + 
  geom_col(aes(x=experience_level,y=count_experience
               ,fill=experience_level))+
  labs(x='Experience Level'
       ,y='Count Experience'
       ,fill='Experience Level'
       ,title='Count By Experience Level')
#Notes/Findings: The most experience exists in in the MI and SE level within
#this dataset.



#Median Salary in USD and exchange rates for International Analysis
#Exchange Rate Equation - Multiply salary by multiplier_to_usd to get 
#salary in USD
currency_exchange_rate <- r_project_data %>%
  group_by(salary_currency) %>%
  summarise(multiplier_to_usd=mean(salary_in_usd/salary))

#Median salary in usd given the country
median_salary_international <- r_project_data %>%
  group_by(salary_currency) %>%
  summarise(median_salary_usd=median(salary_in_usd))

#Join tables together to get exchange rate multiplier and median salary in usd
joined_salary_exchange <- currency_exchange_rate %>%
  inner_join(median_salary_international, by='salary_currency')

#Plot median salary and color by exchange rate multiplier
ggplot(joined_salary_exchange) +
  geom_rect(aes(xmin=-Inf, xmax=Inf, ymin=0, ymax=50000), fill="green", alpha=0.2)+
  geom_rect(aes(xmin=-Inf, xmax=Inf, ymin=50000, ymax=100000), fill="yellow", alpha=0.2)+
  geom_rect(aes(xmin=-Inf, xmax=Inf, ymin=100000, ymax=150000), fill="red", alpha=0.2)+
  geom_point(aes(x=salary_currency, y=median_salary_usd 
                  ,color=multiplier_to_usd))+
  scale_y_continuous(labels = dollar_format(prefix = "$", 
                                            big.mark = ",", decimal.mark = "." 
                                            ,accuracy = 1)) +
  labs(x='Country of Salary Paid'
       ,y='Median Salary in USD'
       ,color='$ Multiplier'
       ,title='Median Foreign Salaries in USD')
#Notes/Findings: Green means a lower median salary given the country to usd,
#and red is the highest median salary in usd. The gradient of the dots show
#how low or high the exchange rate is in relation to the salary paid. 
#So, a darker dot means the salary is worth less in relation to usd.


