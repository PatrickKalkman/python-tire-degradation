import os
from matplotlib import ticker
import matplotlib.pyplot as plt
from dotenv import load_dotenv

from pandasai import PandasAI
from pandasai.llm.openai import OpenAI

from retrieve_race_data import RaceDataRetriever


def seconds_to_mmsssss(time_in_seconds):
    minutes, seconds = divmod(time_in_seconds, 60)
    return f"{int(minutes):02d}:{seconds:06.3f}"


def plot_lap_times_single(df):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the line
    ax.plot(df['lap_number'], df['laptime_seconds'], linestyle='-', color='blue',
            linewidth=2, zorder=1)

    # Plot the markers
    compound_colors = {'MEDIUM': 'yellow', 'HARD': 'white'}
    for compound in df['compound'].unique():
        compound_df = df[df['compound'] == compound]
        ax.scatter(compound_df['lap_number'], compound_df['laptime_seconds'], marker='o',
                   s=120, facecolor=compound_colors[compound], edgecolor='black',
                   alpha=1.0, label=compound, zorder=2)
        
    # Find and plot the fastest lap
    min_time_row = df.loc[df['laptime_seconds'].idxmin()]
    fastest_lap = ax.scatter(min_time_row['lap_number'], min_time_row['laptime_seconds'], marker='o',
                             s=120, facecolor='violet', edgecolor='blue', zorder=3)

    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: seconds_to_mmsssss(x)))

    ax.grid(True)

    ax.set_title('Max Verstappen - 2023 Miami Grand Prix')
    ax.set_xlabel('Lap')
    ax.set_ylabel('Lap Time')

    # Create a custom legend
    from matplotlib.lines import Line2D
    custom_lines = [Line2D([0], [0], marker='o', color='yellow', label='MEDIUM', 
                           markersize=10, markerfacecolor='yellow', markeredgecolor='black'),
                    Line2D([0], [0], marker='o', color='white', label='HARD',
                           markersize=10, markerfacecolor='white', markeredgecolor='black'),
                    Line2D([0], [0], marker='o', color='violet', label='Fastest lap',
                           markersize=10, markerfacecolor='violet', markeredgecolor='black')]

    ax.legend(handles=custom_lines)

    plt.show()


def plot_driver_data(df, ax, compound_colors, line_color):
    # Plot the line
    ax.plot(df['lap_number'], df['laptime_seconds'], linestyle='-', color=line_color, linewidth=2, zorder=1)

    # Plot the markers
    for compound in df['compound'].unique():
        compound_df = df[df['compound'] == compound]
        ax.scatter(compound_df['lap_number'], compound_df['laptime_seconds'], marker='o',
                   s=40, facecolor=compound_colors[compound], edgecolor='black',
                   alpha=1.0, label=compound, zorder=2)

    # Find and plot the fastest lap
    min_time_row = df.loc[df['laptime_seconds'].idxmin()]
    ax.scatter(min_time_row['lap_number'], min_time_row['laptime_seconds'], marker='o',
               s=120, facecolor='violet', edgecolor='blue', zorder=3)


def plot_lap_times(df_max, df_perez):
    fig, ax = plt.subplots(figsize=(10, 6))

    compound_colors = {'MEDIUM': 'yellow', 'HARD': 'white'}

    plot_driver_data(df_max, ax, compound_colors, line_color='blue')
    plot_driver_data(df_perez, ax, compound_colors, line_color='red')

    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: seconds_to_mmsssss(x)))

    ax.grid(True)

    ax.set_title('Max Verstappen vs Sergio Perez - 2023 Miami Grand Prix')
    ax.set_xlabel('Lap')
    ax.set_ylabel('Lap Time')
    ax.set_ylim(88, 98)

    # Create a custom legend
    from matplotlib.lines import Line2D
    custom_lines = [Line2D([0], [0], marker='o', color='yellow', label='MEDIUM', 
                           markersize=10, markerfacecolor='yellow', markeredgecolor='black'),
                    Line2D([0], [0], marker='o', color='white', label='HARD',
                           markersize=10, markerfacecolor='white', markeredgecolor='black'),
                    Line2D([0], [0], marker='o', color='violet', label='Fastest lap',
                           markersize=10, markerfacecolor='violet', markeredgecolor='black')]

    ax.legend(handles=custom_lines)

    plt.show()


def main():
    retriever = RaceDataRetriever()
    retriever.load_data()
    total_df = retriever.create_timing_dataframe()

    load_dotenv()

    # read the OPEN_API_KEY from the environment
    # uncomment the following to enable using Pandas AI
    # OPEN_API_KEY = os.environ.get('OPENAI_API_KEY')
    # llm = OpenAI(api_token=OPEN_API_KEY)
    # pandas_ai = PandasAI(llm)
    # result = pandas_ai.run(total_df, prompt='List all the average lap times of all drivers?')
    #print(result)

    max_df = total_df[total_df['driverId'] == 'max_verstappen']
    perez_df = total_df[total_df['driverId'] == 'perez']

    # plot_lap_times_single(max_df)
    plot_lap_times(max_df, perez_df)


if __name__ == '__main__':
    main()
