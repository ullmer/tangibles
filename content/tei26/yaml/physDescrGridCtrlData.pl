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

%%% end %%%

