% Prolog processing of enoContent files 
% Brygg Ullmer, Clemson University
% Begun 2023-12-10

%%% Return all contributions (both abbreviations and title) associated with a specific country %%%

contributionFromCountry(Abbrev, Title, Country) :-
  contribution(Abbrev, Title, Authors, _),
  authorsFromCountry(Authors, Country).

%%% See if any of authors from a specified country %%%

authorsFromCountry([AuthorHead|AuthorTail], Country) :-
  not(is_list(AuthorHead)), 
  authorFromCountry([AuthorHead|AuthorTail], Country).

authorsFromCountry([AuthorHead|AuthorTail], Country) :-
  is_list(AuthorHead), 
  (authorsFromCountry(AuthorHead, Country);
   authorsFromCountry(AuthorTail, Country)).

authorFromCountry([AuthorHead|AuthorTail], Country) :-
  not(is_list(Author)),
  last(AuthorTail, Country).

%%% end %%%
