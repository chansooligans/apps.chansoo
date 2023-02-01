import pandas as pd
from glob import glob
fp = "../cache"

reload=False

def localcache(name=None, dtype=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if name:
                filename = f"{fp}/{name}"
            else:
                filename = f"{fp}/{func.__name__}.csv"

            if (filename in glob(f"{fp}/*")) & (reload == False):
                df = pd.read_csv(filename, dtype=dtype)
            else:
                df = func(*args, **kwargs)
                df.to_csv(filename, index=False)
            return df
        return wrapper
    return decorator