import calendar
from datetime import date
import os
from colorama import Fore, Back, Style
import sys

#configurable variables
files_folder =  None                #'/home/usman/Desktop/Training/Assignment-1-Weather-Man/weatherdata/'
files_prefix = 'lahore_weather_'
min_year = 1996
max_year = 2011

elements_indices_dict = dict()      #Dictionary for mapping from element name to the element index in the sequence of elements


def set_elements_indices(elements_str):
    """Initialize the elements_indices_dict according to the comma separated elements names
     given in the string
     """
    elements_indices_dict.clear()
    elements = elements_str.split(',')

    for i,elem in enumerate(elements):
        elements_indices_dict[elem.strip()] = i


def get_file_contents_line_by_line(file_path):
    """Given file path, it yields contents of
     that file line by line
     """
    try:
        file = open(file_path)
    except:
        print('File not found', file_path)
        quit()

    for line in file:
        if line.startswith('1') or line.startswith('2'):
            yield line

        elif len(line) > 25:
            if not elements_indices_dict:       #Assuming each file has same sequence defined for the elements
                set_elements_indices(line)


def display_specific_days_of_a_year(year):
    """For a given year displays the highest temperature and day, lowest temperature and day, most humid day
    and humidity
    """
    if year < min_year or year > max_year:
        raise Exception('Year should be in between ' + str(min_year) + ' and ' + str(max_year))

    max_temp = float('-inf')
    min_temp = float('inf')
    max_humidity = float('-inf')
    max_temp_day = date(1970,1,1)
    min_temp_day = date(1970,1,1)
    max_humidity_day = date(1970,1,1)
    fileCount = 0

    for month in calendar.month_abbr:
        if len(month) < 1:
            continue

        current_file_path = files_folder + files_prefix + str(year) + '_' + month + '.txt'

        if not os.path.exists(current_file_path):
            continue
        fileCount += 1

        for line in get_file_contents_line_by_line(current_file_path):

            elements = line.split(',')
            current_day = date(*[int(i) for i in elements[elements_indices_dict['PKT']].split('-')])
            current_max_temp = elements[elements_indices_dict['Max TemperatureC']]
            current_min_temp = elements[elements_indices_dict['Min TemperatureC']]
            current_max_humidity = elements[elements_indices_dict['Max Humidity']]

            if len(current_max_temp) > 0 and float(current_max_temp) > max_temp:
                max_temp = float(current_max_temp)
                max_temp_day = current_day

            if len(current_min_temp) > 0 and float(current_min_temp) < min_temp:
                min_temp = float(current_min_temp)
                min_temp_day = current_day

            if len(current_max_humidity) > 0 and float(current_max_humidity) > max_humidity:
                max_humidity = float(current_max_humidity)
                max_humidity_day = current_day

    if fileCount < 1:
        print('data not found')
        quit()

    print('Highest: ' + '{:02d}'.format(round(max_temp)) + 'C on ' + calendar.month_name[max_temp_day.month] + ' ' + str(max_temp_day.day))
    print('Lowest: ' + '{:02d}'.format(round(min_temp)) + 'C on ' + calendar.month_name[min_temp_day.month] + ' ' + str(min_temp_day.day))
    print('Humidity: ' + str(round(max_humidity)) + '% on ' + calendar.month_name[max_humidity_day.month] + ' ' + str(max_humidity_day.day))


def display_averages_of_a_month(year, month):
    """For a given month with a year displays the average highest temperature,
     average lowest temperature, average humidity
     """
    if year < min_year or year > max_year:
        raise Exception('Year should be in between ' + str(min_year) + ' and ' + str(max_year))

    if month < 1 or month > 12:
        raise Exception('Month should be in between 1 and 12 ')

    month_abbrev = calendar.month_abbr[month]
    current_file_path = files_folder + files_prefix + str(year) + '_' + month_abbrev + '.txt'

    if not os.path.exists(current_file_path):
        print('Error data missing for', calendar.month_abbr[month], year)
        return

    avg_max_temp = 0
    avg_min_temp = 0
    avg_mean_humidity = 0
    max_temp_count = 0.0
    min_temp_count = 0.0
    mean_humidity_count = 0.0

    for line in get_file_contents_line_by_line(current_file_path):

        elements = line.split(',')
        max_temp = elements[elements_indices_dict['Max TemperatureC']]
        min_temp = elements[elements_indices_dict['Min TemperatureC']]
        mean_humidity = elements[elements_indices_dict['Mean Humidity']]

        if len(max_temp) > 0:
            max_temp_count += 1
            avg_max_temp += float(max_temp)

        if len(min_temp) > 0:
            min_temp_count += 1
            avg_min_temp += float(min_temp)

        if len(mean_humidity) > 0:
            mean_humidity_count += 1
            avg_mean_humidity += float(mean_humidity)

    print('Highest Average: {:2d}C'.format(round(avg_max_temp / max_temp_count)))
    print('Lowest Average: {:2d}C'.format(round(avg_min_temp / min_temp_count)))
    print('Average Humidity: {:2d}%'.format(round(avg_mean_humidity / mean_humidity_count)))


def draw_two_horizontal_bar_charts(year, month):
    """Given a month, draws two horizontal bar charts on the console for
    the highest and lowest temperature on each day
    """
    if year < min_year or year > max_year:
        raise Exception('Year should be in between ' + str(min_year) + ' and ' + str(max_year))

    if month < 1 or month > 12:
        raise Exception('Month should be in between 1 and 12 ')

    print(calendar.month_name[month],year)
    month_abbrev = calendar.month_abbr[month]
    current_file_path = files_folder + files_prefix + str(year) + '_' + month_abbrev + '.txt'

    if not os.path.exists(current_file_path):
        print('Error data missing for', calendar.month_abbr[month], year)
        return

    for day,line in enumerate(get_file_contents_line_by_line(current_file_path)):

        elements = line.split(',')
        print('{:02d} '.format(day+1), end='')
        max_temp = elements[elements_indices_dict['Max TemperatureC']]

        if len(max_temp) < 1:
            print('Missing Data')
        else:
            max_temp = round(float(max_temp))
            [print(Fore.RED + '+', end='') for _ in range(max_temp)]
            print(Style.RESET_ALL + ' {:02d}C'.format(max_temp))

        print('{:02d} '.format(day + 1), end='')
        min_temp = elements[elements_indices_dict['Min TemperatureC']]

        if len(min_temp) < 1:
            print('Missing Data')
        else:
            min_temp = round(float(min_temp))
            [print(Fore.BLUE + '+', end='') for _ in range(min_temp)]
            print(Style.RESET_ALL + ' {:02d}C'.format(min_temp))


def draw_one_horizontal_bar_chart(year, month):
    """Given a month, draws one horizontal bar chart on the console for
     the highest and lowest temperature on each day
     """
    if year < min_year or year > max_year:
        raise Exception('Year should be in between ' + str(min_year) + ' and ' + str(max_year))

    if month < 1 or month > 12:
        raise Exception('Month should be in between 1 and 12 ')

    print(calendar.month_name[month], year)
    month_abbrev = calendar.month_abbr[month]
    current_file_path = files_folder + files_prefix + str(year) + '_' + month_abbrev + '.txt'

    if not os.path.exists(current_file_path):
        print('Error data missing for', calendar.month_abbr[month], year)
        return

    for day,line in enumerate(get_file_contents_line_by_line(current_file_path)):

        elements = line.split(',')
        print('{:02d} '.format(day+1), end='')

        max_temp = elements[elements_indices_dict['Max TemperatureC']]
        min_temp = elements[elements_indices_dict['Min TemperatureC']]

        if len(max_temp) < 1:
            print('Missing Data', end='')
        else:
            max_temp = round(float(max_temp))
            [print(Fore.RED + '+', end='') for _ in range(max_temp)]

        print(Style.RESET_ALL, end='')

        if len(min_temp) < 1:
            print('Missing Data', end='')
        else:
            min_temp = round(float(min_temp))
            [print(Fore.BLUE + '+', end='') for _ in range(min_temp)]

        print(Style.RESET_ALL, end='')
        print(' {:02d}C - {:02d}C'.format(min_temp, max_temp))


if __name__ == '__main__':

    try:
        option = sys.argv[1]
        year_month = sys.argv[2]
        files_folder = sys.argv[3]
    except:
        print('3 Arguments are required', len(sys.argv) - 1, 'were given')
        quit()

    if option == '-e':
        try:
            year = int(year_month)

            if year < min_year or year > max_year:
                print('Year should be in between', min_year, 'and', max_year)
                quit()
        except:
            print('INVALID Input')
            quit()

        display_specific_days_of_a_year(year)

    elif option == '-a':
        try:
            year,month = [int(elem) for elem in year_month.split('/')]

            if year < min_year or year > max_year:
                print('Year should be in between', min_year, 'and', max_year)
                quit()

            if month < 1 or month > 12:
                print('Month should be in between 1 and 12')
                quit()
        except:
            print('INVALID Input')
            quit()

        display_averages_of_a_month(year, month)

    elif option == '-c':
        try:
            year, month = [int(elem) for elem in year_month.split('/')]

            if year < min_year or year > max_year:
                print('Year should be in between', min_year, 'and', max_year)
                quit()

            if month < 1 or month > 12:
                print('Month should be in between 1 and 12')
                quit()
        except:
            print('INVALID Input')

        draw_two_horizontal_bar_charts(year, month)
        print('----------------------------------------------')
        print('----------------------------------------------')
        print('----------------------------------------------')
        draw_one_horizontal_bar_chart(year, month)

    else:
        print('Invalid Option Try Again')
