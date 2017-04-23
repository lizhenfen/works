import os

BASEPATH = os.path.dirname(__file__)
settings = {
            "template_path": os.path.join( os.path.dirname(BASEPATH), "templates"),
            "static_path": os.path.join( os.path.dirname(BASEPATH), "statics"),
            "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            #"debug": True,
            "login_url": '/login'
        }


port = 9000
