// Display server for QueryUI
// By Brygg Ullmer, MIT Media Lab

// Descended from MediaFlow ParamWheelMgr
// Begun October 9, 2000
// Reworked on May 2, 2001

import java.net.*;
import java.io.*;
import java.sql.*;
import java.util.*;

//////////////////////////////////////////////////////
/////////////////// Param Wheel /////////////////////
//////////////////////////////////////////////////////

public class ParamWheelMgr {

//////////////////// fields /////////////////////

  Vector    pwVect = new Vector();

  Hashtable pwIdHash   = new Hashtable();
  Hashtable pwNameHash = new Hashtable();

//////////////////// methods /////////////////////

//  public ParamWheelMgr(DbThread dbthread) 


/////////////////////////////////////////////////
//////////////////// bodies /////////////////////
/////////////////////////////////////////////////

///////////// addWheel ///////////////

  public void addWheel(ParamWheel wheel) {

    dbg("addWheel runs on " + wheel.paramName);

    pwVect.addElement(wheel);

    Integer idKey = new Integer(wheel.tagId);
    pwIdHash.put(idKey, wheel);

    String nameKey = wheel.paramName;
    pwNameHash.put(nameKey, wheel);
  }

///////////// listParams ///////////////

  public void listParams() {

    dbg("listing params: ");

    int size = pwVect.size();

    for (int i=0; i<size; i++) {
      ParamWheel el = (ParamWheel) pwVect.elementAt(i);
      dbg(el.paramName + " " + el.tagId);
    }
  }

///////////// getById ///////////////

  public ParamWheel getId(int tagId) {

    Integer idKey = new Integer(tagId);

    ParamWheel result = (ParamWheel) pwIdHash.get(idKey);
    return result;
  }

///////////// getByName ///////////////

  public ParamWheel getName(String name) {

    ParamWheel result = (ParamWheel) pwNameHash.get(name);

    if (result == null) {
      dbg("getName error: null result on " + name);
    }
    
    return result;
  }

///////////// loadDefaultWheels ///////////////

  public void loadDefaultWheels(DbThread dbthread) {


/// CONSORTIUM

/*
    ParamWheel consort = new ParamWheel(dbthread);

    consort.paramName    = "consort";
    consort.valsQuery    = "select mg.metagroup_id, mg.fullname\n" + 
                           "  from MetaGroup mg, MetaGroupType mgt where\n" +
			   "    mg.type = mgt.mgtype_id and\n" +
			   "    mgt.type = 'consortium';";

    consort.projQuery     = "select pr.project_id" + 
                           "  from MetaGroup mg, MetaGroupType mgt, Project pr, ProjectMetaGroup pmg where" +
			   "  pmg.project = pr.project_id and pmg.metagroup = mg.metagroup_id and" +
			   "    mg.type = mgt.mgtype_id and" +
			   "    mgt.type = 'consortium' and" +
			   "    mg.fullname='%s';";

    consort.valsKeyfield = "metagroup_id";
    consort.valsName     = "fullname";
    consort.setColor(155,0,0);
    consort.tagId = 190;
    consort.tier = 0;

    consort.loadVals();
    addWheel(consort);
*/

/// High school

    ParamWheel hs = new ParamWheel(dbthread);

    hs.paramName    = "high school";
    hs.valsQuery    = "select highschool_abbrev from building "+
                       "  where highschool_abbrev is not null "+
                       "  group by highschool_abbrev " +
                       "  order by highschool_abbrev";


    hs.projQuery    = "select mls from building " +
                      "  where highschool_abbrev = '%s';";

    hs.valsKeyfield = "highschool_abbrev";
    hs.valsName     = "highschool_abbrev";
    //hs.setColor(216,169,40);
    hs.setColor(224, 170, 15);
    hs.tagId = 65533;
    hs.tier = 2;
    hs.continParam = false;

    hs.loadVals();
    addWheel(hs);

/// Building type

    ParamWheel bt = new ParamWheel(dbthread);

    bt.paramName    = "bldg type";
    bt.valsQuery    = "select bldg_type from building "+
                       "  where bldg_type is not null "+
                       "  group by bldg_type " +
                       "  order by bldg_type";


    bt.projQuery    = "select mls from building " +
                      "  where bldg_type = '%s';";

    bt.valsKeyfield = "bldg_type";
    bt.valsName     = "bldg_type";
    //bt.setColor(169,40,216);
    bt.setColor(52,86,134);
    bt.tagId = 190;
    bt.tier = 2;
    bt.continParam = false;
 
    bt.loadVals();
    addWheel(bt);

/// Features

    bt = new ParamWheel(dbthread);

    bt.paramName    = "features";
    bt.valsQuery    = "select minortype as feature from typeKeeper"+
                       "  where majortype = 'feature' " +
                       "  order by minortype";

    bt.projQuery    = "select mls from building " +
                      "  where feature_%s = true;";

    bt.valsKeyfield = "feature";
    bt.valsName     = "feature";
    //bt.setColor(40, 169, 216);
    bt.setColor(155,170,192);
    bt.tagId = 8225;
    bt.tier = 2;
    bt.continParam = false;

    bt.loadVals();
    addWheel(bt);

/// GROUP

/*    ParamWheel   group = new ParamWheel(dbthread);

    group.paramName    = "group";
    group.valsQuery    = "select group_id, name from ResearchGroup order by name;";

    group.projQuery    = "select pr.project_id from ResearchGroup gr, Project pr, ProjectGroup pg " +
                         " where pg.resgroup = gr.group_id and pg.project = pr.project_id and " + 
			 " gr.name='%s';";

    group.valsKeyfield = "group_id";
    group.valsName     = "name";
    group.setColor(0,0,200); 
    group.tagId = 207; 
    group.tier = 1;

    group.loadVals();
    addWheel(group);

*/
 
    ParamWheel   sqfoot = new ParamWheel(dbthread);

    sqfoot.paramName    = "sqfoot";
    sqfoot.valsQuery    = "";

    sqfoot.valsQuery    = "select metagroup_id from MetaGroup where metagroup_id < 10";
    sqfoot.projQuery    = "select metagroup_id from MetaGroup where metagroup_id < 10";

    sqfoot.valsKeyfield = "metagroup_id";
    sqfoot.valsName     = "name";
    //sqfoot.setColor(0,0,200); 
    sqfoot.setColor(202, 140, 141);
    sqfoot.tagId = 207; 
    sqfoot.tier = 1;
    sqfoot.invertTok = true;
    sqfoot.queryValsMinded = false;

   // sqfoot.min = 1500;
    sqfoot.min = 0;
    sqfoot.max = 4400;
    sqfoot.increment = 100;

    sqfoot.loadVals();
    addWheel(sqfoot);

/// continuous

/*
    ParamWheel contin = new ParamWheel(dbthread);

    contin.paramName    = "contin1";
    contin.valsQuery    = "select metagroup_id from MetaGroup where metagroup_id < 10";
    contin.projQuery    = "select metagroup_id from MetaGroup where metagroup_id < 10";

    contin.valsKeyfield = "metagroup_id";
    contin.valsName     = "fullname";
    contin.setColor(155,155,0);
    contin.tagId = 172;
    contin.tier = 3;

    contin.loadVals();
*/

/// Floors

    bt = new ParamWheel(dbthread);

//    bt.paramName    = "floors";

    bt.paramName    = "distToA";
    bt.valsQuery    = "select floorStr from building "+
                       "  where floors is not null "+
                       "  group by floorStr" +
                       "  order by floorStr";


    bt.projQuery    = "select mls from building " +
                      "  where floors >= %s;";

    bt.valsKeyfield = "distToA";
    bt.valsName     = "distToA";

    //bt.setColor(40,169,216);
    bt.setColor(15,44,92);
    bt.tagId = 51;
    bt.tier = 2;

    bt.min = 0;
    bt.max = 40; // max = ~.92
    bt.increment = 0.01;
//    bt.invertTok = true;
    bt.queryValsMinded = false;

    bt.loadVals();
    addWheel(bt);

/// acreage 

    ParamWheel acreage = new ParamWheel(dbthread);

    acreage.paramName    = "acreage";
    acreage.valsQuery    = "select metagroup_id from MetaGroup where metagroup_id < 10";
    acreage.projQuery    = "select metagroup_id from MetaGroup where metagroup_id < 10";

    acreage.valsKeyfield = "metagroup_id";
    acreage.valsName     = "fullname";
//    acreage.setColor(155,155,0);
//    acreage.setColor(0,200,0);
    acreage.setColor(253,218,87);
    acreage.tagId = 172;
    acreage.tier = 3;

    acreage.min = 0;
    acreage.max = 3.;
    acreage.increment = .1;
    acreage.invertTok = true;
    acreage.queryValsMinded = false;

    acreage.loadVals();
    addWheel(acreage);

/// price

    ParamWheel price = new ParamWheel(dbthread);

//    price.paramName    = "price2";
    price.paramName    = "price";
    price.valsQuery    = "select metagroup_id from MetaGroup where metagroup_id < 10";
    price.projQuery    = "select metagroup_id from MetaGroup where metagroup_id < 10";

    price.valsKeyfield = "metagroup_id";
    price.valsName     = "fullname";
    //price.setColor(0,155,155);
    //price.setColor(200,0,0);
    price.setColor(158,42,72);
    price.tagId = 76;
    price.tier = 3;

    price.min       =  0;
    price.max       = 1200;
    price.increment = 10;
    price.queryValsMinded = false;

    price.loadVals();
    addWheel(price);

/// taxes


    ParamWheel tax = new ParamWheel(dbthread);

    tax.paramName    = "taxes";
    tax.setColor(119, 33, 179); //purple
    tax.tagId = 99;
    tax.tier = 3;

    tax.min       =  0;
    tax.max       = 5000;
    tax.increment = 25;
    tax.queryValsMinded = false;

    tax.loadVals();
    addWheel(tax);

//// B

    tax = new ParamWheel(dbthread);

    tax.paramName    = "distToB";
    tax.setColor(119, 33, 179); //purple
    tax.tagId = 181;
    tax.tier = 3;

    tax.min       = 0;
    tax.max       = 40;
    tax.increment = .1;
    tax.queryValsMinded = false;

    tax.loadVals();
    addWheel(tax);
  }

////////////////////  Main /////////////////////////////

  static public void main(String args[]) {

    DbThread dbthread = new DbThread("pldb", "tmg-internal");

    ParamWheelMgr mgr = new ParamWheelMgr();
    mgr.loadDefaultWheels(dbthread);

    mgr.getName("consort").printVals();

    dbg("TEST");
    mgr.getId(65533).printVals();
  }

/////////////////////// dbg ///////////////////////

  public static int dcnt;
  public static void dbg(String s) {
    System.out.println("ParamWheelMgr[" + (dcnt++) + "] " + s);
  }
}

/// END ///

 
