image = ''
config = ''


def set_path(current, temp):
    global image
    global config
    image = current + "/images/"
    config = temp + '/config.xml'


def img(file=''):
    if file != '':
        return image + file + '.1334x750.png'
    else:
        return image


def cfg():
    return config
