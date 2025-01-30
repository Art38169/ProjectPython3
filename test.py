import numpy as np
import matplotlib.pyplot as plt

# Data
data = [
    ["2019-01", 70.02, 17.83, 3.85, 1.66, 1.66, 4.38, 0.26, 0.07, 0.19, 0.05, 0.03],
    ["2019-02", 72.73, 14.69, 2.87, 2.03, 2.15, 4.94, 0.12, 0.04, 0.36, 0.05, 0.02],
    ["2019-03", 73.92, 13.25, 2.3, 3.98, 1.78, 4.42, 0.2, 0.05, 0.05, 0.04, 0.01],
    ["2019-04", 76.66, 14.05, 2.46, 4.92, 1.5, 0.18, 0.14, 0.03, 0.01, 0.03, 0.03],
    ["2019-05", 80.21, 11.34, 2.55, 4.33, 1.31, 0, 0.17, 0.03, 0.01, 0.04, 0],
    ["2019-06", 81.52, 10.33, 2.05, 4.47, 1.45, 0.02, 0.09, 0.02, 0.01, 0.04, 0],
    ["2019-07", 79.01, 9.82, 2.38, 6.73, 1.82, 0, 0.15, 0.03, 0.02, 0.05, 0.01],
    ["2019-08", 73.74, 13.37, 4.89, 5.23, 2.31, 0, 0.22, 0.17, 0.02, 0.05, 0],
    ["2019-09", 68.03, 19.22, 5.43, 4.7, 1.99, 0, 0.23, 0.33, 0.02, 0.04, 0],
    ["2019-10", 60.7, 22.75, 9.89, 3.72, 2.1, 0.1, 0.44, 0.25, 0.02, 0.04, 0],
    ["2019-11", 67.12, 20.98, 6.36, 2.45, 1.76, 0.7, 0.33, 0.25, 0.02, 0.03, 0],
    ["2019-12", 63.48, 20.41, 10.78, 2.09, 1.94, 0.73, 0.4, 0.12, 0.01, 0.03, 0]
]

# Convert to numpy array
data_np = np.array(data)

# Extract months
months = data_np[:, 0]

# Extract each app's data
facebook = data_np[:, 1].astype(float)
twitter = data_np[:, 2].astype(float)
youtube = data_np[:, 3].astype(float)
vk = data_np[:, 4].astype(float)
pinterest = data_np[:, 5].astype(float)
google_plus = data_np[:, 6].astype(float)
instagram = data_np[:, 7].astype(float)
reddit = data_np[:, 8].astype(float)
linkedin = data_np[:, 9].astype(float)
tumblr = data_np[:, 10].astype(float)
other = data_np[:, 11].astype(float)


# Print the extracted numpy arrays
# print("Months:", months)
# print("Facebook data:", facebook)
# print("Twitter data:", twitter)
# print("YouTube data:", youtube)
# print("VKontakte data:", vk)
# print("Pinterest data:", pinterest)
# print("Google+ data:", google_plus)
# print("Instagram data:", instagram)
# print("Reddit data:", reddit)
# print("LinkedIn data:", linkedin)
# print("Tumblr data:", tumblr)
# print("Other data:", other)
plt.figure(figsize=(10, 6))  # Size of the plot
plt.bar(months, facebook, color='skyblue')  # Create bar chart with skyblue color

# Adding labels and title
plt.xlabel('Month', fontsize=12)
plt.ylabel('Percentage of Facebook Users (%)', fontsize=12)
plt.title('Facebook Usage Percentage Over Time (2019)', fontsize=14)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Show the plot
plt.tight_layout()  # Adjusts the plot to prevent clipping of labels
plt.show()