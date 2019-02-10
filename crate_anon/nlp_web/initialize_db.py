import os
import sys
from typing import List

from sqlalchemy import engine_from_config
from pyramid.paster import (
    get_appsettings,
    # setup_logging,
)

from crate_anon.nlp_web.models import (
    DBSession,
    SessionForCelery,
    Base,
)


def usage(argv: List[str]):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv: List[str] = sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    # setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)