## Code for filtering HTML to produce an iconic web page representation

## Brygg Ullmer

## Begun 10/5/95
## Rewritten 11/8/95
## First functional for textual output 11/9/95

set CS_FILTER_HTML 1

############################ Parse tags #############################
# builds list of tags/text

proc parse_sgml {sgml} {

  set sgml [string trim $sgml] 
  regsub -all "\n" $sgml {} sgml
  set result {}

  ;# Drop case of all tags so we can correctly detect matched pairs

  set casgml "" ;# case-aligned sgml

  while {![regexp {^$} $sgml]} {
   
   if {[regexp {^<} $sgml]} { ;# drop case of continue text sequence 

     regsub {(^<[a-zA-Z0-9//]*)(.*)} $sgml {\1} tag
     regsub {(^<[a-zA-Z0-9//]*)(.*)} $sgml {\2} sgml

     append casgml [translit A-Z a-z $tag]

   } else {

     regsub {([^<]*)(.*)} $sgml {\1} notag
     regsub {([^<]*)(.*)} $sgml {\2} sgml

     append casgml $notag
   }
  }

  set sgml $casgml

  ;# Parse the first-level tags

  while {![regexp {^$} $sgml]} {
    set sgml [string trim $sgml] 

    if {[regexp {^</[^>]*>} $sgml]} { ;# we've got a close-tag
      ;# confusing/bogus; remove it

      regsub {^</[^>]*>} $sgml {} sgml
      continue
    }

    if {[regexp {^<!-[^>]*>} $sgml]} { ;# we've got a comment; ignore

      regsub {^<!-[^>]*>} $sgml {} sgml
      continue
    }

    if {[regexp {^<[a-zA-Z]+.*>} $sgml]} { ;# we've got a tag

      regsub {^<([^>]+)>(.*)} $sgml {\1} tag  ;#extract tag
      regsub {^<([^>]+)>(.*)} $sgml {\2} sgml ;# remove tag from sgml

      regsub {([^ ]+)[ ]*(.*)} $tag {\1} tag_head ;#extract tag head
      regsub {([^ ]+)[ ]*(.*)} $tag {\2} tag_text ;# and tail

      ;# look for end of tag
      set endtag [format "</%s>" $tag_head]
      set index  [string first $endtag $sgml]

      if {$index == -1} { ;# no tail found

	lappend result [list tag $tag_head $tag_text {}]
      } else { ;# strip out tagged text

	set tagged_text [string range $sgml 0 [expr $index - 1]]
	set sgml [string range $sgml $index end]

	;# clear end-of-tag
	;#set exclude_tail [format {%s[^>]*>} $endtag]
	set exclude_tail $endtag
	regsub $exclude_tail $sgml {} sgml

	lappend result [list tag $tag_head $tag_text $tagged_text]
      }
    } else { ;# strip out plaintext and continue

      if {[string first "<" $sgml] == -1 ||
	  [string first ">" $sgml] == -1} {;# no more tags

	  lappend result [list text $sgml]
	  return $result
      }

      ;# otherwise, return text up to first "<"

      set index [string first "<" $sgml]
      set text [string range $sgml 0 [expr $index - 1]]
      set sgml [string range $sgml $index end]

      lappend result [list text $text]
    }
  }

  return $result

}

########################## Xform_html ##############################

proc xform_html {html} {

  set processed_list {}

  set toklist [parse_sgml $html]

  foreach tok $toklist {

    set type [lindex $tok 0]

## Handle text

    if {[string match $type "text"]} {
      lappend processed_list [list text [string length [lindex $tok 1]]]
      continue
    }

    if {[string match $type "tag"]} {

      set tag [lindex $tok 1]

##### Handle single line-breaks

      if {[string match $tag "br"] ||
          [string match $tag "tr"] ||
          [string match $tag "hr"] ||
          [string match $tag "dd"] ||
          [string match $tag "li"]} {

	  lappend processed_list "nl"
	  continue
      }

##### Handle paragraphs

      if {[string match $tag "p"]} {

	lappend processed_list "nl" "nl"
	continue
      }

##### Handle img's 

      if {[string match $tag "img"]} {

	lappend processed_list "img"
	continue
      }

#### Handle h[1-n]'s, simply

     if {[string match $tag "ul"] ||
         [string match $tag "dl"] ||
         [string match $tag "li"]} {

       set processed_list [concat $processed_list \
	 [xform_html [lindex $tok 3]]]

       lappend processed_list "nl"
       continue
     }
       
#### Handle h[1-n]'s, simply

     if {[regexp {^h[0-3]} $tag]} {

       set processed_list [concat $processed_list \
	 [xform_html [lindex $tok 3]]]

       lappend processed_list "nl"
       continue
     }
       
##### Handle img's 

      if {[string match $tag "title"]} {

	lappend processed_list [list "title" [lindex $tok 3]]
	continue
      }


#### Handle h[1-n]'s, simply

     if {[string match $tag "a"]} {

       set hyperlist [concat {hyper} [xform_html [lindex $tok 3]]]

       lappend processed_list $hyperlist
       continue
     }

#### Handle body/html/center/head/font/etc. as transparent

     if {[string match $tag "body"] ||
	 [string match $tag "head"] ||
	 [string match $tag "center"] ||
	 [string match $tag "font"] ||
	 [string match $tag "i"] ||
	 [string match $tag "b"] ||
	 [string match $tag "pre"] ||
	 [string match $tag "html"]} {

       set processed_list [concat $processed_list \
	 [xform_html [lindex $tok 3]]]

       continue
     }

#### default case

       set processed_list [concat $processed_list \
	 [xform_html [lindex $tok 3]]]

       continue
   }
  }

## Make sure no more than two consec NL's exist

  set result {}
  set nlcount 0

  foreach tag $processed_list {

    if {[string match $tag "nl"]} {
      incr nlcount
      if {$nlcount > 2} {continue}
    } else {
      set nlcount 0
    }

    lappend result $tag
  }

  return $result
}

####################### Load HTML ####################

proc load_html {url} {

#assumes url is of form service://host/path; 

  regsub {^([a-zA-Z]+)://([^/]+)(.*)$} $url {\1} protocol
  regsub {^([a-zA-Z]+)://([^/]+)(.*)$} $url {\2} host
  regsub {^([a-zA-Z]+)://([^/]+)(.*)$} $url {\3} path

  set port 80 ;#default

  if {[regexp {:} $host]} {  ;# Manual define of port number

    regsub {^.*:([0-9]+).*$} $host {\1} port
    regsub {^([^:]+):.*$}    $host {\1} host
  } else {

    switch -glob $protocol {

      http   {set port 80}
      gopher {set port 70}
    }
  }

### Connect

  puts "Connecting to host $host, port $port"

  set handle [server_connect -buf $host $port]
  

  switch -glob $protocol {

    http   {server_send $handle "GET $path"}
    gopher {regsub {^/} $path {} path; server_send $handle $path}
  }

  set result ""

  while {![eof $handle]} { append result [gets $handle] "\n"}

  close $handle

  return $result
}

######################### Rationalize WebToks ###########################
# Straightens out results of xform_html

proc rationalize_webtoks {webtoks} {

## First pass -- expand hyper's

  set firstpass {}

  foreach tok $webtoks {

    if {[string match [lindex $tok 0] "hyper"]} {
      
      set tok [lreplace $tok 0 0] ;# remove hyper element
      foreach subtok $tok {
	set el [lreplace $subtok 0 0 \
	  [format {hyper-%s} [lindex $subtok 0]]]
	lappend firstpass $el
      }
    } else {
      lappend firstpass $tok
    }
  }

## Second pass -- aggregate same-type neighbors

  set result {}
  set lastel {}
  set lasttype {}

  foreach tok $firstpass {
    set thistype [lindex $tok 0]

    if {[regexp {text} $lasttype] &&
	[regexp {text} $thistype] &&
	[string match $lasttype $thistype]} { ;# aggregate-em

      set lastel [lreplace $lastel 1 1 \
	[expr ([lindex $lastel 1] + [lindex $tok 1])]]
    } else {
      lappend result $lastel
      set lastel $tok
      set lasttype $thistype
    }
  }

  set result [lreplace $result 0 0] ;# delete starter {}
  return $result
}

######################## Get Webtoks #######################

proc open_webtokdb {{dbpath "/vlw/data/ullmer/webtoks.db"} {attrib "rwc"}} {

  global GLwebtokdb

  if {[info exists GLwebtokdb]} {
   close_webtokdb
  }

  set GLwebtokdb [gdbm open $dbpath $attrib]
}

proc close_webtokdb {} {

  global GLwebtokdb

  if {[info exists GLwebtokdb]} {

    gdbm close $GLwebtokdb
    unset GLwebtokdb
  }
}

proc get_webtok {url} {

  global GLwebtokdb

  if {![info exists GLwebtokdb]} {
    puts "get_webtok error: webtokdb not yet opened!  Using default open"
    open_webtokdb
  }
 
  if {[gdbm exists $GLwebtokdb $url]} {

    return [gdbm fetch $GLwebtokdb $url]
  }
 
  puts "Retrieving <$url>..."
  set html    [load_html $url]
  set toklist [xform_html $html]
  set toklist [rationalize_webtoks $toklist]
  gdbm store $GLwebtokdb $url $toklist
  puts "Retrieved and cached."

  return $toklist
}
