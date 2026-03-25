%%% expressions of people and themes %%%
% brygg ullmer (clemson) & copilot
% begun 2026-03-24

:- op(950, xfx, :=). % helper to support more compact & human-legible mappings

themeAbbrev(natuSust)  := [eco, env, consrv, sust, agr].
themeAbbrev(cultIdent) := [culPlr, xcultu, indig, intl].
themeAbbrev(exprCreat) := [drama, mus, perf].
themeAbbrev(civGovern) := [gov, civ, colAc, infr].
themeAbbrev(ethMoral)  := [eth, moral, humRi, relTol].
themeAbbrev(knowLearn) := [edu, phil].

personAbbrev(gottholdEphraimLessing, gel).
personDomains(gottholdEphraimLessing) := [drama, enlightenmentEthics, religiousTolerance].
personThemes(gottholdEphraimLessing)  := [ethMoral, knowLearn, exprCreat].

personAbbrev(johannGottfriedHerder, jgh).
personDomains(johannGottfriedHerder) := [philosophy, culturalPluralism].
personThemes(johannGottfriedHerder)  := [cultIdent, knowLearn].

personAbbrev(johnMuir, jm).
personDomains(johnMuir) := [environment, wildernessPhilosophy].
personThemes(johnMuir)  := [natuSust, ethMoral].

personAbbrev(georgeWashingtonCarver, gwc).
personDomains(georgeWashingtonCarver) := [agriculture, sustainability, education].
personThemes(georgeWashingtonCarver)  := [natuSust, knowLearn, civGovern].

personAbbrev(theodoreRoosevelt, tr).
personDomains(theodoreRoosevelt) := [governance, conservationPolicy].
personThemes(theodoreRoosevelt)  := [civGovern, natuSust].

personAbbrev(franklinD.Roosevelt, fdr).
personDomains(franklinD.Roosevelt) := [governance, infrastructure, collectiveAction].
personThemes(franklinD.Roosevelt)  := [civGovern, ethMoral].

personAbbrev(eleanorRoosevelt, er).
personDomains(eleanorRoosevelt) := [humanRights, ethics, internationalFrameworks].
personThemes(eleanorRoosevelt)  := [ethMoral, cultIdent, civGovern].

personAbbrev(robertFrost, rf).
personDomains(robertFrost) := [poetry, moralReflection].
personThemes(robertFrost)  := [exprCreat, ethMoral].

personAbbrev(joyHarjo, jh).
personDomains(joyHarjo) := [poetry, indigenousKnowledge, music].
personThemes(joyHarjo)  := [cultIdent, exprCreat, natuSust].

personAbbrev(amandaGorman, ag).
personDomains(amandaGorman) := [poetry, performance, civicImagination].
personThemes(amandaGorman)  := [exprCreat, civGovern, ethMoral].

personAbbrev(lizeliaAugustaJenkinsMoorer, lajm).
personDomains(lizeliaAugustaJenkinsMoorer) := [poetry, education, civicAdvocacy].
personThemes(lizeliaAugustaJenkinsMoorer)  := [ethMoral, civGovern, knowLearn].

personAbbrev(arthurSze, as).
personDomains(arthurSze) := [poetry, ecology, crossCulturalImagination].
personThemes(arthurSze)  := [natuSust, cultIdent, exprCreat, knowLearn].

%%% end %%%
