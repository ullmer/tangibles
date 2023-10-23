// Holder for building dbase entries

////////////////////////////////////////////
//////////// BldgRecord ///////////////////
////////////////////////////////////////////

import java.lang.reflect.*;

public class BldgRecord {

  int    bldg_id, mls;

  String address, floor_descript, highschool_abbrev, bldg_type, floorStr;

  int   area_num, zip, listing_price, ballpark_price, sq_foot, taxes;
  float acreage, floors, lat, lon;

  float distToA, distToB; // "special coords"

  boolean feature_club, feature_golf, feature_pool, 
          feature_porch, feature_waterfront;

/////////// methods ////////////

  BldgRecord() {}

/////////// methods ////////////

  Field brGetField(String fieldName) {
    Field result = null;

    try {
      result = this.getClass().getDeclaredField(fieldName);

      if (result == null) {
        dbg("brGetField: result is null!");
	return null;
      }
    } catch (Exception e) {
      dbg("getField error: " + e.toString());
      e.printStackTrace();
    }


    return result;
  }

/////////// getInt ////////////

  int getInt(Field whichField) {

    int result = 0;

    try {
      result = whichField.getInt(this);
    } catch (Exception e) {dbg("getInt error: " + e.toString());}

    return result;
  }

/////////// getFloat ////////////

  float getFloat(Field whichField) {

    float result = 0;

    try {
      result = whichField.getFloat(this);
    } catch (Exception e) {dbg("getFloat error: " + e.toString());}

    return result;
  }

/////////// getBoolean ////////////

  boolean getBoolean(Field whichField) {

    boolean result = false;

    try {
      result = whichField.getBoolean(this);
    } catch (Exception e) {dbg("getBoolean error: " + e.toString());}

    return result;
  }

/*
  boolean getBoolean (String fieldName) {

    boolean result = false;

    try {
      Field field = this.getClass().getDeclaredField(fieldName);
      result = field.getBoolean(this);

    } catch (Exception e) {dbg("getBoolean(2) error: " + e.toString());}

    return result;
  }
*/
/////////// getString /////////////

  String getString(Field whichField) {

    String result = null;

    if (whichField == null) {
      dbg("getString bogosity: whichField = null!");
      return null;
    }

    try {
      result = (String) whichField.get(this);
    } catch (Exception e) {
       dbg("getString (" + whichField.getName() +
           ") error: " + e.toString()); 

       e.printStackTrace();
    }
       

//dbg("getString called on " + whichField);
//dbg("result: " + result + " | " + highschool_abbrev);

    return result;
  }

/*

/////////// getFloat ////////////

  float getFloat(String fieldName) {

    float result = 0;

    try {
      Field field = this.getClass().getDeclaredField(fieldName);
      result = field.getFloat(this);

    } catch (Exception e) {dbg("getInt error: " + e.toString());}

dbg("getFloat: " + result);

    return result;
  }
*/

/////////////////////// dbg ///////////////////////

  public static int dcnt;
  public static void dbg(String s) {
    System.out.println("BldgRecord[" + (dcnt++) + "] " + s);
  }
}

