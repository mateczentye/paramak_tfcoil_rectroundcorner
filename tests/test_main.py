import paramak_tfcoil_rectroundcorner as ptfc
import pytest


pytest.importorskip('paramak')

obj = ptfc.ToroidalFieldCoilRectangleRoundCorners(
    lower_inner_coordinates= (50,0),
    mid_point_coordinates= (100,100),
    thickness= 20,
    distance= 10,
    number_of_coils= 1,
    )

@pytest.mark.value
def test_surface_area():
    paramak_area = obj.area
    print(paramak_area)
    package_area = ptfc.surface_area((50, 0),(100, 100), 20, 10)
    assert pytest.approx(package_area) == paramak_area

@pytest.mark.value
def test_volume():
    paramak_vol = ExtrudeMixedShape(
        points = find_points((50, 0), (100, 100), 20, line_type=True),
        distance=10,).volume
    package_vol = ptfc.volume((50, 0),(100, 100), 20, 10)
    assert pytest.approx(package_vol) == paramak_vol

test_surface_area()
