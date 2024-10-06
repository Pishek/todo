import mimesis


class FakeGeneric(mimesis.Generic):
    """
    Custom class inherited from the mimesis.Generic and made for type hints only,
    because of mimesis.Generic set attributes dynamically for lazy initialization.
    """

    address: mimesis.Address
    choice: mimesis.Choice
    code: mimesis.Code
    datetime: mimesis.Datetime
    internet: mimesis.Internet
    numeric: mimesis.Numeric
    path: mimesis.Path
    person: mimesis.Person
    text: mimesis.Text
    cryptographic: mimesis.Cryptographic


fake = FakeGeneric(locale=mimesis.Locale.EN)
