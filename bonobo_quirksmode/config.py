from bonobo.config import use_context_processor


def set_output_type(output_type):
    def set_output_type_wrapper(f):
        def _set_output_type_context_processor(self, context):
            nonlocal output_type
            context.set_output_type(output_type)
            yield

        return use_context_processor(_set_output_type_context_processor)(f)

    return set_output_type_wrapper


def set_output_fields(fields, typename='Bag'):
    def set_output_fields_wrapper(f):
        def _set_output_fields_context_processor(self, context):
            nonlocal fields, typename
            context.set_output_fields(fields, typename=typename)
            yield

        return use_context_processor(_set_output_fields_context_processor)(f)

    return set_output_fields_wrapper


def use_output_type(f):
    def _use_output_type_context_processor(self, context):
        yield (context.output_type,)

    return use_context_processor(_use_output_type_context_processor)(f)


@use_output_type
@set_output_fields(['a', 'b'])
def x(OutputType):
    yield OutputType(
        a=1,
        b=2,
    )
    yield OutputType(
        b=3,
        a=4,
    )


if __name__ == '__main__':
    import bonobo, mondrian

    mondrian.term.istty = True
    graph = bonobo.Graph(
        x,
        bonobo.PrettyPrinter(),
    )
    bonobo.run(graph)
