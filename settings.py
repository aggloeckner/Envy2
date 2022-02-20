from os import environ

SESSION_CONFIGS = [
    dict(
        name = 'Envy',
        display_name = "Envy and Social Preferences",
        app_sequence = [ 'Welcome', 'LabIds', 'Consent', 'Instructions', 'Envy2', 'SeriousnessCheck' ],
        num_demo_participants = 2,
        sliders_per_column = 50,
        slider_columns = 3,
        max_slider_offset = 150,
        svo_file = "SVO_Full.csv"
    ),
    dict(
        name = 'Envy_test',
        display_name = "Envy and Social Preferences (Test)",
        app_sequence = [
        #    'Welcome',
        #    'LabIds',
        #    'Consent',
        #    'Instructions',
            'Envy2',
            'SeriousnessCheck' ],
        num_demo_participants = 2,
        sliders_per_column = 50,
        slider_columns = 3,
        max_slider_offset = 50,
        svo_file = "SVO_Testing.csv"
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point = 1.00,
    participation_fee = 0.00,
    doc = ""
)

PARTICIPANT_FIELDS = [ 'time_start' , 'time_end']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'de'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '9140961862942'
