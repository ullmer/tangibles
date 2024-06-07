package require tmg::canvsurface
package require tmg::piemenuobj 


CanvasSurfBase cv -rx 1280. -ry 1024.
cv init

CvPieBase p1 -canvsurface cv -numdivs 3
CvPieBase p2 -canvsurface cv -numdivs 5 -outerdiameter 9 \
  -incolor {blue} \
  -outcolorlist {aquamarine3 darkviolet aquamarine3 darkviolet aquamarine3}
CvPieBase p3 -canvsurface cv -numdivs 7 -outerdiameter 11

p1 constructPie
p2 constructPie
p3 constructPie

cv moveNObj ::p1 {5 5}
cv moveNObj ::p2 {8 8}
cv moveNObj ::p3 {12 12}

