import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

def no_city_found(city):
    return CITY_DATA.get(city) == None

def no_month_data(month):
    return  month not in MONTHS and month != 'all'

def not_day_of_week(day):
    return  day not in ['sunday','monday','tuesday', 'wednesday', 'thursday', 'friday', 'saturday'] and day != 'all'

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please enter name of city to analyze: ').lower()
    while no_city_found(city):        
        print('No data exist for the city you entered! Please try again. \n')
        city = input('Please enter name of city to analyze: ').lower()
    
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Please name of month to filter by. Enter "all" to apply no month filter: ').lower()
    while no_month_data(month):
        print('No data exist for the month you entered! Please try again. \n')
        month = input('Please type name of month to filter by. Enter "all" to apply no month filter: ').lower()
        
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please day of week to filter by. Enter "all" to apply no day filter: ').lower()
    while not_day_of_week(day):
        print('{} is not day of the week! Please try again. \n'.format(day))
        day = input('Please type day of week to filter by. Enter "all" to apply no day filter: ').lower()

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
    df = pd.read_csv(CITY_DATA[city.lower()])
    # Start Time column converted to datetime object
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int        
        month = MONTHS.index(month) + 1
    
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
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month is: {}'.format(common_month))
    # TO DO: display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print('The most common day of week is: {}'.format(common_day_of_week))
    # TO DO: display the most common start hour
    common_start_hr = df['hour'].mode()[0]
    print('The most common start hour is: {}'.format(common_start_hr))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station: ', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station: ', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    #popular_start_and_end_station = df.groupby(['Start Station']).count().max()
    popular_start_and_end_station = df.groupby(['Start Station','End Station']).size().idxmax()
    print('Most popular start and end station combination: ', popular_start_and_end_station)
    #print(df[['Start Station','End Station']].max())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\nTotal travel time: ', total_travel_time)
    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nMean travel time: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    
    # TO DO: Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('\nCount of user types \n {}'.format(user_type_count))
    
    try:
        # TO DO: Display counts of gender
        gender_count = df['Gender'].value_counts()
        print('\nCount of gender \n {}'.format(gender_count))

        # TO DO: Display earliest, most recent, and most common year of birth
        earliest_yob = df['Birth Year'].min()
        print('\nEarliest year of birth: ', earliest_yob)
        most_recent_yob = df['Birth Year'].max()
        print('\nMost recent year of birth: ', most_recent_yob)
        popular_yob = df['Birth Year'].mode()[0]
        print('\nMost popular year of birth: ', popular_yob)
    except KeyError as e:
        print('KeyError: Key does not exist in the selected dataset. ', e)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def get_user_input(size):
	""" Prompts user to enter number of rows to display """
    user_input = input('Enter number of rows to display. Number should not be greater than {}: '.format(size))
    while not user_input.isdigit() or int(user_input) > size:
        print('Please you need to enter a number less than or equal to {} to continue. \n'.format(size))
        user_input = input('Enter number of rows to display: Number should not be greater than {}: '.format(size))        
    return int(user_input)

def display_raw_data(df):
    """Displays raw data on bikeshare upon user request."""
    start_index = 0
    end_index = 5
    while True:
        show_data = input('\nDo you wish to view more data on bikeshare? Enter yes/no. \n').lower()
        if show_data != 'yes':
            break 
   
        if end_index < len(df):
            no_of_rows = 0#variable initialized          
            #User is invited to enter number of rows to display after the initial display 
            if start_index > 0 :
                no_of_rows = get_user_input(len(df)-start_index)# Number of rows entered should not exceed remaining rows in dataframe                
            end_index+=no_of_rows
            
            print('\nCalculating User Stats...\n')
            start_time = time.time()
            
            print(df.iloc[start_index:end_index])
            start_index = end_index
            
            print("\nThis took %s seconds." % (time.time() - start_time))
            print('-'*40)            
        else:  
            print('You have reached end of the dataset! \n')
            break
       
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
