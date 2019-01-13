from sqlalchemy import func, String, Text, type_coerce, TypeDecorator

""" From SQLAlchemy UsageRecipes:
https://bitbucket.org/zzzeek/sqlalchemy/wiki/UsageRecipes/DatabaseCrypt
"""


class PasswordType(TypeDecorator):
    impl = Text

    def bind_expression(self, bindvalue):
        """Apply a SQL expression to an incoming cleartext value being
        rendered as a bound parameter.

        For this example, this handler is intended only for the
        INSERT and UPDATE statements.  Comparison operations
        within a SELECT are handled below by the Comparator.

        """
        return func.crypt(bindvalue, func.gen_salt('bf', 8))

    class comparator_factory(String.comparator_factory):
        def __eq__(self, other):
            """Compare the local password column to an incoming cleartext
            password.

            This handler is invoked when a PasswordType column
            is used in conjunction with the == operator in a SQL
            expression, replacing the usage of the "bind_expression()"
            handler.

            """
            # we coerce our own "expression" down to String,
            # so that invoking == doesn't cause an endless loop
            # back into __eq__() here
            local_pw = type_coerce(self.expr, String)
            return local_pw == func.crypt(other, local_pw)
