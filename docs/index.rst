.. Toroidal Field Coil with Round Corners for Paramak documentation master file, created by
   sphinx-quickstart on Thu Jul  1 17:44:11 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Toroidal Field Coil with Round Corners for Paramak's documentation!
==============================================================================


ToroidalFieldCoilRectangleRoundCorners()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. cadquery::
   :select: cadquery_object
   :gridsize: 0

   import paramak
   import paramak_tfcoil_rectroundcorner as ptfc

   my_component = ptfc.ToroidalFieldCoilRectangleRoundCorners(
      lower_inner_coordinates= (50,0),
      mid_point_coordinates= (100,100),
      thickness= 20,
      distance= 20,
      number_of_coils= 9,
      rotation_angle=180,
   )

   cadquery_object = my_component.solid


.. automodule:: paramak_tfcoil_rectroundcorner.ToroidalFieldCoilRectangleRoundCorners
   :members:
   :show-inheritance:
