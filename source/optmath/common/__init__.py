import os

IS_TEST_SESSION = os.environ["IS_TEST_SESSION"] == "yes"
IS_DEBUG_SESSION = os.environ["IS_DEBUG_SESSION"] == "yes"
IS_PRODUCTION_SESSION = not IS_TEST_SESSION and not IS_DEBUG_SESSION
