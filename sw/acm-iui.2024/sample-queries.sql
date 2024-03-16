select * from titles as t, authors as a, ti_au as ta where a.lastn in ('Laney', 'Dewan') and 
                        ta.ti_id = t.id and ta.au_id = a.id;
