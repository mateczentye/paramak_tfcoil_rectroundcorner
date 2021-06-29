from typing import Optional, Tuple, Union
from _pytest.python_api import raises
from numpy.lib.function_base import angle
from paramak.parametric_shapes.extruded_mixed_shape import ExtrudeMixedShape
import numpy as np

class ToroidalFieldCoilRectangleRoundCorners(ExtrudeMixedShape):
    """
    Creates geometry for TF coil with rounded corners.
    Finds the coordinates for verteces of a TF coil, in a 2D profile on the XZ plane using
    the main function find_points() which takes 3 positional arguments for the TF coil parameters,
    and takes three additional boolean arguments.

    Arguments:
        lower_inner_coordinates (Tuple): the (X,Z) coordinate of the inner
        corner of the lower end of the coil (cm)

        mid_point_coordinates (Tuple): the (X,Z) coordinate of the mid 
        point of the vertical section (cm)

        thickness: The thickness in the (X,Z) plane of the toroidal
        field coils (cm)

        extrusion_distance: The total extruded thickness of the coils
        when in the y-direction (centered extrusion)

        coil_count: The number of coils placed in the model
        (changing azimuth_placement_angle by dividing 360 by
        the amount given) Defaults to 1

        inner_coil: Boolean to include the inside of the Coils

        file_name_stp: Defults to "ToroidalFieldCoilRectangleRoundCorners.stp"

        file_name_stl: Defaults to "ToroidalFieldCoilRectangleRoundCorners.stl"

        material_tag: Defaults to "outter_tf_coil_mat"

        test: True prints to console the list of points
        
        line_type: Sets the returned list to be populated by elements for MixedShape()
        Defaults to True

        analyse: Defaults to False; if True returns values that are calculated for the 2D Shape

    """

    def __init__(
        self,
        lower_inner_coordinates: Tuple[float,float],
        mid_point_coordinates: Tuple[float,float],
        thickness: Union[float,int],
        distance: float,
        number_of_coils: int,
        inner_coil: Optional[bool] = True,
        stp_filename: Optional[str] = "ToroidalFieldCoilRectangleRoundCorners.stp",
        stl_filename: Optional[str] = "ToroidalFieldCoilRectangleRoundCorners.stl",
        material_tag: Optional[str] = "outter_tf_coil_mat",
        test: Optional[bool] = False,
        analyse: Optional[bool] = False,
        **kwargs
        ) -> None:
        
        super().__init__(
            distance=distance,
            stp_filename=stp_filename,
            stl_filename=stl_filename,
            material_tag=material_tag,
            **kwargs
            )

        self.lower_inner_coordinates = lower_inner_coordinates[0], lower_inner_coordinates[1]
        self.mid_point_coordinates = mid_point_coordinates[0], mid_point_coordinates[1]
        self.thickness = thickness,
        self.number_of_coils = number_of_coils,
        self.inner_coil = inner_coil,
        self.test = test
        self.analyse = analyse
        self.analyse_attributes = [
            0,
            0,
            0,
            0
        ]


        ### Check if input values are what they meant to be ###
        if type(self.lower_inner_coordinates) != tuple or type(self.mid_point_coordinates) != tuple:
            raise TypeError("Invalid input - Coordinates must be a tuple")

        elif type(self.thickness) == float or type(self.thickness) == int:
            raise TypeError("Invalid input - Thickness must be a number")
            
        elif len(self.lower_inner_coordinates) != 2 or len(self.mid_point_coordinates) != 2:
            raise ValueError("The input tuples are too long or too short, they must be 2 element long")

        elif self.lower_inner_coordinates[0] > self.mid_point_coordinates[0]:
            raise ValueError("The middle point's x-coordinate must be larger than the lower inner point's x-coordinate")
        else:
            ### Adding hidden attributes for analyse list population
            
            # inner base length of the coil
            self._base_length = mid_point_coordinates[0] - lower_inner_coordinates[0]
            self.analyse_attributes[0] = self._base_length
            # height of the coil
            self._height = abs(mid_point_coordinates[1] - lower_inner_coordinates[1])*2
            self.analyse_attributes[1] = self._height
            
            """ Inner and outter radius of curvature for the corners
            The inner curvature is scales as a function of the base length 
            of the coil and its thickness as long as the thickness does not exceed the base length
            if the thickness/base length ratio is larger or equal to 1
            it takes 10% of the thickness as the inner curve radius 
            this to avoid having coordinates before the previous or at the same spot as Paramak 
            cannot compute it"""
            
            if thickness/self._base_length >= 1:
                self._inner_curve_radius = thickness*0.1
                self._outter_curve_radius = thickness*1.1
                self.analyse_attributes[2] = self._inner_curve_radius
                self.analyse_attributes[3] = self._outter_curve_radius
            else:
                self._outter_curve_radius = (1 + (thickness/self._base_length))*thickness
                self._inner_curve_radius = (thickness**2) / self._base_length
                self.analyse_attributes[2] = self._inner_curve_radius
                self.analyse_attributes[3] = self._outter_curve_radius
                

    @property
    def azimuth_placement_angle(self):
        self.find_azimuth_placement_angle()
        return self._azimuth_placement_angle
    
    @azimuth_placement_angle.setter
    def azimuth_placement_angle(self, val):
        self._azimuth_placement_angle = val

    def find_points(self):
        """
        lower_inner_coordinates must be a 2 element tuple
        mid_point_coordinates must be a 2 elemenet tuple
        thickness must be a float or an int
        test=True will print the returned coordinates to console
        line_type=True will return a 3 element tuple with line types for mixed shape paramak functions
        analyse=True will return values for volumetric and surface analysis for 3D parametric shape 
        """

        lower_x, lower_z = self.lower_inner_coordinates
        mid_x, mid_z = self.mid_point_coordinates

        ### redifine values to be floats to make it look consistent 
        lower_x,lower_z, mid_x, mid_z, thickness = float(lower_x),float(lower_z), float(mid_x),float(mid_z), float(self.thickness[0])

        ### Define differences to avoid miss claculation due to signs
        base_length = self.analyse_attributes[0]
        height = self.analyse_attributes[1]
        
        ### 10 points/tuples are returned from the initial 2 coordinates and thickness value
        p1 = (lower_x,lower_z)
        p2 = (p1[0]+base_length,p1[1])
        p3 = (p2[0],p2[1]+height)
        p4 = (p1[0],p1[1]+height)
        p5 = (p4[0],p4[1]+thickness)
        p6 = (p3[0],p4[1]+thickness)
        p7 = (p3[0]+thickness,p3[1])
        p8 = (p2[0]+thickness,p2[1])
        p9 = (p2[0],p2[1]-thickness)
        p10 = (lower_x,lower_z-thickness)
        
        inner_curve_radius = self.analyse_attributes[2]
        outter_curve_radius = self.analyse_attributes[3]

        ### New subroutines to calculate inner and outter curve mid-points, x and y displacement from existing points
        # long shift does a sin(45)*radius of curvature amount of shift
        # short shift does a (1-sin(45))*radius of curvature amount of shift
        def shift_long(radius):
            """radius is the radius of curvature"""
            return (2**0.5)*0.5*radius
            
        def shift_short(radius):
            """radius is the radius of curvature"""
            return (2-(2**0.5))*0.5*radius

        p11 = (p2[0]-inner_curve_radius, p2[1])
        p12 = (p11[0]+shift_long(inner_curve_radius),p11[1]+shift_short(inner_curve_radius))
        p13 = (p2[0],p2[1]+inner_curve_radius)
        p14 = (p3[0],p3[1]-inner_curve_radius)
        p15 = (p14[0]-shift_short(inner_curve_radius),p14[1]+shift_long(inner_curve_radius))
        p16 = (p3[0]-inner_curve_radius, p3[1])
        p17 = (p6[0]-inner_curve_radius, p6[1])
        p18 = (p17[0]+shift_long(outter_curve_radius), p17[1]-shift_short(outter_curve_radius))
        p19 = (p14[0]+thickness,p14[1])
        p20 = (p8[0],p8[1]+inner_curve_radius)
        p21 = (p18[0], p20[1]-shift_long(outter_curve_radius))
        p22 = (p11[0], p11[1]-thickness)

        ### List holding the points that are being returned by the function
        points = [p1,p11,p12,p13,p14,p15,p16,p4,p5,p17,p18,p19,p20,p21,p22,p10]
        tri_points = []
        lines = ["straight"] + ['circle']*2 + ['straight'] + ['circle']*2 + ['straight']*3 + ['circle']*2 + ['straight'] + ['circle']*2 + ['straight']*2

        for i in range(len(points)):
            tri_points.append(points[i] + (lines[i],))

        self.points = tri_points
        """
        for att in [base_length,height,inner_curve_radius,outter_curve_radius]:
            if att not in self.analyse_attributes:
                self.analyse_attributes.append(att) 
        """
        if self.test == True:
            print(tri_points)

        if self.analyse == True:
            print(self.analyse_attributes)


                    
    def find_azimuth_placement_angle(self):
        """ Finds the placement angles from the number of coils given in a 360 degree """
        angles = list(np.linspace(0, 360, self.number_of_coils[0], endpoint = False))        
        self.azimuth_placement_angle = angles

    def get_analyse_attributes(self):
        print("Attributes for Analysis:\n",self.analyse_attributes)
        return self.analyse_attributes

if __name__== "__main__":
        
    obj = ToroidalFieldCoilRectangleRoundCorners(
        lower_inner_coordinates= (50,0),
        mid_point_coordinates= (100,100),
        thickness= 20,
        distance= 20,
        number_of_coils= 10,
        rotation_angle=180,
        test=True,
        analyse=True
        )
    obj.show()
    print(obj.get_analyse_attributes())