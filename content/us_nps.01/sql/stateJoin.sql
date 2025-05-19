select pd.name from parkDetails as pd
  join parkDetailState as pds on pds.parkDetailId = pd.id
  join usStates        as st  on pds.stateId      = st.id
  where st.abbrev='SC';

select st.abbrev, group_concat(pd.abbrev) from parkDetails as pd
  join parkDetailState as pds on pds.parkDetailId = pd.id
  join usStates        as st  on pds.stateId      = st.id
  group by st.abbrev;

