from _pytest.capture import TeeCaptureIO
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

@pytest.mark.length
def test_input_tuple2():
    with pytest.raises(ValueError):
        o = ptfc.ToroidalFieldCoilRectangleRoundCorners(
            lower_inner_coordinates= (50,0,5),
            mid_point_coordinates= (100,100),
            thickness= 20,
            distance= 10,
            number_of_coils= 1,
            )

@pytest.mark.length
def test_input_tuple2():
    with pytest.raises(ValueError):
        o = ptfc.ToroidalFieldCoilRectangleRoundCorners(
            lower_inner_coordinates= (50,0),
            mid_point_coordinates= (100,100,100),
            thickness= 20,
            distance= 10,
            number_of_coils= 1,
            )

@pytest.mark.value
def test_input_num_coils():
    with pytest.raises(TypeError):
        o = ptfc.ToroidalFieldCoilRectangleRoundCorners(
            lower_inner_coordinates= (50,0),
            mid_point_coordinates= (100,100),
            thickness= 20,
            distance= 10,
            number_of_coils= 1.5,
            )

@pytest.mark.value
def test_input_x_coordinates():
    with pytest.raises(ValueError):
        o = ptfc.ToroidalFieldCoilRectangleRoundCorners(
            lower_inner_coordinates= (50,0),
            mid_point_coordinates= (0,100),
            thickness= 20,
            distance= 10,
            number_of_coils= 1,
            )

@pytest.mark.value
def test_input_testboolean():
    with pytest.raises(TypeError):
        o = ptfc.ToroidalFieldCoilRectangleRoundCorners(
            lower_inner_coordinates= (50,0),
            mid_point_coordinates= (100,100),
            thickness= 20,
            distance= 10,
            number_of_coils= 1,
            test="not a boolean"
            )


@pytest.mark.value
def test_input_analyseboolean():
    with pytest.raises(TypeError):
        o = ptfc.ToroidalFieldCoilRectangleRoundCorners(
            lower_inner_coordinates= (50,0),
            mid_point_coordinates= (100,100),
            thickness= 20,
            distance= 10,
            number_of_coils= 1,
            analyse="not a boolean"
            )

