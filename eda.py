# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns

# Read in csv
df = pd.read_csv('combined_df.csv')

# Visualize college readiness rating distribution
def college_readiness_distribution(df):
    sns.set_style("darkgrid")
    sns.distplot(df["subratings_College Readiness Rating"], bins=10, kde=False)
    plt.title('College Readiness Rating Distribution', fontsize=16)
    plt.xlabel('College Readiness Rating', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.xticks(np.arange(df["subratings_College Readiness Rating"].min(), df["subratings_College Readiness Rating"].max()+1))

college_readiness_distribution(df)

# Scatterplot function
def scatterplot(x, y, data, title, xlabel, ylabel, hline=0, vline=0):
    plt.scatter(x, y, data=data, s=8)
    plt.title(title, fontsize=16)
    plt.xticks(np.arange(0, data[x].max(), step=10))
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    if hline != 0:
        plt.axhline(hline, color='r')
    if vline != 0:
        plt.axvline(vline, color='g')

# Percent Low Income vs. Percent College Rate
scatterplot('percentLowIncome', 'collegeEnrollmentData_school_value', df, 
            'Percent Low Income vs. Percent College Rate', 'Percent Low Income', 'Percent College Rate', 
            hline=df['collegeEnrollmentData_state_average'].mean())

# Exploratory Boxplot
def exploratory_boxplot(x, y, df, title, xlabel, ylabel):
    sns.set_style("darkgrid")
    ax = sns.boxplot(x, y,
                 data=df, palette="Set3")
    ax.set_title(title, fontsize=16)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)

# Boxplot of College Readiness Ratings by Students per Teacher 
exploratory_boxplot('subratings_College Readiness Rating', 'studentsPerTeacher', df, 
                                         'College Readiness Ratings by Students Per Teacher', 
                                         'College Readiness Ratings (1-10)',
                                        'Students Per Teacher')

# Boxplot of Student Progress Rating by Students per Teacher

exploratory_boxplot('subratings_Student Progress Rating', 'studentsPerTeacher', df, 
                                         'Student Progress Ratings by Students Per Teacher', 
                                         'Student Progress Ratings (1-10)',
                                        'Students Per Teacher')

# Return a table of Student Progress Ratings and median students per teacher                                    
df.groupby('subratings_Student Progress Rating')['studentsPerTeacher'].median()

# Boxplot comparing percent low income to student progress rating
exploratory_boxplot('subratings_Student Progress Rating', 'percentLowIncome', df, 
                                         'Student Progress Ratings by Percent Low Income', 
                                         'Student Progress Ratings (1-10)',
                                        'Percent Low Income')

# Boxplot comparing percent low income and test score ratings. Includes a pointplot overlap.
sns.pointplot(x='subratings_Test Scores Rating', y='percentLowIncome', data=df.groupby('subratings_Test Scores Rating', as_index=False).median())
exploratory_boxplot('subratings_Test Scores Rating', 'percentLowIncome', df, 
                                         'Student Test Score Ratings by Percent Low Income', 
                                         'Student Test Score Ratings (1-10)',
                                        'Percent Low Income')

# Return a table of Test Score Ratings and median percent of low income students
df.groupby('subratings_Test Scores Rating')['percentLowIncome'].median()

# Save the updated csv file
df.to_csv('combined_df.csv')