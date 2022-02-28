lc=0.05;
//generationdurectangle
Point(1)={0,0,0,lc};
Point(2)={2,0,0,lc};
Point(3)={2,1,0,lc};
Point(4)={0,1,0,lc};
Line(1)={1,2};
Line(2)={2,3};
Line(3)={3,4};
Line(4)={4,1};
//generationdel’ellipse
Point(5)={1,0.5,0,lc};
Point(6)={1.5,0.5,0,lc};
Point(7)={1,0.75,0,lc};
Point(8)={0.5,0.5,0,lc};
Point(9)={1,0.25,0,lc};
Ellipse(5)={6,5,6,7};
Ellipse(6)={7,5,8,8};
Ellipse(7)={8,5,8,9};
Ellipse(8)={9,5,6,6};
//generationdescontours
Line Loop(1)={1,2,3,4};
Line Loop(2)={5,6,7,8};
//generationdelasurface
Plane Surface(1)={1,2};