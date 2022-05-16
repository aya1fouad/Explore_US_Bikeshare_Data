import time
import pandas as pd
import numpy as np
from tabulate import tabulate

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def check_input(input_string,input_type):
    """
    check the validity of user input.
    
    Args:
        input_user: is the input of the user.
        input_type: is the type of input: 1 = city, 2 = month, 3 = day.
        
    Return:
        valid_user_input :the valid data which will filter depending on it.
    """
    while True:
        valid_user_input = input(input_string)
        print(valid_user_input)
        try:
            # inputs is case insensitive.
            if valid_user_input in ['chicago','new_york_city','washington'] and input_type == 1:
                break
            elif valid_user_input in ['january', 'february', 'march', 'april', 'may', 'june','all'] and input_type == 2:
                break
            elif valid_user_input in ['saturday','sunday','monday','tuesday','wednesday','thursday','friday','all'] and input_type == 3:
                break
            else:
                if input_type == 1:
                    print("Invalid city; The input should be:'chicago'or'new_york_city'or'washington'")
                if input_type == 2:
                    print("Invalid month; The input should be:'january'or'february'or'march'or'april'or'may'or'june'or'all'")
                if input_type == 3:
                    print("Invalid day; The input should be:'saturday'or'sunday'or'monday'or'tuesday'or'wednesday'or'thursday'or'friday'or'all'")
        except ValueError:
            print("Invalid Input !")
            
    return valid_user_input



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city & check the validity of user input.
    city = check_input("which city? ('chicago'or'new_york_city'or'washington')",1).lower()
    
    # get user input for month & check the validity of user input.
    month = check_input("Which Month? ('january'or'february'or'march'or'april'or'may'or'june'or'all')", 2).lower()
    
    # get user input for day & check the validity of user input.
    day = check_input("Which day? ('saturday'or'sunday'or'monday'or'tuesday'or'wednesday'or'thursday'or'friday'or'all')", 3).lower()
     
    print('-'*40)
    return city, month, day



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe.
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month from Start Time to create new column.
    df['month'] = df['Start Time'].dt.month
    
    # extract day of week from Start Time to create new column.
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # extract hour from Start Time to create new column.
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable.
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    # determine the start time.
    start_time = time.time()
    
    # display the most common month.
    print("\nThe most common month:",df['month'].mode()[0],".\n")

    # display the most common day of week.
    print("The most common day of week:",df['day_of_week'].mode()[0],".\n")

    # display the most common start hour.
    print("The most common start hour:",df['hour'].mode()[0],".\n")
    
    # display the taken time.
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    # determine the start time.
    start_time = time.time()

    # display the most common start station.
    print("The most common start station:",df['Start Station'].mode()[0],"\n")

    # display the most common end station.
    print("The most common end station:",df['End Station'].mode()[0],"\n")

    # display the most common trip from start to end .
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']
    print("The most common trip from start to end:",df['trip'].mode()[0],"\n")
    
    # display the taken time.
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    # determine the start time.
    start_time = time.time()
    
    # display the total travel time.
    print("The total travel time:",df['Trip Duration'].sum(),"\n")

    # display the average travel time.
    print("The average travel time:",df['Trip Duration'].mean(),"\n")
    
    # display the taken time.
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    # determine the start time.
    start_time = time.time()
    
    # display counts of each user type.
    print("User info : ",df['User Type'].value_counts() ,"\n")
    
    # gender dose't exsit in washington.
    if city != 'washington':
        
        # display the counts of gender.
        print("Gender Stats:",df['Gender'].value_counts() ,"\n")
        
        # display the earliest year of birth.
        print("The earliest year of birth:",df['Birth Year'].min() ,"\n")
        
        # display the most recent year of birth.
        print("The most recent year of birth:",df['Birth Year'].max() ,"\n")
        
        # display the most common year of birth.
        print("The most common year of birth:",df['Birth Year'].mode()[0] ,"\n")
        
    # display the taken time.
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """
    Displays raw data upon request by the user.
    
    Args:
         df : Pandas DataFrame containing city data filtered by month and day.
    """
    i = 0
    
    while True:
        display_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        if display_data.lower() != 'yes':
            break
        print(tabulate(df.iloc[np.arange(0+i,5+i)], headers ="keys"))
        i+=5
    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
