% Reed descriptions toward interactive compositional fabrication
% Transcoded from YAML by CoPilot for Brygg Ullmer, with BAU evolutions
% 2025-07-16

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
reed_width("1/4",   0.2500).
reed_width("3/8",   0.3750).
reed_width("1/2",   0.5000).
reed_width("5/8",   0.6250).
reed_width("3/4",   0.7500).
reed_width("7/8",   0.8750).
reed_width("1",     1.0000).

% Fabrication constraints
reed_cut_constraint_frac( range("0",   "1/4"), min_cut("1/16"), preferred_cut("3/32")).
reed_cut_constraint_frac( range("3/8", "1/2"), min_cut("3/32"), preferred_cut("1/8")).
reed_cut_constraint_frac( range("5/8", "1"),   min_cut("1/8"),  preferred_cut("5/32")).

reed_cut_constraint_dec( range(0,     0.25), min_cut(0.0625), preferred_cut(0.0938)).
reed_cut_constraint_dec( range(0.375, 0.50), min_cut(0.0938), preferred_cut(0.1250)).
reed_cut_constraint_dec( range(0.675, 1.00), min_cut(0.1250), preferred_cut(0.1560)).

%%% end %%%
