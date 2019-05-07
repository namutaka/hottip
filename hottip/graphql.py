import logging
from time import time as timer

logger = logging.getLogger(__name__)

def timing_middleware(next, root, info, **args):
    if not root:
        logger.info("user:{user} - {field_name}: {vars}".format(
            user=info.context.user,
            field_name=info.field_name,
            vars=info.variable_values,
        ))

    return next(root, info, **args)