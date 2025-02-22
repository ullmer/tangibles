select * from titles as t, authors as a, ti_au as ta where a.lastn in ('Laney', 'Dewan') and 
                        ta.ti_id = t.id and ta.au_id = a.id;

select * from keywords as k, ti_kw as tk, titles as t where tk.kw_id = k.id and tk.ti_id = t.id and t.id in (637, 638);

select * from titles as t, keywords as k, ti_kw as tk, ti_au as ta, authors as a where a.lastn in ('Laney', 'Dewan') and
   ta.ti_id = t.id and ta.au_id = a.id and tk.ti_id = t.id and tk.kw_id = k.id;

select k.keyword from titles as t, keywords as k, ti_kw as tk, ti_au as ta, authors as a where a.lastn in ('Laney', 'Dewan') and
   ta.ti_id = t.id and ta.au_id = a.id and tk.ti_id = t.id and tk.kw_id = k.id group by keyword;

select t.id from titles as t, authors as a, ti_au as ta where a.lastn in ('Laney', 'Dewan') and 
                        ta.ti_id = t.id and ta.au_id = a.id group by t.id;

select id, lastn, firstn from authors where lastn in
   ('Desmond', 'Ashktorab', 'Pan', 'Johnson', 'Dugan', 'Cooper') order by lastn, firstn;

select id, lastn, firstn from authors where lastn in
   ('Simic', 'Singh', 'Partl', 'Veas', 'Sabol') order by lastn, firstn;

select id, lastn, firstn from authors where lastn in
   ('Wang', 'Ivrissimtzis', 'Li', 'Shi') order by lastn, firstn;
  
select id, lastn, firstn from authors where lastn in
   ('Gupta', 'Chen', 'Tsai') order by lastn, firstn;

select id, lastn, firstn from authors where lastn in
   ('Delic', 'Emamgholizadeh', 'Nguyen', 'Ricci') 
   order by lastn, firstn;

select id, lastn, firstn from authors where lastn in
   ('Aly', 'Byrne', 'Knijnenburg')
   order by lastn, firstn;

select t.id from titles as t, authors as a, ti_au as ta where 
  t.id in (1209, 1207, 908, 1224, 4827) 
  and ta.ti_id = t.id and ta.au_id=a.id group by t.id;

select t.id from titles as t, authors as a, ti_au as ta where 
  a.id in (1209, 1207, 908, 1224, 4827) 
  and ta.ti_id = t.id and ta.au_id=a.id group by t.id;


select k.id, k.keyword from titles as t, keywords as k, ti_kw as tk, ti_au as ta, authors as a where 
  t.id in (1209, 1207, 908, 1224, 4827) 
   and ta.ti_id = t.id and ta.au_id = a.id and tk.ti_id = t.id and tk.kw_id = k.id group by keyword;

select t.id from titles as t, authors as a, ti_au as ta where 
  a.id in (1623, 1117, 2155, 2654)
  and ta.ti_id = t.id and ta.au_id=a.id group by t.id;

select k.id, k.keyword from titles as t, keywords as k, ti_kw as tk, ti_au as ta, authors as a where 
  t.id in (367, 471, 474, 792, 969, 1308, 1327, 1480, 2113, 2185, 2268)
   and ta.ti_id = t.id and ta.au_id = a.id and tk.ti_id = t.id and tk.kw_id = k.id group by keyword;

select t.id from titles as t, authors as a, ti_au as ta where 
  a.id in (2446, 844, 2734)
  and ta.ti_id = t.id and ta.au_id=a.id group by t.id;

select t.id from titles as t, authors as a, ti_au as ta where 
  a.id in (1048)
  and ta.ti_id = t.id and ta.au_id=a.id group by t.id;

select id, lastn, firstn from authors where lastn in
   ('Yamaguchi', 'Murashige', 'Yoshihisa', 'Shimojo', 'Mehmood', 'Kawai']
   order by lastn, firstn;

select id, lastn, firstn from authors where lastn in
   ('Rahdari', 'Brusilovksy')
   order by lastn, firstn;

select t.id from titles as t, authors as a, ti_au as ta where 
  a.id in (2384)
  and ta.ti_id = t.id and ta.au_id=a.id group by t.id;


select id, lastn, firstn from authors where lastn in
   ('Sasaoka', 'Yamakata', 'Tajima')
   order by lastn, firstn;

select t.id from titles as t, authors as a, ti_au as ta where 
  a.id in (2366)
  and ta.ti_id = t.id and ta.au_id=a.id group by t.id;

select id, lastn, firstn from authors where lastn in
   ('Tilekbay', 'Yang', 'Lewkowicz', 'Suryapranata', 'Kim')
   order by lastn, firstn;

select t.id from titles as t, authors as a, ti_au as ta where 
  a.id in (3617, 3249)
  and ta.ti_id = t.id and ta.au_id=a.id group by t.id;

select id, lastn, firstn from authors where lastn in
   ('Liu', 'Sra')
   order by lastn, firstn;

select id, lastn, firstn from authors where lastn in
   ('Guo', 'Mohanty', 'Hao', 'Gou', 'Ren')
   order by lastn, firstn;

select t.id from titles as t, authors as a, ti_au as ta where 
  a.id in (3776, 3242, 2112)
  and ta.ti_id = t.id and ta.au_id=a.id group by t.id;

select id, lastn, firstn from authors where lastn in
   ('Mitra', 'Patil', 'Mothish', 'Kumar', 'Mukhopadhyay', 'Murthy', 'Chakrabarti', 'Biswas')
   order by lastn, firstn;

select t.id from titles as t, authors as a, ti_au as ta where 
  a.id in (2522, 4726, 2526, 1918)
  and ta.ti_id = t.id and ta.au_id=a.id group by t.id;

select id, lastn, firstn from authors where lastn in
   ('Yang', 'Haeri', 'Magaki', 'Zarrin-Khameh', 'Gu', 'Chen')
   order by lastn, firstn;

 authors: [Chunxu Yang, Mohammad Haeri, Shino Magaki, Neda Zarrin-Khameh, Hongyan Gu, Xiang ‘Anthony’ Chen]
