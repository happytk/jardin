import MoinMoin.events as ev
from MoinMoin.dayone_multi import DayoneMiddleware

def handle_page_changed(event):
    # comment = event.comment
    # page = event.page
    # request = event.request
    # trivial = isinstance(event, ev.TrivialPageChangedEvent)
    # subscribers = page.getSubscribers(request, return_users=1)
    # mail_from = page.cfg.mail_from
    pass

def handle_page_renamed(event):
    # event.page.page_name_fs (saved already)
    event.old_page.rename_page(event.page.page_name_fs)

def handle_page_deleted(event):
    event.page.delete_page()

def handle_page_reverted(event):
    # name = event.page.page_name
    # logging.info('reverted ' + name + ',' + event.previous + ',' + event.current)
    pass

def handle_page_copied(event):
    # name = event.page.page_name
    # logging.info('copied ' + name)
    pass

def handle(event):
    """An event handler"""

    if isinstance(event, (ev.PageChangedEvent, ev.TrivialPageChangedEvent)):
        return handle_page_changed(event)
    elif isinstance(event, ev.PageRenamedEvent):
        return handle_page_renamed(event)
    elif isinstance(event, ev.PageDeletedEvent):
        return handle_page_deleted(event)
    elif isinstance(event, ev.PageCopiedEvent):
        return handle_page_copied(event)
    elif isinstance(event, ev.PageRevertedEvent):
        return handle_page_reverted(event)
