"""
final_image_data.py
-----------------------------------
Summary:
    This project turns text data into visual images using Red as an indication of a high number.
    The data text file has a header, number of values line, and values ranging from 0 to 1.0
    These values are fractions and are ordered from past to most recent.
    Each value represents 1 stripe that will be shaded in to represent a high or low number.
    This Program accepts 4 data files and are displayed at the same time.
    In the end, there will be 4 colorful rectangles filled with colorful lines all from actual data.
    An image with statistical meaning behind it.
Data.txt format:
    1st line = what data represents & range of time
    2nd line = number of fractions (data values) present
    3rd & beyond = values that range from 0 to 1.0 (fractions)
"""
from simpleimage import SimpleImage
import sys

PROJECT_SUMMARY = 'bar_descriptions.txt'
DATA_REF = 'text data/data-test.txt'
DATA1 = 'text data/data-climate.txt'
DATA2 = 'text data/data-illiteracy.txt'
DATA3 = 'text data/data-child-mortality.txt'

BLUE = 127
RED = 255

BAR_WIDTH = 1100
BAR_HEIGHT = 200

FILES_NUM = 4


def main():
    description(PROJECT_SUMMARY)
    print('')
    ask2show = input('Press ENTER to see image.')

    if ask2show == '':
        data_square()
    else:
        sys.exit()


def data_square():
    print('')
    print('LOADING...')
    total_height = BAR_HEIGHT * FILES_NUM
    big_image = SimpleImage.blank(BAR_WIDTH, total_height)
    add_bar(DATA_REF, 0, big_image)
    add_bar(DATA1, 1, big_image)
    add_bar(DATA2, 2, big_image)
    add_bar(DATA3, 3, big_image)

    print('DISPLAYING IMAGE...')
    big_image.show()
    print('EXITING...')


def add_bar(file, row, big_image):
    data_bar = image_data_bar(file)
    for y in range(BAR_HEIGHT):
        for x in range(BAR_WIDTH):
            pixel = data_bar.get_pixel(x, y)
            big_image.set_pixel(x, y + BAR_HEIGHT * row, pixel)
    return big_image


def image_data_bar(text_file):
    # note: fraction & stripe represent same thing (fraction = number form; stripe = visual form)
    # fraction = 1 fractional number (float) representing 1 colored stripe on whole image

    data_list = get_data(text_file)
    total_stripes = int(data_list.pop(0))  # removes total floats LINE & converts float to int
    red_list = data2red(data_list)  # returns list of red RGB values
    green_list = red2green(red_list)  # returns list of green RGB values

    all_stripes = stripes(total_stripes, red_list, green_list)
    resize(all_stripes)  # resizes to desired width

    return all_stripes


def resize(final_image):
    resize_image = SimpleImage.blank(BAR_WIDTH, BAR_HEIGHT)
    final_image.make_as_big_as(resize_image)


def stripes(total_stripes, red_list, green_list):
    """
    :param green_list: list full of green values to be applied to 1 stripe per index of list
    :param red_list: list full of red values to be applied to 1 stripe per index of list
    :param total_stripes: number of stripes that we have
    :return: final image with all stripes
    """
    # divisible width is a number that is divisible by the total number giving back a int instead of a float
    # CANVAS WIDTH is the desired width, will resize to this width later
    divisible_width = (BAR_WIDTH // total_stripes) * total_stripes
    stripe_width = divisible_width // total_stripes
    stripe = SimpleImage.blank(stripe_width, BAR_HEIGHT)
    all_stripes = SimpleImage.blank(divisible_width, BAR_HEIGHT)  # size of all stripes combined

    # making total amount of stripes & taking red out of red_list
    for i in range(total_stripes):
        red_val = red_list[i]
        green_val = green_list[i]

        # adding colors to 1 stripe
        for pixel in stripe:
            pixel.red = red_val
            pixel.green = green_val
            pixel.blue = BLUE

        # add 1 color to 1 stripe to all_stripes
        for y in range(BAR_HEIGHT):
            for x in range(stripe_width):
                pixel = stripe.get_pixel(x, y)
                all_stripes.set_pixel(stripe_width * i + x, y, pixel)
    return all_stripes


def red2green(red_list):
    """
    :param red_list: list full of RGB red values
    :return: list full of RGB green values

    >>> red2green([255.0, 145.0, 0])
    [0, 145.0, 255.0]
    """
    green_list = red_list[::-1]  # [Start:Stop:Steps]
    return green_list


def data2red(fraction_list):
    """
    Turns data fraction number into red number for RGB value.
    These red are in a list & is reveresed to get a contrasting green list
    Returns Red and Green value list

    >>> data2red([1.0, 0.5, 0])
    [255.0, 127.5, 0]
    """
    fraction2red = []

    for i in range(len(fraction_list)):
        fraction_list[i] *= RED
        fraction2red.append(fraction_list[i])

    return fraction2red


def get_data(filename):
    # get strings from file & returns as list of floats, skipping 1st line
    data_list = []
    with open(filename) as f:
        next(f)  # skips header line
        for line in f:
            line = line.rstrip()  # strips whitespaces right of lines
            data_list.append(float(line))  # adds each line to list
    return data_list


def description(summary_file):
    with open(summary_file) as f:
        for line in f:
            line = line.strip()
            print(line)


if __name__ == '__main__':
    main()
