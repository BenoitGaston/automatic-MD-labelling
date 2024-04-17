import os
import base64
list_of_images_dict = []

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


num_of_labels = len(list_of_images_dict)

num_of_splits = int(num_of_labels/14)+1

list_of_lists = [list_of_images_dict[k*14:(k+1)*(14)] for k in range(num_of_splits)]

for l in range(len(list_of_lists)):
    list_of_images = list_of_lists[l]

    open('temp-1.svg', 'w').write(open('MD-Labels-Template.svg').read())
    open('temp-2.svg', 'w').write(open('MD-Labels-Template.svg').read())


        #encoded_string = str(encoded_string)[2:20]
                                                            
    for i in range(1,len(list_of_images)+1):
        image_dict = list_of_images[i-1]

        open(f'temp-2.svg', 'w').write(open(f'temp-1.svg').read().replace(f'>title {i}</tspan>',f'>{image_dict["Title"]}</tspan>'))
        open(f'temp-1.svg', 'w').write(open(f'temp-2.svg').read().replace(f'>year {i}</tspan>',f'>{image_dict["Year"]}</tspan>'))
        open(f'temp-2.svg', 'w').write(open(f'temp-1.svg').read().replace(f'>artist {i}</tspan>',f'>{image_dict["Artist"]}</tspan>'))
        if len(image_dict["Artist"])>0:
            open(f'temp-1.svg', 'w').write(open(f'temp-2.svg').read().replace(f'>artist {i} - title {i}</tspan>',f'>{image_dict["Artist"]} - {image_dict["Title"]}</tspan>'))
        else:
            open(f'temp-1.svg', 'w').write(open(f'temp-2.svg').read().replace(f'>artist {i} - title {i}</tspan>',f'>{image_dict["Title"]}</tspan>'))
        
        open(f'temp-2.svg', 'w').write(open(f'temp-1.svg').read().replace(f'xlink:href="data:image/png;base64, image_number_{i}"',f'xlink:href="data:image/png;base64, {image_dict["Image"]}"'))
        open(f'temp-1.svg', 'w').write(open(f'temp-2.svg').read())

    open(f'MinidiscLabels-{l+1}.svg', 'w').write(open('temp-2.svg').read())
    os.remove('temp-1.svg')
    os.remove('temp-2.svg')