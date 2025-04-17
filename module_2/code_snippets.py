"""
Collection of code examples demonstrating various algorithms and data operations.

This module contains implementations of sorting algorithms and
data manipulation examples using pandas and numpy.
"""

import pandas as pd
import numpy as np


def bubble_sort(arr):
    """
    Sort an array using the bubble sort algorithm.

    Parameters
    ----------
    arr : list
        The input array to be sorted.

    Returns
    -------
    list
        The sorted array in ascending order.
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def process_weather_data(filename="weather.csv"):
    """
    Process weather data from a CSV file.

    Parameters
    ----------
    filename : str, optional
        Path to the CSV file containing weather data.
        Default is 'weather.csv'.

    Returns
    -------
    tuple
        A tuple containing numpy arrays of wind_speed, wind_direction,
        and wind_direction in radians.

    Raises
    ------
    FileNotFoundError
        If the specified file cannot be found.
    """
    try:
        weather_df = pd.read_csv(filename)

        # Numpy is faster so convert
        wind_speed = weather_df["Data.Wind.Speed"].to_numpy()
        wind_direction = weather_df["Data.Wind.Direction"].to_numpy()

        # Better built in function in np
        wind_direction_rad = np.deg2rad(wind_direction)

        return wind_speed, wind_direction, wind_direction_rad
    except FileNotFoundError:
        print(f"Weather data file '{filename}' not found.")
        raise


# Example usage of the bubble_sort function
if __name__ == "__main__":
    unsorted_array = [64, 34, 25, 12, 22, 11, 90]
    sorted_array = bubble_sort(unsorted_array)
    print("Sorted array:", sorted_array)

    # Example usage of the process_weather_data function
    try:
        wind_speed, wind_direction, wind_direction_rad = process_weather_data()
        print("Wind Speed:", wind_speed)
        print("Wind Direction:", wind_direction)
        print("Wind Direction in Radians:", wind_direction_rad)
    except FileNotFoundError:
        pass