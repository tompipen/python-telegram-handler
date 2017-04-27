import logging

from copy import copy

from django.views.debug import ExceptionReporter

# from telegram_handler.utils import escape_html

from django.template.defaultfilters import force_escape as escape_html

__all__ = ['TelegramFormatter', 'MarkdownFormatter', 'HtmlFormatter']


class TelegramFormatter(logging.Formatter):
    """Base formatter class suitable for use with `TelegramHandler`"""

    fmt = "%(asctime)s %(levelname)s\n[%(name)s:%(funcName)s]\n%(message)s"
    parse_mode = None

    def __init__(self, fmt=None, *args, **kwargs):
        super(TelegramFormatter, self).__init__(fmt or self.fmt, *args, **kwargs)


class MarkdownFormatter(TelegramFormatter):
    """Markdown formatter for telegram."""
    fmt = '`%(asctime)s` *%(levelname)s*\n[%(name)s:%(funcName)s]\n%(message)s'
    parse_mode = 'Markdown'

    def formatException(self, *args, **kwargs):
        string = super(MarkdownFormatter, self).formatException(*args, **kwargs)
        return '```%s```' % string


class EMOJI:
    WHITE_CIRCLE = '\xE2\x9A\xAA'
    BLUE_CIRCLE = '\xF0\x9F\x94\xB5'
    RED_CIRCLE = '\xF0\x9F\x94\xB4'


class HtmlFormatter(TelegramFormatter):
    """HTML formatter for telegram."""
    fmt = '<code>%(asctime)s</code> <b>%(levelname)s</b>\n<pre>From %(name)s:%(funcName)s\n%(message)s</pre>'
    parse_mode = 'HTML'

    def __init__(self, *args, **kwargs):
        self.use_emoji = kwargs.pop('use_emoji', False)
        super(HtmlFormatter, self).__init__(*args, **kwargs)

    def format(self, record, limit=4096):
        """
        :param record: logging.Record 
        :param limit: default 4096
        :return: 
        """

        try:
            request = record.request

            if getattr(request, 'POST', None) is None:
                request = None
        except Exception:

            request = None

        # Since we add a nicely formatted traceback on our own, create a copy
        # of the log record without the exception data.
        # no_exc_record = copy(record)
        # no_exc_record.exc_info = None
        # no_exc_record.exc_text = None

        # if record.exc_info:
        #     exc_info = record.exc_info
        # else:
        #     exc_info = (None, record.getMessage(), None)
        #
        # if record.exc_info:
        #     exc_info = record.exc_info
        # else:
        #     exc_info = (None, record.getMessage(), None)

        # reporter = ExceptionReporter(request, is_email=True, *exc_info)
        #
        # message = "%s\n\n%s" % (
        #     super(HtmlFormatter, self).format(no_exc_record),
        #     escape_html(
        #         reporter.get_traceback_text()
        #     )
        # )

        message = super(HtmlFormatter, self).format(record)

        return message

        # return '<pre>{0}</pre>'.format(
        #     message if len(message) <= limit
        #     else message[:limit]
        # )

