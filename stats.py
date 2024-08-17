import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
politicians_df = pd.read_csv('Databases/final_politicians_info.csv')
senators_df = pd.read_csv('Databases/final_senators_info.csv')
representatives_df = pd.read_csv('Databases/final_representatives_info.csv')

# Function to create bias score distribution plot
def plot_bias_distribution(df, title, file_name):
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='Bias Score', hue='Party Affiliation', kde=True, palette='coolwarm', binwidth=5)
    plt.title(title)
    plt.xlabel('Bias Score')
    plt.ylabel('Count')
    plt.legend(title='Party Affiliation')
    plt.tight_layout()
    plt.savefig(f'Graphs/{file_name}.png')
    plt.close()

# Function to create bar plot comparing average bias score by party
def plot_avg_bias_by_party(df, title, file_name):
    plt.figure(figsize=(8, 6))
    sns.barplot(data=df, x='Party Affiliation', y='Bias Score', palette='coolwarm', ci=None)
    plt.title(title)
    plt.xlabel('Party Affiliation')
    plt.ylabel('Average Bias Score')
    plt.tight_layout()
    plt.savefig(f'Graphs/{file_name}.png')
    plt.close()

# Plot for all politicians
plot_bias_distribution(politicians_df, 'Bias Score Distribution (All Politicians)', 'bias_distribution_all')
plot_avg_bias_by_party(politicians_df, 'Average Bias Score by Party (All Politicians)', 'avg_bias_all')

# Plot for senators
plot_bias_distribution(senators_df, 'Bias Score Distribution (Senators)', 'bias_distribution_senators')
plot_avg_bias_by_party(senators_df, 'Average Bias Score by Party (Senators)', 'avg_bias_senators')

# Plot for representatives
plot_bias_distribution(representatives_df, 'Bias Score Distribution (Representatives)', 'bias_distribution_representatives')
plot_avg_bias_by_party(representatives_df, 'Average Bias Score by Party (Representatives)', 'avg_bias_representatives')
