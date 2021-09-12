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
    print('Hello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Which city would you like to see data for? Chicago, New York City or Washington?\n ').lower()
    while city not in ['chicago', 'new york city', 'washington']:
        city = input ('Invalid selection. Please choose between Chicago, New York City or Washington.\n').lower()

    # get user input for month (all, january, february, ... , june)
    month = input ('What month would you like to see data for? Or All?\n').lower()
    while month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
        month = input ('Invalid selection. Please choose from January, February, March, April, May, June or All.\n').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input ('What day would you like to see data for? Or All?\n').lower()
    while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
        day = input ('Error. Please enter Monday-Sunday or \'all\'.\n').lower()
    print('The filters you selected are; \n City: {} \n Month: {} \n Day: {}'.format(city, month, day))
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Create start month day and hour columns to answer the frequent times of travel descriptive statistics questions
    df['Start Month'] = df['Start Time'].dt.month_name()
    df['Start Day'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour

    # Create travel time and hours columns fromt the start and end time columns to answer the travel time description statistics questions
    df['Trip Duration Hours'] = (
        (df['End Time'] - df['Start Time']) / pd.Timedelta(hours=1)).round(2)
    df['Trip Duration Minutes'] = (
        ((df['End Time'] - df['Start Time']) / pd.Timedelta(hours=1))*60).round(2)

    # Create a start and end station concatenate column to help answer the station descriptive statistice questions
    df['Trip Stations'] = df['Start Station'] + '_' + df['End Station']
    if month.title() != 'All':
        df = df[df['Start Month'] == month]
    if day.title() != 'All':
        df = df[df['Start Day'] == day]
    return df

def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    if month == 'All':
    # display the most common day of week
        if day == 'All':
            print('Most Popular Start Month: {}'.format(
                df['Start Month'].mode()[0]))
            print('Most Popular Start Day: {}'.format(
                df['Start Day'].mode()[0]))
    # display the most common month
        else:
            print('Most Popular Start Month: {}'.format(
                df['Start Month'].mode()[0]))
    # display the most common day of week
    else:
        if day == 'All':
            print('Most Popular Start Day: {}'.format(
                df['Start Day'].mode()[0]))

    # display the most common start hour
    print('Most Popular Start Hour: {} Count = {}'.format(df['Start Hour'].mode()[
          0], df[df['Start Hour'] == df['Start Hour'].mode()[0]]['Start Time'].count()))

    # Display the filters that were used to get this result
    print('\nThe filters you selected are \nCity: {} \nMonth: {} \nDay: {}'.format(city, month, day))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df, city, month, day):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station is: {}. Count = {}'.format(df['Start Station'].mode()[
          0], df[df['Start Station'] == df['Start Station'].mode()[0]]['Start Time'].count()), '\n')

    # display most commonly used end station
    print('The most common end station is: {}. Count = {}'.format(df['End Station'].mode()[
          0], df[df['End Station'] == df['End Station'].mode()[0]]['Start Time'].count()), '\n')

    # display most frequent combination of start station and end station trip
    start_station, end_station = (df['Trip Stations']).mode()[0].split('_')

    print('The most common combination of start and end stations is: {} and {}. Count = {}'.format(
        start_station, end_station, df[df['Trip Stations'] == df['Trip Stations'].mode()[0]]['Start Time'].count()))

    # Display the filters that were used to get this result
    print('\nThe filters you selected are \nCity: {} \nMonth: {} \nDay: {}'.format(city, month, day))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df, city, month, day):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    if month.title() != 'All':
        if day.title() != 'All':
            print('Total travel time in {} was: {} hours or {} minutes or {} seconds on {}s in {}'.format(city, df['Trip Duration Hours'].sum().round(2),
            df['Trip Duration Minutes'].sum().round(2), df['Trip Duration'].sum().round(2), day, month), '\n')
            print('The average travel time per ride in {} was: {} hours or {} minutes or {} second on {}s in {}'.format(city,
            df['Trip Duration Hours'].mean().round(2), df['Trip Duration Minutes'].mean().round(2), df['Trip Duration'].mean().round(2), day, month))
        else:
            print('Total travel time in {} was: {} hours or {} minutes or {} seconds in {}'.format(city, df['Trip Duration Hours'].sum().round(2),
            df['Trip Duration Minutes'].sum().round(2), df['Trip Duration'].sum().round(2), month), '\n')
            print('The average travel time per ride in {} was: {} hours or {} minutes or {} seconds in {}'.format(
                city, df['Trip Duration Hours'].mean().round(2), df['Trip Duration Minutes'].mean().round(2), df['Trip Duration'].mean().round(2), month))
    else:
        if day.title() != 'All':
            print('Total travel time in {} was: {} hours or {} minutes or {} second on {}s'.format(city, df['Trip Duration Hours'].sum().round(2),
            df['Trip Duration Minutes'].sum().round(2), df['Trip Duration'].sum().round(2), day), '\n')
            print('The average travel time per ride in {} was: {} hours or {} minutes or {} seconds on {}s'.format(city, df['Trip Duration Hours'].mean().round(2),
            df['Trip Duration Minutes'].mean().round(2), df['Trip Duration'].mean().round(2), day))
        else:
            print('Total travel time in {} was: {} hours or {} minutes or {} seconds'.format(city, df['Trip Duration Hours'].sum().round(2),
            df['Trip Duration Minutes'].sum().round(2), df['Trip Duration'].sum().round(2)), '\n')
            print('The average travel time per ride in {} was: {} hours or {} minutes or {} seconds'.format(city, df['Trip Duration Hours'].mean().round(2),
            df['Trip Duration Minutes'].mean().round(2), df['Trip Duration'].mean().round(2)))

    # Display the filters that were used to get this result
    print('\nThe filters you selected are \nCity: {} \nMonth: {} \nDay: {}'.format(city, month, day))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city, month, day):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Type and Count:', '\n {}'.format(df.groupby(df['User Type'])['Start Time'].count()), '\n')

    # Display counts of gender
    if city in ['chicago', 'new york city']:
        print('Gender and Count:', '\n {}'.format(df.groupby(df['Gender'])['Start Time'].count()))
    else:
        print('No Gender data is available for Washington')

    # Display earliest, most recent, and most common year of birth
    if city in ['chicago', 'new york city']:
        print('\nThe earliest birth year is: {}'.format(
            int(df['Birth Year'].min())))
        print('\nThe most recent birth year is: {}'.format(
            int(df['Birth Year'].max())))
        print('\nThe most common birth year is: {} Count = {}'.format(int(df['Birth Year'].mode()[0]), df[df['Birth Year'] == df['Birth Year'].mode()[0]]['Start Time'].count()))
    else:
        print('\nNo Birth Year data is available in the washington dataset')

    # Display the filters that were used to get this result
    print('\nThe filters you selected are \nCity: {} \nMonth: {} \nDay: {}'.format(city, month, day))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, city, month, day)
        station_stats(df, city, month, day)
        trip_duration_stats(df, city, month, day)
        user_stats(df, city, month, day)
        df.drop(['Start Month', 'Start Day', 'Start Hour', 'Trip Duration Hours','Trip Duration Minutes', 'Trip Stations'], axis=1, inplace=True)
        view_data = 'First Run'
        x = 0
        y = 5
        pd.set_option('display.Max_Columns',None)
        while view_data.lower() not in ['yes', 'no']:
            view_data = input('Would you like to view more individual trip data? Type \'yes\' or \'no\'.\n')
        while view_data.lower() == 'yes' and x < len(df)-1:
            print(df[x:y])
            view_data = input('Would you like to view more individual trip data? Type \'yes\' or \'no\'.\n')
            x += 5
            y += 5
            if y > len(df):
                y = len(df)
            while view_data.lower() not in ['yes', 'no']:
                view_data = input('Error. Please use \'yes\' or \'no.\' Would you like to view the individual trip data?\n')
        restart = input('\nWould you like to restart? Enter \'yes\' or \'no\'.\n')
        if restart.lower() != 'yes':
            print('Have a wonderful day!\n')
            print('-'*40)
            break

if __name__ == "__main__":
    main()
