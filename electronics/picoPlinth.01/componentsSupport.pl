% rpi_pico1.pl — minimal, YAML-aligned pin/function map
% Source: official Pico pinout, cross-checked with Pinout.xyz.
% (SPI/I2C/UART alternates only; no CTS/RTS/PWM/PIO in this minimal set.)
% Prolog expansions of YAML file by CoPilot
% Brygg Ullmer and CoPilot, Clemson University
% Begun 2026-03-07 

% -------- Convenience predicates --------

% true if Pin supplies Capability (exact term match).
pin_supports(Component, Pin, Capability) :-
    pin(Component, Pin, Caps),
    member(Capability, Caps).

% list all physical pins that match a Capability, e.g., pins_with(i2c(1,sda), Pins).
pins_with(Component, Capability, Pins) :-
    findall(P, pin_supports(Component, P, Capability), PList),
    sort(PList, Pins).

% collect pins that offer any role on a given SPI or I2C controller
% (e.g., pins_for_spi(0, Pins).)
pins_for_spi(Component, Ctrl, Pins) :-
    findall(P, (pin(Component, P, Caps), member(spi(Ctrl, _), Caps)), PList),
    sort(PList, Pins).

pins_for_i2c(Component, Ctrl, Pins) :-
    findall(P, (pin(Component, P, Caps), member(i2c(Ctrl, _), Caps)), PList),
    sort(PList, Pins).

% lightweight name lookup helpers
is_ground(Component, Pin)   :- pin(Component, Pin, Caps), member(gnd, Caps).
is_analog(Component, Pin)   :- pin(Component, Pin, Caps), (member(adc(_), Caps); member(adc_vref, Caps); member(agnd, Caps)).

% Deterministic yes/no test when Pin is (usually) ground

% Enumerates on backtracking (use this as your main is_power/2)
is_power(Component, Pin) :-
    power_pins(Component, L),
    member(Pin, L).

% Deterministic yes/no test when Pin is (usually) ground
is_power_chk(Component, Pin) :-
    power_pins(Component, L),
    memberchk(Pin, L).

%% ---- Alias maps to canonical roles ----
%% Canonical atoms we’ll use: spi_cs, spi_sck, spi_mosi, spi_miso, rst, irq, v3v3, gnd

role_alias(spi_cs,   sda).
role_alias(spi_cs,   ss).
role_alias(spi_cs,   cs).
role_alias(spi_cs,   csn).
role_alias(spi_cs,   nss).

role_alias(spi_sck,  sck).
role_alias(spi_sck,  sclk).
role_alias(spi_sck,  clk).

role_alias(spi_mosi, mosi).
role_alias(spi_mosi, copi).
role_alias(spi_mosi, sdi).
role_alias(spi_mosi, di).
role_alias(spi_mosi, din).

role_alias(spi_miso, miso).
role_alias(spi_miso, cipo).
role_alias(spi_miso, sdo).
role_alias(spi_miso, do).
role_alias(spi_miso, dout).

role_alias(rst,      rst).
role_alias(rst,      reset).
role_alias(rst,      rst_n).
role_alias(rst,      nreset).

role_alias(irq,      irq).
role_alias(irq,      int).

role_alias(v3v3,     '3v3').
role_alias(v3v3,     '3.3v').
role_alias(v3v3,     vcc).
role_alias(v3v3,     vdd).

role_alias(gnd,      gnd).
role_alias(gnd,      ground).

%% Resolve a possibly-aliased label into a canonical role
canonical_role(Label, Canon) :-
    (   role_alias(Canon, Label)
    ->  true
    ;   Canon = Label     % if already canonical or unrecognized, leave as-is
    ).

%% true if Caps contains something that matches CanonRole via aliasing
caps_has_role(Caps, CanonRole) :-
    member(Lab, Caps),
    canonical_role(Lab, CanonRole0),
    CanonRole0 == CanonRole.

%% has_role(Component, Pin, CanonRole, Caps) unifies if pin supports a role (with alias resolution)
has_role(Component, Pin, CanonRole, CapsOut) :-
    pin(Component, Pin, Caps),
    canonical_role(CanonRole, CanonRole), % ensure CanonRole is canonical atom we use
    caps_has_role(Caps, CanonRole),
    CapsOut = Caps.

%%% end %%%
