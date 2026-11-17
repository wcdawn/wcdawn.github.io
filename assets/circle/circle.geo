// Run this with the following command line.
// gmsh circle.geo -save -format msh22

refinement=5;
h = 4.0*0.5^refinement;

radius = 10.0;

Point(1) = {0.0, 0.0, 0.0, h};     // Center
Point(2) = {radius, 0.0, 0.0, h};  // Right
Point(3) = {0.0, radius, 0.0, h};  // Top

Circle(1) = {2, 1, 3};
Line(2) = {3, 1};
Line(3) = {1, 2};

Curve Loop(1) = {1, 2, 3};

Plane Surface(1) = {1};
Physical Surface(1) = {1};

Mesh.ElementOrder = 2;
Mesh.HighOrderOptimize = 2;

Mesh 2;
