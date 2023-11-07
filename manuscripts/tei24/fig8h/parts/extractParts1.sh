grep " _" *yaml|sed 's/^ - _//; s/_.*$//'|sort|uniq -c
