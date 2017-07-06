image = ''
config = ''
iproxy = ''


def set_path(current):
    global image
    global config
    global iproxy
    iproxy = current + "/iproxy"
    image = current + "/images/"
    config = current + '/config.xml'


def img(file=None):
    if file is not None:
        return image + file + '.1334x750.png'
    else:
        return image


def cfg():
    return config


def ipr():
    return iproxy
