import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

def main():
    '''Produces a simple plot

       `python competitions.py data/datafile.xlsx`

    '''
    # Import data
    dataset = sys.argv[1]
    results_basename = os.path.basename(dataset).split('.')[0]
    df_inoculum = pd.read_excel(dataset, sheetname='inoculum')
    df = pd.read_excel(dataset, sheetname='squid')

    # Calculate input ratios
    df_inoculum['ratioWB'] = df_inoculum['white']/df_inoculum['blue']
    # Calculate output ratios
    df['ratioWB'] = df['white']/df['blue']
    # Mean of duplicate input plates
    df_inoculum_summary = df_inoculum.groupby(['competition'], as_index=False).mean()
    # Merge input data & calculate competitive index
    df_summary = pd.merge(df, df_inoculum_summary[['competition', 'ratioWB']], on=['competition'])
    df_summary.rename(columns={'ratioWB_x': 'ratioWB_o', 'ratioWB_y': 'ratioWB_i'}, inplace=True)
    df_summary['CI'] = np.log10(df_summary['ratioWB_o'] / df_summary['ratioWB_i'])
    # Mean of replicate plates per animal
    df_summary = df_summary.groupby(['competition', 'animal'], as_index=False).mean()

    # Save dataframe to csv
    df_summary.to_csv('results/' + results_basename + '.csv')

    # Plot competitions
    # Create a new figure of size 8x6 points, using 100 dots per inch
    plt.figure(figsize=(8,6), dpi=100)
    # Create a new subplot from a grid of 1x1
    plt.subplot(111)
    plt.scatter(df_summary['competition'], df_summary['CI'], marker='o', s=75,
                color='gray', linewidths=2, alpha=0.7)
    plt.scatter(df_summary.groupby('competition', as_index=False).median()['competition'],
                df_summary.groupby('competition', as_index=False).median()['CI'], marker='_', s=500,
                color='black', linewidths=2, alpha=1.0)
    # Save plot to png, pdf
    plt.savefig('results/' + results_basename + '.png')
    plt.savefig('results/' + results_basename + '.pdf')


if __name__ == '__main__':
    main()
