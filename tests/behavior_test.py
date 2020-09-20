import kivyhelper.widgets as wd


class TestTooltipBehavior:
    def test_mod_mouse_pos(self):
        tt = wd.TooltipBehavior(size=(100, 500))
        assert tt._mod_mouse_pos(500, 500, (1920, 1080)) == (500, 500)
        assert tt._mod_mouse_pos(1900, 500, (1920, 1080)) == (1820, 500)
        assert tt._mod_mouse_pos(500, 1000, (1920, 1080)) == (500, 580)
        tt.edge_padding = 10
        assert tt._mod_mouse_pos(-50, 500, (1920, 1080)) == (10, 500)

    def test_get_edge_pos(self):
        tt = wd.TooltipBehavior(size=(100, 500))
        # Test default settings:
        assert tt._get_edge_pos(500, 1000) == (500, 1500, 600, 1000)
        # Test left position:
        tt.relative_x = 'left'
        assert tt._get_edge_pos(500, 1000) == (400, 1500, 500, 1000)
        # Test below position:
        tt.relative_y = 'below'
        assert tt._get_edge_pos(500, 1000) == (400, 1000, 500, 500)
        # Test center:
        tt.relative_x = 'center'
        tt.relative_y = 'center'
        assert tt._get_edge_pos(500, 1000) == (450, 1250, 550, 750)

    def test_mod_props(self):
        tt = wd.TooltipBehavior(size=(100, 500))
        # Test default settings:
        assert tt.width == 100
        assert tt.height == 500
        assert tt.x_mod == 0
        assert tt.y_mod == 0
        # Test relative_y changes:
        tt.relative_y = 'below'
        assert tt.x_mod == 0
        assert tt.y_mod == -500
        tt.relative_y = 'center'
        assert tt.x_mod == 0
        assert tt.y_mod == -250
        # Test relative_x changes:
        tt.relative_y = 'above'
        tt.relative_x = 'left'
        assert tt.x_mod == -100
        assert tt.y_mod == 0
        tt.relative_x = 'center'
        assert tt.x_mod == -50
        assert tt.y_mod == 0
