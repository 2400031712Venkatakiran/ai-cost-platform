import logging
import sys 
#Python uses a standard output stream to send output 
# to the terminal. The sys module gives us access to 
# that stream through sys.stdout 
# Logging means recording messages about what your application is doing.


def setup_logging(level: str = "INFO") -> None:
    """Configure application-wide logging to stdout."""
    logging.basicConfig(
        level=level.upper(),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        stream=sys.stdout,
        force=True,
    )
    # SQLAlchemy is very chatty at INFO level; keep it quiet unless it's a problem.
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)