#!/usr/bin/env python
# crate_anon/nlp_manager/models.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column, Index, MetaData
from sqlalchemy.types import BigInteger, DateTime, String

from crate_anon.anonymise.constants import (
    MAX_PID_STR,
    MYSQL_TABLE_KWARGS,
)
from crate_anon.nlp_manager.constants import (
    HashClass,
    MAX_STRING_PK_LENGTH,
    SqlTypeDbIdentifier,
)

progress_meta = MetaData()
ProgressBase = declarative_base(metadata=progress_meta)


# =============================================================================
# Global constants
# =============================================================================

encrypted_length = len(HashClass("dummysalt").hash(MAX_PID_STR))
SqlTypeHash = String(encrypted_length)


# =============================================================================
# Record of progress
# =============================================================================

class NlpRecord(ProgressBase):
    """
    Class to record the fact of processing a source record (and to keep a hash
    allowing identification of altered source contents later).
    """
    __tablename__ = 'crate_nlp_progress'
    __table_args__ = (
        Index('_idx1',  # index name
              # index fields:
              'srcpkval',   # integer and most specific
              'nlpdef',     # usually >1 NLP def to 1 db/table/field combo
              'srcfield',   # } roughly, more to less specific?
              'srctable',   # }
              'srcdb',      # }
              'srcpkstr',   # last as we may not use it
              # - performance is critical here
              # - put them in descending order of specificity
              #   http://stackoverflow.com/questions/2292662/how-important-is-the-order-of-columns-in-indexes  # noqa
              # - start with srcpkval, as it's (a) specific and (b) integer
              # - srcpkfield: don't need to index, because the source table
              #   can only have one PK
              # - srcpkstr: must include, since srcpkval can be non-unique,
              #   due to hash collisions, if we're using a string
              #   ... but ?should be last because we may not use it in
              #   queries (for tables with integer PK)
              unique=True),
        MYSQL_TABLE_KWARGS
    )
    # http://stackoverflow.com/questions/6626810/multiple-columns-index-when-using-the-declarative-orm-extension-of-sqlalchemy  # noqa
    # http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/table_config.html  # noqa

    pk = Column(
        'pk', BigInteger, primary_key=True, autoincrement=True,
        doc="PK of NLP record (no specific use)")
    srcdb = Column(
        'srcdb', SqlTypeDbIdentifier, doc="Source database"
        # primary_key=True
    )
    srctable = Column(
        'srctable', SqlTypeDbIdentifier, doc="Source table name"
        # primary_key=True
    )
    srcpkfield = Column(
        'srcpkfield', SqlTypeDbIdentifier,
        doc="Primary key column name in source table (for info only)")
    srcpkval = Column(
        'srcpkval', BigInteger,
        doc="Primary key value in source table (or hash if PK is a string)"
        # primary_key=True
    )
    srcpkstr = Column(
        'srcpkstr', String(MAX_STRING_PK_LENGTH),
        doc="Original string PK, used when the table has a string PK, to deal "
            "with hash collisions. Max length: {}".format(
            MAX_STRING_PK_LENGTH)
        # primary_key=True, default=''  # can't have a NULL in a composite PK
    )
    srcfield = Column(
        'srcfield', SqlTypeDbIdentifier,
        doc="Name of column in source field containing actual data"
        # primary_key=True
    )
    nlpdef = Column(
        'nlpdef', SqlTypeDbIdentifier,
        doc="Name of natural language processing definition that source was "
            "processed for"
        # primary_key=True
    )
    whenprocessedutc = Column(
        'whenprocessedutc', DateTime,
        doc="Time that NLP record was processed")
    srchash = Column(
        'srchash', SqlTypeHash,
        doc='Secure hash of source field contents at the time of processing')