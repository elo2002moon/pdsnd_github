import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city=input('Please specify the city (Chicago, New York City, Washington) ').lower()
        if city not in ['chicago','new york city','washington']:
            print("This was no valid input. Try again! ")
            continue
        else:
            break
        
        # get user input for month (all, january, february, ... , june)
    while True:
        month=input('Please specify the month (All, January, February, Marach, April, May, or June) ').lower()
        if month not in ['all','january','february','march','april','may','june']:
            print("This was no valid input. Try again! ")
            continue
        else:
            break

        # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day=input('Please specify the day (All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)').lower()
        if day not in ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
            print("This was no valid input. Try again!")
            continue
        else:
            break

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
#        df = df[df['day_of_week'] == day.title()]
        dof = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        df = df.loc[df['day_of_week']==dof.index(day)]    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[df['month'].mode()[0]-1].title()
        
    print('Most Popular Month:', popular_month)

    # display the most common day of week
    dof = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    popular_day = dof[df['day_of_week'].mode()[0]].title()
        
    print('Most Popular Day:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour

    ## find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Route']=df['Start Station']+'-->'+df['End Station']
    popular_route = df['Route'].mode()[0]
    print('Most Popular Route:', popular_route)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time: [in sec]: ', total_travel_time)
    
    # display mean travel time
    mean_travel_time = total_travel_time / df['Trip Duration'].count()
    print('Mean Travel Time [in sec]: ', mean_travel_time)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    try:
        gender_types = df['Gender'].value_counts()
        print(gender_types)
    except KeyError:
        print("No information on gender available.")
    # Display earliest, most recent, and most common year of birth
    
    try:
        oldest = df['Birth Year'].min()
        youngest = df['Birth Year'].max()
        commonyear = df['Birth Year'].mode()[0]
        print('The oldest customer was born in {} and the youngest customer was born in {}.'.format(int(oldest),int(youngest)))
        print('The most active customer cohort was born in {}.'.format(int(commonyear)))
    except KeyError:
        print("No information on birth year available.")    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw data in pieces of 5 obs."""
    #start_time = time.time()
    
    counter=0
    max_entries = df.shape[0]-1 
    df.index = range(len(df.index))
    while True:
        five_more = input('Do you want to see five lines of raw data ("yes" or "no")?').lower()
        if five_more not in ['yes','no']:
            print('no valid input')
            continue
        elif five_more == 'yes':
            print('\nPrint 5 lines of raw data...\n')
            print(df.loc[counter:counter+4,:])
            if counter >= max_entries:
                break
            else:
                counter+=5
                continue
        else:
            break
            

    #print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
