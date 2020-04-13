from flask import current_app


def debug(msg, *args, **kwargs):
    return current_app.logger.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    return current_app.logger.info(msg, *args, **kwargs)


def warn(msg, *args, **kwargs):
    return current_app.logger.warn(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    return current_app.logger.error(msg, *args, **kwargs)
