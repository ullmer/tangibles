themeAbbrev(civGovern)        := [gov, civ, colAc, infr].
themeAbbrev(civicsGovernance) := [governance, civics, collectiveAction, infrastructure].

:- op(950, xfx, :=).

themeAbbrev(K, X) :- K := L, member(X, L).

