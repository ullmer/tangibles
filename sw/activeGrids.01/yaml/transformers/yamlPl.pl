%%% yaml to prolog transformer 
% by brygg ullmer (clemson) and copilot
% begun 2026-03-24

:- use_module(library(yaml)).

:- op(950, xfx, :=).

%%%%%%%% load_yaml(+File, -Data) %%%%%%%% 
load_yaml(File, Data) :-
    yaml_read(File, Data, [canonical(false)]).

%%%%%%%% extract_theme_abbrevs(+YAML, -Pairs) %%%%%%%% 
%% Produces pairs CategoryKey-[ThemeKeys...]

extract_theme_abbrevs(YAML, Pairs) :-
    Categories = YAML.categories,
    findall(Key-Themes,
        (   get_dict(Key, Categories, CatObj),
            get_dict(themes, CatObj, ThemeDict),
            dict_keys(ThemeDict, Themes)
        ),
        Pairs).

%%%%%%%% print_prolog_dsl(+Pairs) %%%%%%%% 
%% Emits lines like:
%%   themeAbbrev(civGovern) := [gov, civ, colAc, infr].

print_prolog_dsl([]).
print_prolog_dsl([Key-Themes | Rest]) :-
    format('themeAbbrev(~w) := ~w.~n', [Key, Themes]),
    print_prolog_dsl(Rest).

%%%%%%%% top-level convenience %%%%%%%% 
yaml_to_prolog_dsl(File) :-
    load_yaml(File, YAML),
    extract_theme_abbrevs(YAML, Pairs),
    print_prolog_dsl(Pairs).

%%% end %%%
