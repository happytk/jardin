#!/opt/bin/python
#-*-encoding:utf-8-*-
from ridibooks_hls import ridibooks_hls_getter
from dayone_helper import Entry
from pprint import pprint
import os
import sys
import datetime
import baker
import logging
import logging.config

logging.config.fileConfig('/volume1/moindev/config/ridibooks_hls_logging.conf')


RIDIBOOKS_ID = 'happytk'
RIDIBOOKS_PW = 'power123'
MOIN_RESULT_PATH = '/volume1/moindev/wiki-mei/data/quote_notes/DelightfulQuotes/'

def to_moin_format(results, under=None):
    t = []
    imgs = []
    for r in results:
        highlights = [h[1] for h in r['highlights'] if h[0] == under or under is None]
        if len(highlights) > 0:
            t.append('= %s(%s) =' % (r['title'], r['author'],))
            imgs.append('{{%s}}' % r['bookimg_s'])
            for h in highlights:
                t.append('{{{\n%s\n}}}\n' % h.strip())
    output = []
    if len(imgs) or len(t):
        imgs = '\n'.join(imgs)
        t = '\n'.join(t)

        # imgs = imgs.encode('utf8')
        # t = t.encode('utf8')

        output.append(imgs)
        output.append('\n\n')
        output.append(t)

    return ''.join(output)


def get(under=None, color=None, refresh=False):
    logging.info('finding note after the day - %s' % under)

    ridi = ridibooks_hls_getter()
    ridi.login(RIDIBOOKS_ID, RIDIBOOKS_PW)

    def _gen():
        for dt, book_id in ridi.timeline(under=under):
            r = ridi.reading_note(book_id, under=under, color=color)
            if r:
                logging.info('%s %s %s' % (dt, 'book-id:', book_id,))
                yield r

    return [r for r in _gen()]


def save_to_dayone(basepath, results, under=None):
    delta_seconds = 0
    for r in results:
        for dt, highlight in r['highlights']:
            if under is None or dt == under:
                entry = Entry(highlight.strip(), basepath=basepath)
                # for keeping the order
                entry.date = datetime.datetime.strptime(dt, '%Y%m%d') + datetime.timedelta(days=1) - datetime.timedelta(seconds=delta_seconds)
                delta_seconds += 1
                entry.tags = ['ridibooks', r['title'], r['author']]
                entry.save()
                logging.info('saved to %s' % entry.filepath)


def save_to_tk(results, under=None):
    save_to_dayone('/volume1/homes/me/dropbox/Apps/Day One/Journal.dayone/entries', results, under)


def save_to_mei(results, under=None):
    save_to_dayone('/volume1/homes/me/dropbox_happytk/Apps/Day One (1)/Journal.dayone/entries', results, under)


def print_(results, under=None):
    for r in results:
        for dt, highlight in r['highlights']:
            if under is None or dt == under:
                print highlight.strip()


def save_to_moin(results, under=None):
    output_moin = to_moin_format(results, under)
    if len(output_moin):
        if under:   
            filename = under[:4] + '-' + under[4:6] + '-' + under[6:8] + '.md'
        else:
            filename = 'all-%s.md' % datetime.datetime.now().strftime('%Y%m%d')
        filepath = os.path.join(MOIN_RESULT_PATH, filename)
        print 'saving to .. ', filepath

        with open(filepath, 'wt') as f:
            f.write(output_moin.encode('utf8'))
    else:
        print 'No output to write. You should read a book.'


def get_and_save(under, moin=False, tk_dayone=False, mei_dayone=False, stdout=False, color=None):
    results = get(under, color)
    if moin:
        save_to_moin(results, under)
    if tk_dayone:
        save_to_tk(results, under)
    if mei_dayone:
        save_to_mei(results, under)
    if stdout:
        print_(results, under)
    if not(moin or tk_dayone or mei_dayone or stdout):
        print len(results)


@baker.command
def ymd(yyyymmdd, moin=False, dayone=False, mei=False, stdout=False, color=None):
    _ = datetime.datetime.strptime(yyyymmdd, '%Y%m%d')
    get_and_save(yyyymmdd, moin, dayone, mei, stdout, color)


@baker.command
def delta(delta, moin=False, dayone=False, mei=False, stdout=False, color=None):
    under = datetime.datetime.today() - datetime.timedelta(days=int(delta))
    under = under.strftime("%Y%m%d")
    get_and_save(under, moin, dayone, mei, stdout, color)


@baker.command
def all(moin=False, dayone=False, mei=False, stdout=False, color=None):
    get_and_save(None, moin, dayone, mei, stdout, color)


if __name__ == "__main__":
    baker.run()
