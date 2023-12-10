% Prolog processing of enoContent files 
% Brygg Ullmer, Clemson University
% Begun 2023-12-10

%%% Return all contributions (both abbreviations and title) associated with a specific country, continent, or keyword

contributionFromCountry(Abbrev, Title, Country) :-
  contribution(Abbrev, Title, Authors, _),
  authorsFromCountry(Authors, Country).

contributionFromContinentAbbrev(Abbrev, Title, ContinentAbbrev) :-
  contribution(Abbrev, Title, Authors, _),
  authorsFromCountry(Authors, Country),
  continent(_,_,ContinentAbbrev,CountryList),
  member(Country, CountryList).

contributionWithKeyword(Abbrev, Title, Keyword) :-
  contribution(Abbrev, Title, _, Keywords),
  member(Keyword, Keywords).

%%% Determine if any of authors from a specified country %%%

authorsFromCountry([AuthorHead|AuthorTail], Country) :-
  not(is_list(AuthorHead)), 
  authorFromCountry([AuthorHead|AuthorTail], Country).

authorsFromCountry([AuthorHead|AuthorTail], Country) :-
  is_list(AuthorHead), 
  (authorsFromCountry(AuthorHead, Country);
   authorsFromCountry(AuthorTail, Country)), !.  %avoids N matches when N authors from same country

authorFromCountry([AuthorHead|AuthorTail], Country) :-
  not(is_list(AuthorHead)),
  last(AuthorTail, Country).

%%% end %%%
