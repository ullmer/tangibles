% Metadata
reed_dimensions(inch).

% Source references
reed_source(
    web("https://basketweaving.com/shopsite_sc/store/html/flat-reed.html"),
    country(us), state(ne)
).
reed_source(
    web("https://www.easttroybasketry.com/index.php?main_page=index&cPath=4_69"),
    country(us), state(ny)
).

% Reed width options
reed_width("11/64", 0.1718).
reed_width("3/16",  0.1875).
reed_width("1/4",   0.25).
reed_width("3/8",   0.375).
reed_width("1/2",   0.5).
reed_width("5/8",   0.625).
reed_width("3/4",   0.75).
reed_width("7/8",   0.875).
reed_width("1",     1.0).

% Fabrication constraints
reed_cut_constraint( range("0",   "1/4"), min_cut("1/16"), preferred_cut("3/32")).
reed_cut_constraint( range("3/8", "1/2"), min_cut("3/32"), preferred_cut("1/8")).
reed_cut_constraint( range("5/8", "1"),   min_cut("1/8"),  preferred_cut("5/32")).

%%% end %%%
