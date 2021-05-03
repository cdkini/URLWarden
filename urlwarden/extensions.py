from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_session import Session

debug_toolbar: DebugToolbarExtension = DebugToolbarExtension()
cache: Cache = Cache(config={
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 900
})
session: Session = Session()
