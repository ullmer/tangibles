
load ./visionPackage.so

set foo {}
set bar {{0 1 2 3 4 5 6 7 8 9}}
set zap [labelScene $foo $bar]
puts $zap
set zap [labelScene $foo $bar -autolabel]
puts $zap
set zap [labelScene $foo $bar frank]
puts $zap
set bar {{0 1 2 3 4 5 6 7 8 9} {0 1 2 3 4 5 6 7 8 9}}
set zap [labelScene $foo $bar frank -autolabel]
puts $zap

