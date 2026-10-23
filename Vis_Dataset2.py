import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the datasets
vle = pd.read_csv('Universityy_learning_data/studentVle.csv')
info = pd.read_csv('Universityy_learning_data/studentInfo.csv')
assessment = pd.read_csv('Universityy_learning_data/studentAssessment.csv')

# converting "score" to numeric, turning non-numbers into NaN
assessment['score'] = pd.to_numeric(assessment['score'], errors='coerce')

# total clicks per student, only from module AAA
info_aaa = info[info['code_module'] == 'AAA']
clicks = vle.groupby('id_student')['sum_click'].sum().reset_index()

# Average assessment score per student
# Now calculate the average score, ignoring the NaN values
scores = assessment.groupby('id_student')['score'].mean().reset_index()

# Merge the datasets
# Start with unique students and their final outcomes
student_data = info_aaa[['id_student', 'final_result']].drop_duplicates()
student_data = student_data.merge(clicks, on='id_student', how='inner')
student_data = student_data.merge(scores, on='id_student', how='inner')

# 4. Create the visualizations
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Plot A: Categorical grades (Final Result) vs Total Clicks
sns.boxplot(
    data=student_data, 
    x='final_result', 
    y='sum_click',
    #ylim=(0, 10000),
    order=['Distinction', 'Pass', 'Fail', 'Withdrawn'],
    ax=axes[0]
)
axes[0].set_title('Online Engagement by Final Result')
axes[0].set_xlabel('Final Course Result')
axes[0].set_ylabel('Total VLE Clicks')
axes[0].set_ylim([-5, 10000])


# Plot B: Average Score vs Total Clicks
sns.scatterplot(
    data=student_data, 
    x='sum_click', 
    y='score',
    alpha=0.2, 
    ax=axes[1]
)
axes[1].set_title('Average Assessment Score vs Total VLE Clicks')
axes[1].set_xlabel('Total VLE Clicks')
axes[1].set_ylabel('Average Assessment Score')

plt.tight_layout()
plt.savefig('Learning_distribution')
plt.show()

# second plot: Histogram
plt.figure(figsize=(8, 5))
sns.countplot(
    data=info,
    x='final_result',
    order=['Distinction', 'Pass', 'Fail', 'Withdrawn'],
    palette='muted'
)

# add labels and title
plt.title('Distribution of Final Course Results')
plt.xlabel('Final Result')
plt.ylabel('Number of Students')

# show and save the plot
plt.tight_layout()
plt.savefig('histResult')
plt.show()