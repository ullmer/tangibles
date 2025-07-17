% MIDI Grid Controller Descriptions
% Transcoded from YAML by CoPilot for Brygg Ullmer, with BAU evolutions
% 2025-07-16

% Controller: Novation Launchpad X
grid_controller(novation_launchpad_x, notes("Square pads, RGB, velocity-sensitive"),
    dims_mm(241, 241, 17), grid(8, 8), pad_pitch_mm(30, 30), pad_size_mm(24, 24)).

% Controller: Novation Launchpad Mini
grid_controller(novation_launchpad_mini, notes("Compact form, square pads, RGB"),
    dims_mm(180, 180, 14), grid(8, 8), pad_pitch_mm(27, 27), pad_size_mm(20, 20)).

% Controller: Akai APC Mini Mk2
grid_controller(akai_apc_mini_mk2, notes("Rectangular pads, RGB, includes faders"),
    dims_mm(232, 172, 32), grid(8, 8), pad_pitch_mm(26, 21), pad_size_mm(21, 15)).

% Controller: Adafruit NeoTrellis
grid_controller(adafruit_neotrellis, notes("Tileable 4x4 grid, RGB NeoPixels, I2C, elastomer pad opt"),
    dims_mm( 60,  60,  7), grid(4, 4), pad_pitch_mm(15, 15), pad_size_mm(12, 12)).

%%% transformational predicates (copilot impl, per naming and functionality requested by BAU)

% Distance between pads in X and Y directions
% Example: grid_pad_dist_between_pads(adafruit_neotrellis, mm, 3, 3).
grid_pad_dist_between_pads(Controller, Unit, GapX, GapY) :-
    pad_spacing(Controller, Unit, GapX, GapY).

% Optional offset from center
% Example: grid_pad_center_offset(adafruit_neotrellis, mm, 1.5, 1.5).
grid_pad_center_offset(Controller, Unit, OffsetX, OffsetY) :-
    pad_offset(Controller, Unit, OffsetX, OffsetY).

% Margins around the grid
% If offset exists, margins are asymmetric and centered is false
% If no offset, margins are symmetric and centered is true
grid_pad_dist_margins(Controller, Unit, margin(Left, Right, top_bottom(Top, Bottom)), false) :-
    grid_pad_center_offset(Controller, Unit, OffsetX, OffsetY),
    pad_spacing(Controller, Unit, GapX, GapY),
    Left is OffsetX,
    Right is GapX - OffsetX,
    Top is OffsetY,
    Bottom is GapY - OffsetY.

grid_pad_dist_margins(Controller, Unit, margin(Horiz, Vert, both), true) :-
    \+ grid_pad_center_offset(Controller, Unit, _, _),
    pad_spacing(Controller, Unit, GapX, GapY),
    Horiz is GapX / 2,
    Vert is GapY / 2.

% Conversion factor
mm_to_in(25.4).

% Extract pad spacing from grid_controller facts
pad_spacing(Controller, mm, GapX, GapY) :-
    grid_controller(Controller, _, _, _, pad_pitch_mm(GapX, GapY), _).

% Convert pad spacing to inches
pad_spacing(Controller, in, GapX_in, GapY_in) :-
    pad_spacing(Controller, mm, GapX_mm, GapY_mm),
    mm_to_in(Factor),
    GapX_in is GapX_mm / Factor,
    GapY_in is GapY_mm / Factor.

% Extract dimensions in mm
dims(Controller, mm, W, H, D) :-
    grid_controller(Controller, _, dims_mm(W, H, D), _, _, _).

% Convert dimensions to inches
dims(Controller, in, W_in, H_in, D_in) :-
    dims(Controller, mm, W_mm, H_mm, D_mm),
    mm_to_in(Factor),
    W_in is W_mm / Factor,
    H_in is H_mm / Factor,
    D_in is D_mm / Factor.

%%% end %%%

