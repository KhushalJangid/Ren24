# settings.py
import sentry_sdk

sentry_sdk.init(
    dsn="https://6ca2d413a490f99ba2658e6c92f6ed9e@o4506847830736896.ingest.sentry.io/4506847832506368",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)