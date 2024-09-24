from datetime import date
import matplotlib.pyplot as plt
import numpy as np

dates = [1999, 2017, 2020, 2024]
labels = ['Andrew was born', 'Andrew starts attending Berk', 'Andrew drops out of Berk', 'Today']

fig, ax = plt.subplots(figsize=(15, 4), constrained_layout=True)
_ = ax.set_ylim(-2, 1.75)
_ = ax.set_xlim(1999, 2024)
_ = ax.axhline(0, xmin=0.05, xmax=0.95, c='deeppink', zorder=1)
 
_ = ax.scatter(dates, np.zeros(len(dates)), s=120, c='palevioletred', zorder=2)
_ = ax.scatter(dates, np.zeros(len(dates)), s=30, c='darkmagenta', zorder=3)

label_offsets = np.zeros(len(dates))
label_offsets[::2] = 0.35
label_offsets[1::2] = -0.7
for i, (l, d) in enumerate(zip(labels, dates)):
    _ = ax.text(d, label_offsets[i], f"{d}: {l}", ha='center', fontfamily='serif', fontweight='bold', color='royalblue',fontsize=12)

stems = np.zeros(len(dates))
stems[::2] = 0.3
stems[1::2] = -0.3   
markerline, stemline, baseline = ax.stem(dates, stems)
_ = plt.setp(markerline, marker=',', color='darkmagenta')
_ = plt.setp(stemline, color='darkmagenta')

# hide lines around chart
for spine in ["left", "top", "right", "bottom"]:
    _ = ax.spines[spine].set_visible(False)
 
# hide tick labels
_ = ax.set_xticks([])
_ = ax.set_yticks([])
 
_ = ax.set_title('Andrew\'s Timeline', fontweight="bold", fontfamily='serif', fontsize=16, 
                 color='royalblue')

plt.show()


# https://dadoverflow.com/2021/08/17/making-timelines-with-python/
# eventually need to handle different details of time:

# from datetime import datetime

# Define different timestamp formats
# formats = [
#     "%Y",            # Year only
#     "%Y-%m",         # Year and month
#     "%Y-%m-%d",      # Year, month, and day
#     "%Y-%m-%d %H:%M:%S"  # Year, month, day, and time
# ]

# # Function to parse timestamp
# def parse_timestamp(timestamp):
#     for fmt in formats:
#         try:
#             return datetime.strptime(timestamp, fmt)
#         except ValueError:
#             continue
#     raise ValueError("No valid date format found")

# # Example usage
# timestamps = ["2024", "2024-09", "2024-09-24", "2024-09-24 11:34:12"]
# parsed_dates = [parse_timestamp(ts) for ts in timestamps]

# for ts, pd in zip(timestamps, parsed_dates):
#     print(f"Original: {ts} -> Parsed: {pd}")
