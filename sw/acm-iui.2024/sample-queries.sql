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

   
