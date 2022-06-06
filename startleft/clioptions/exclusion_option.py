from click import Option, UsageError


class Exclusion(Option):
    def __init__(self, *args, **kwargs):
        self.mutually_exclusion = set(kwargs.pop('mutually_exclusion', []))
        self.mandatory = kwargs.pop('mandatory', False)
        help = kwargs.get('help', '')
        if self.mutually_exclusion:
            ex_str = ', '.join(self.mutually_exclusion)
            kwargs['help'] = help + (
                    ' NOTE: This argument is mutually exclusive with '
                    ' arguments: [' + ex_str + '].'
            )
        super(Exclusion, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        intersection = self.mutually_exclusion.intersection(opts)
        if intersection and self.name in opts:
            others = ', '.join(self.mutually_exclusion)
            raise UsageError(f'Invalid arguments: {self.name} is incompatible with: {others}')

        if self.mandatory and not intersection and self.name not in opts:
            raise UsageError(f'Missing one of this arguments: {self.mutually_exclusion.union([self.name])}')

        return super(Exclusion, self).handle_parse_result(
            ctx,
            opts,
            args
        )
