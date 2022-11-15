from pytest import mark

from slp_mtmt.slp_mtmt.util.math.line_utils import get_limit


class TestLineUtils:

    @mark.parametrize('x1, y1, x2, y2, expected_x, expected_y, limit_min, limit_max', [
        (100, 100, 100, 50, 100, 500, 0, 500),
        (50, 100, 100, 100, 500, 100, 0, 500),
        (200, 200, 320, 80, 500, -100, 0, 500),
        (40, 240, 160, 120, 500, -220, 0, 500),
        (40, 360, 210, 297, 1011.4285714285714, 0, 0, 500),
        (240, 440, 360, 320, 680, 0, 0, 500),
        (280, 440, 400, 320, 720, 0, 0, 500),
        (320, 440, 459, 338, 919.6078431372549, 0, 0, 500),
        (240, 480, 127, 100, 0, -327.07964601769913, 0, 500),
        (330, 280, 436, 330, 796.4, 500, 0, 500),
        (240, 250, 156, 442, 0, 798.5714285714286, 0, 500),
        (90, 390, 60, 412, -60, 500, 0, 500),

    ])
    def test_get_line(self, x1, y1, x2, y2, expected_x, expected_y, limit_min, limit_max):

        limit = get_limit(x1, y1, x2, y2, limit_min, limit_max)
        assert limit == (expected_x, expected_y)
