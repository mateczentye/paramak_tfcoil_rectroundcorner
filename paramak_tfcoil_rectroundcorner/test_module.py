"""
The module contains testing functions for Paramak use. It calculates the 
"""
from paramak_tfcoil_rectroundcorner import ToroidalFieldCoilRectangleRoundCorners as tfc
from tf_coil_coordinator import find_points
from math import pi

def surface_area(lower_left,middle_right,thickness,extrusion_length,test=False,XZ_face_only=False,extrusion_area_only=False):
    """
    Function calculates the total surface area of the TF coil from the coordinates given in the find_points function
    """
    test_object = tfc(
        lower_inner_coordinates= lower_left,
        mid_point_coordinates= middle_right,
        thickness= thickness,
        distance= extrusion_length,
        number_of_coils= 1,
        )
        
    analyse_attributes = test_object.analyse_attributes
    #print(dir(tfc))
    print("analyse_attributes:",analyse_attributes)
    print(find_points(lower_left,middle_right,thickness,test=False,line_type=False,analyse=True))
    base, height, inner_rad, outter_rad = find_points(lower_left,middle_right,thickness,test=False,line_type=False,analyse=True)
    
    # The surface area of the face in XZ plane is divisible into 5 segments
    base_segment_area = thickness * (base - inner_rad)
    vertical_segment_area = thickness * (height - (inner_rad * 2))
    corner_area = (pi/4) * (outter_rad**2 - inner_rad**2)
    
    total_face_area = base_segment_area*2 + vertical_segment_area + corner_area*2

    # The surface area of the planes in YZ plane
    contour_length = inner_rad * (pi - 8) + pi * outter_rad + 2 * (2*base + thickness + height)
    extrusion_area = contour_length * extrusion_length
 
    total_bounding_surface = total_face_area*2 + extrusion_area
    
    ### pytest.approx() good to approximate values

    if test == True:
        print("Self testing:\nCalculated parameters:\nbase: {}\nheight: {}\ninner radius: {}\noutter radius: {}\nContour length: {}".format(base,height,inner_rad,outter_rad,contour_length))

    if XZ_face_only == True:
        if test == True:
            print("Face area = {} cm2".format(total_face_area))
        return total_face_area
    
    elif extrusion_area_only == True:
        if test == True:
            print("Extrusion area = {} cm2".format(extrusion_area))
        return extrusion_area

    else:
        if test == True:
            print("Total Surface area = {} cm2".format(total_bounding_surface))
        return total_bounding_surface


def volume(lower_left,middle_right,thickness,extrusion_length,test=False):
    """
    The function calculates the volume from the given coordinates used for parametarising the component in find_points function in core module
    it takes an additional variable for extrusion length which is the thickness of the coil
    """
    face_area = surface_area(lower_left,middle_right,thickness,extrusion_length,test=False,XZ_face_only=True)
    total_shape_volume = face_area * extrusion_length

    if test == True:
        print("Self testing:\nArea of the XZ plane face:\n", face_area)
        print("Total Shape Volume is:", total_shape_volume)

    return total_shape_volume

if __name__ == "__main__":
    print("Area testing:\n")
    surface_area((50,0), (100,100), 20, 10, test=True)
    print("\nVolume testing:\n")
    volume((50,0), (100,100), 20, 10, test=True)
    