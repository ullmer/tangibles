cat *csv|sed 's/,,.*$//; s/[0-9],[TM][A-Z]*,[0-9],//' > S25abbrev.yaml
