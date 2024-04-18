import os
import base64
import datetime
list_of_images_dict = []

back_ground_color_template = '211e1e'
text_color_template = 'ffffff'

black = '000000'
white = 'ffffff'

yellow = 'ffd42a'
red = 'ff2a2a'
green = '00ff00'
orange = 'ff6600'
purpule = '892ca0'
blue = '3737c8'

classical_theme = (yellow, black,'classical')
jazz_theme = (blue, white,'jazz')
electro_theme = (purpule, green,'electro')
pop_theme = (orange, black,'pop')
rock_theme = (red, black,'rock')

default_theme = (back_ground_color_template, text_color_template,'default')


back_ground_color,text_color,theme_name = rock_theme

for full_file_name in os.listdir():

    if full_file_name.endswith('.jpg') or full_file_name.endswith('.png'):
        image_dict = {}
        file_name = full_file_name.replace('.jpg','').replace('.png','')
        if len(file_name.split('-')) == 1:
            image_dict['Title'] = file_name.split('-')[0].strip()
            image_dict['Artist'] = ''
            image_dict['Year'] = ''
        elif len(file_name.split('-')) == 2:

            image_dict['Title'] = file_name.split('-')[0].strip()
            image_dict['Artist'] = file_name.split('-')[1].strip()
            image_dict['Year'] = ''
        elif len(file_name.split('-')) == 3:

            image_dict['Title'] = file_name.split('-')[0].strip()
            image_dict['Artist'] = file_name.split('-')[1].strip()
            image_dict['Year'] = file_name.split('-')[2].strip()
        else:
            print(f'Too many "-" in file {file_name}')
    
        with open(full_file_name, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('ascii')
            image_dict['Image'] = encoded_string
        list_of_images_dict.append(image_dict)

# Inner Label
num_of_labels = len(list_of_images_dict)

num_of_splits = int(num_of_labels/14)+1

list_of_lists = [list_of_images_dict[k*14:(k+1)*(14)] for k in range(num_of_splits)]

now = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")

def update_temp_svg_with_image_information(image_dict):

    open(f'temp-2.svg', 'w').write(open(f'temp-1.svg').read().replace(f'fill:#{back_ground_color_template};',f'fill:#{back_ground_color};'))
    open(f'temp-1.svg', 'w').write(open(f'temp-2.svg').read().replace(f'fill:#{text_color_template};fill',f'fill:#{text_color};fill'))
    open(f'temp-2.svg', 'w').write(open(f'temp-1.svg').read().replace(f'>title {i}</tspan>',f'>{image_dict["Title"]}</tspan>'))
    open(f'temp-1.svg', 'w').write(open(f'temp-2.svg').read().replace(f'>year {i}</tspan>',f'>{image_dict["Year"]}</tspan>'))
    open(f'temp-2.svg', 'w').write(open(f'temp-1.svg').read().replace(f'>artist {i}</tspan>',f'>{image_dict["Artist"]}</tspan>'))
    if len(image_dict["Artist"])>0:
        open(f'temp-1.svg', 'w').write(open(f'temp-2.svg').read().replace(f'>artist {i} - title {i}</tspan>',f'>{image_dict["Artist"]} - {image_dict["Title"]}</tspan>'))
    else:
        open(f'temp-1.svg', 'w').write(open(f'temp-2.svg').read().replace(f'>artist {i} - title {i}</tspan>',f'>{image_dict["Title"]}</tspan>'))
    
    open(f'temp-2.svg', 'w').write(open(f'temp-1.svg').read().replace(f'xlink:href="data:image/png;base64, image_number_{i}"',f'xlink:href="data:image/png;base64, {image_dict["Image"]}"'))
    open(f'temp-1.svg', 'w').write(open(f'temp-2.svg').read())


for l in range(len(list_of_lists)):
    list_of_images = list_of_lists[l]

    open('temp-1.svg', 'w').write(open('MD-Labels-Inner-Template.svg').read())
    open('temp-2.svg', 'w').write(open('MD-Labels-Inner-Template.svg').read())


        #encoded_string = str(encoded_string)[2:20]
                                                            
    for i in range(1,len(list_of_images)+1):
        image_dict = list_of_images[i-1]

        update_temp_svg_with_image_information(image_dict)

        

    open(f'MD-Labels-In-{theme_name}-{now}-page {l+1}.svg', 'w').write(open('temp-2.svg').read())
    os.remove('temp-1.svg')
    os.remove('temp-2.svg')

# 2 Outer Label

num_of_splits = int(num_of_labels/7)+1

list_of_lists = [list_of_images_dict[k*7:(k+1)*(7)] for k in range(num_of_splits)]

for l in range(len(list_of_lists)):
    list_of_images = list_of_lists[l]

    open('temp-1.svg', 'w').write(open('MD-Labels-Outer-Template.svg').read())
    open('temp-2.svg', 'w').write(open('MD-Labels-Outer-Template.svg').read())

        #encoded_string = str(encoded_string)[2:20]
                                                            
    for i in range(1,len(list_of_images)+1):
        image_dict = list_of_images[i-1]

        update_temp_svg_with_image_information(image_dict)

    open(f'MD-Labels-Out-{theme_name}-{now}-page {l+1}.svg', 'w').write(open('temp-2.svg').read())
    os.remove('temp-1.svg')
    os.remove('temp-2.svg')
