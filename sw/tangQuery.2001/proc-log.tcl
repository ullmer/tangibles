#! proc log

#search for experiment num

 set experiment {}
 while {![eof stdin] && $experiment == {}} {
   set inline [gets stdin]
   if {[regexp {experiment set} $inline]} {
     set experiment [lindex $inline 3]
     puts "experiment: $experiment"
   }
 }

#search for beginning of experiment
 set firstTime {}
 while {![eof stdin] && $firstTime == {}} {
   set inline [gets stdin]
   if {[regexp {begin} $inline]} {
     set firstTime [lindex $inline 0]
   }
 }

 set lastTime $firstTime

 set count 0
 set expComplete 0

#search for beginning of experiment
 while {![eof stdin] && $expComplete == 0} {
   set inline [gets stdin]
   if {[regexp {end} $inline]} {
     set expComplete 1
   }

   if {[regexp {end} $inline] || [regexp {complete} $inline]} {
     set currentTime [lindex $inline 0]

     incr count
     set diff [expr $currentTime - $firstTime]
     set diff2 [expr $currentTime - $lastTime]
     puts "$count $diff $diff2"
     set lastTime $currentTime
   }
 }

#219     experiment set: 2
#31250   begin
#46375   complete; next 1
#66031   complete; next 2
#89344   complete; next 3
#105500  complete; next -1
#105656  end

### END ###

