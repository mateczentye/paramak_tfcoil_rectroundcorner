import pytest
pytest.importorskip('paramak')
import paramak_tfcoil_rectroundcorner as ptfc


obj = ptfc.ToroidalFieldCoilRectangleRoundCorners(
    lower_inner_coordinates= (50,0),
    mid_point_coordinates= (100,100),
    thickness= 20,
    distance= 10,
    number_of_coils= 1,
    )

@pytest.mark.parametric
def test_surface_area():
    paramak_area = obj.area
    print(paramak_area)
    package_area = ptfc.surface_area((50, 0),(100, 100), 20, 10)
    assert pytest.approx(package_area) == paramak_area

@pytest.mark.parametric
def test_volume():
    paramak_vol = obj.volume
    package_vol = ptfc.volume((50, 0),(100, 100), 20, 10)
    assert pytest.approx(package_vol) == paramak_vol

@pytest.mark.analytical
def test_manual_area():
    analytical = 19872.92
    computational = ptfc.surface_area((50, 0),(100, 100), 20, 10)
    assert pytest.approx(computational) == analytical

@pytest.mark.analytical
def test_manual_volume():
    analytical = 64909.73
    computational = ptfc.volume((50, 0),(100, 100), 20, 10)
    assert pytest.approx(computational) == analytical

@pytest.mark.dtype
def test_input_param_lower_inner():
    with pytest.raises(TypeError):
        o = ptfc.ToroidalFieldCoilRectangleRoundCorners(
            lower_inner_coordinates= 1,
            mid_point_coordinates= (100,100),
            thickness= 20,
            distance= 10,
            number_of_coils= 1,
            )


@pytest.mark.dtype
def test_input_param_mid_point():
    with pytest.raises(TypeError):
        o = ptfc.ToroidalFieldCoilRectangleRoundCorners(
            lower_inner_coordinates= (50,0),
            mid_point_coordinates= 1,
            thickness= 20,
            distance= 10,
            number_of_coils= 1,
            )


@pytest.mark.dtype
def test_input_param_thickness():
    with pytest.raises(TypeError):
        o = ptfc.ToroidalFieldCoilRectangleRoundCorners(
            lower_inner_coordinates= (50,0),
            mid_point_coordinates= (100,100),
            thickness= "fail",
            distance= 10,
            number_of_coils= 1,
            )


@pytest.mark.dtype
def test_input_param_distance():
    with pytest.raises(TypeError):
        o = ptfc.ToroidalFieldCoilRectangleRoundCorners(
            lower_inner_coordinates= (50,0),
            mid_point_coordinates= (100,100),
            thickness= 20,
            distance= "fail",
            number_of_coils= 1,
            )


@pytest.mark.dtype
def test_input_param_num_coil():
    with pytest.raises(TypeError):
        o = ptfc.ToroidalFieldCoilRectangleRoundCorners(
            lower_inner_coordinates= (50,0),
            mid_point_coordinates= (100,100),
            thickness= 20,
            distance= 10,
            number_of_coils= 1.5,
            )