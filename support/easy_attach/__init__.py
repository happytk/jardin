import os
import re
import logging
import shutil
import flask
from hashlib import sha1

try:
    import localconfig as config
except ImportError:
    from . import config_default as config

easy_attach_page = flask.Blueprint(
    'easy_attach_page',
    __name__,
    template_folder='templates',
    static_folder='static')

UNSAFE = re.compile(r'[^a-zA-Z0-9_]+')


def safe_addr(ip_addr):
    """Strip of the trailing two octets of the IP address."""
    return '.'.join(ip_addr.split('.')[:2] + ['xxx', 'xxx'])


def save_normalized_image(data_dir, filename, data):

    from PIL import Image, ImageFile
    from pilkit.processors import Transpose

    path = os.path.join(data_dir, filename)

    image_parser = ImageFile.Parser()
    try:
        image_parser.feed(data)
        image = image_parser.close()
    except IOError:
        raise
        return False

    if config.SAVE_ORIGINAL_IMAGE:
        if not os.path.isdir(config.DATA_DIR):
            try:  # Reset saved files on each start
                # rmtree(DATA_DIR, True)
                os.mkdir(config.DATA_DIR)
            except OSError:
                raise
                return False
        image.save(os.path.join(config.DATA_DIR, filename))

    try:
        image = Transpose().process(image)
    except (IOError, IndexError):
        pass

    image.thumbnail(config.MAX_IMAGE_SIZE, Image.ANTIALIAS)
    if image.mode != 'RGB':
        image = image.convert('RGB')

    image.save(path)
    return True


def get_filename(data):
    sha1sum = sha1(data).hexdigest()
    # target = os.path.join(data_dir, '{0}.jpg'.format(sha1sum))
    return sha1sum


@easy_attach_page.route('/configuration', methods=['POST', 'GET'])
def configuration():
    return flask.jsonify(
        flask.current_app.config
    )


@easy_attach_page.route('/post', methods=['POST', 'GET'])
def post():
    filename = flask.request.values.get('filename', '').lower()
    data_dir = flask.request.values.get('path', None)
    direct = flask.request.values.get('direct', 'false')

    if data_dir is None:
        return 'storage-path is not specified.'

    if not os.path.isdir(data_dir):
        try:
            os.mkdir(data_dir)
        except:  # noqa
            return "Couldn't create upload-directory: {}".format(data_dir)

    def _save_direct():
        f = filename
        target = os.path.join(data_dir, f)

        if os.path.isfile(target) or os.path.isdir(target):
            return 'FAIL/%s exists already.' % f

        try:
            open(target, 'wb').write(flask.request.data)
        except Exception as e:
            return '{0}'.format(e)

        return 'success' + '/' + f

    if direct == 'false' and (
            filename.endswith('.jpg') or filename.endswith('.jpeg')):

        sha1sum = get_filename(flask.request.data)
        target = '{0}.jpg'.format(sha1sum)
        try:
            tf = os.path.join(data_dir, target)
            if os.path.isfile(tf) or os.path.isdir(tf):
                return 'FAIL/%s exists already.' % target
            if save_normalized_image(data_dir, target, flask.request.data):
                pass
        except ImportError:
            logging.critical('Image normalizing failed (import error)')
            return _save_direct()

        except Exception as e:  # Output errors
            return 'FAIL/{0}'.format(e)

        return 'success' + '/' + '{0}.jpg'.format(sha1sum)

    else:
        return _save_direct()


if __name__ == "__main__":
    def convert(filename):
        if filename.endswith('.jpg') or filename.endswith('.jpeg'):
            data = open(filename, 'rb').read()
            sha1sum = get_filename(data)
            target = '{0}.jpg'.format(sha1sum)
            try:
                save_normalized_image('.', target, data)
                shutil.move('./' + filename, '/tmp/' + filename)
            except Exception as e:  # Output errors
                print(e)
        else:
            pass

    def convert_all():
        import glob
        for imgfn in glob.glob('*.jpg'):
            print('converting ' + imgfn + '...')
            convert(imgfn)
