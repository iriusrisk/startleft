from vsdx import Shape, VisioFile


def get_shape_name(shape: Shape):
    return shape.text.replace('\n', '')


def read_visio_main_page(visio_filename):
    with VisioFile(visio_filename) as vis:
        return vis.pages[0]


def read_shape_by_name(visio_filename: str, shape_name: str) -> Shape:
    page = read_visio_main_page(visio_filename)
    for shape in page.child_shapes:
        if get_shape_name(shape) == shape_name:
            return shape
