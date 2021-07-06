import pytest
from paramak_tfcoil_rectroundcorner.core import ToroidalFieldCoilRectangleRoundCorners
from paramak_tfcoil_rectroundcorner.test_module import volume, surface_area
pytest.importorskip('paramak')
#import paramak_tfcoil_rectroundcorner as ptfc


obj = ToroidalFieldCoilRectangleRoundCorners(
    lower_inner_coordinates= (50,0),
    mid_point_coordinates= (100,100),
    thickness= 20,
    distance= 10,
    number_of_coils= 1,
    with_inner_leg=False
    )

obj2 = ToroidalFieldCoilRectangleRoundCorners(
    lower_inner_coordinates= (50,0),
    mid_point_coordinates= (100,100),
    thickness= 20,
    distance= 10,
    number_of_coils= 1,
    with_inner_leg=True
    )

@pytest.mark.parametric
#@pytest.mark.skip
def test_parametric_surface_area_wLeg():
    paramak_area = obj2.area
    [print(val) for val in obj2.areas]
    package_area = surface_area((50, 0),(100, 100), 20, 10,with_inner_leg=True)
    assert pytest.approx(package_area) == paramak_area

@pytest.mark.parametric
#@pytest.mark.skip
def test_parametric_volume_wLeg():
    paramak_vol = obj2.volume
    package_vol = volume((50, 0),(100, 100), 20, 10,with_inner_leg=True)
    assert pytest.approx(package_vol) == paramak_vol

@pytest.mark.parametric
def test_parametric_surface_area():
    paramak_area = obj.area
    package_area = surface_area((50, 0),(100, 100), 20, 10)
    assert pytest.approx(package_area) == paramak_area

@pytest.mark.parametric
def test_parametric_volume():
    paramak_vol = obj.volume
    package_vol = volume((50, 0),(100, 100), 20, 10)
    assert pytest.approx(package_vol) == paramak_vol

@pytest.mark.analytical
def test_manual_area():
    analytical = 19872.92
    computational = surface_area((50, 0),(100, 100), 20, 10)
    assert pytest.approx(computational) == analytical

@pytest.mark.analytical
def test_manual_volume():
    analytical = 64909.73
    computational = volume((50, 0),(100, 100), 20, 10)
    assert pytest.approx(computational) == analytical

@pytest.mark.dtype
def test_input_param_lower_inner():
    with pytest.raises(TypeError):
        o = ToroidalFieldCoilRectangleRoundCorners(
            lower_inner_coordinates= 1,
            mid_point_coordinates= (100,100),
            thickness= 20,
            distance= 10,
            number_of_coils= 1,
            )


@pytest.mark.dtype
def test_input_param_mid_point():
    with pytest.raises(TypeError):
        o = ToroidalFieldCoilRectangleRoundCorners(
            lower_inner_coordinates= (50,0),
            mid_point_coordinates= 1,
            thickness= 20,
            distance= 10,
            number_of_coils= 1,
            )


@pytest.mark.dtype
def test_input_param_thickness():
    with pytest.raises(TypeError):
        o = ToroidalFieldCoilRectangleRoundCorners(
            lower_inner_coordinates= (50,0),
            mid_point_coordinates= (100,100),
            thickness= "fail",
            distance= 10,
            number_of_coils= 1,
            )


@pytest.mark.dtype
def test_input_param_distance():
    with pytest.raises(TypeError):
        o = ToroidalFieldCoilRectangleRoundCorners(
            lower_inner_coordinates= (50,0),
            mid_point_coordinates= (100,100),
            thickness= 20,
            distance= "fail",
            number_of_coils= 1,
            )


@pytest.mark.dtype
def test_input_param_num_coil():
    with pytest.raises(TypeError):
        o = ToroidalFieldCoilRectangleRoundCorners(
            lower_inner_coordinates= (50,0),
            mid_point_coordinates= (100,100),
            thickness= 20,
            distance= 10,
            number_of_coils= 1.5,
            )
