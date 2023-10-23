/// Parameter token model
/// By Brygg Ullmer, MIT Media Lab
/// Begun October 25, 2001

import java.util.*;
import java.awt.*;
import java.io.*;

///////////////////////////////////////////////////////////
//////////////////  Parameter token ///////////////////////
///////////////////////////////////////////////////////////


  // NOTE: implementing this quickly, partly as a placeholder
  // Eventually, will need to become a more abstract class, with
  // children to handle the bounds types of different parameters


public class PTokModel {

/////////////  METHODS ///////////////

// public ParamTok()

/////////////  MEMBERS ///////////////

  boolean verbose = true;

//  QRack parentRack = null;

  String paramName;
  Color  paramColor, projectColor;
  String visLabel;

  boolean discreteParam = false;
  boolean boolParam = false;
  ParamWheel pwheel     = null;

//  String paramUnits;

  int boundsSignificantFigures = 2;

  int    tokId = -1;

  private double lowerBound = -1;
  private double upperBound = -1;

  double upperThresh = -1; // "kick-up"

  // NOTE: the following may need to be rethought; or rather, the hash
  //  in ptok dbase perhaps should be revisited.

  int currentRawLowerVal = -1;
  int currentRawUpperVal = -1;

  int    rawRange    = 255;
  double scaledRange = -1;

  private double currentScaledLowerVal = -1;
  private double currentScaledUpperVal = -1;

  int currentRack       = -1;
  int currentCell       = -1;
  int lastCell          = -1;

  boolean invertTok = false;

  private TokMWatchdog watchdog = null;

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////

 ////////////////////  constructor /////////////////////////////

  public PTokModel() {
    watchdog = new TokMWatchdog();
  }
  
 ////////////////////  describeState /////////////////////////////

  public String describeState() {

    if (pwheel == null) {
      dbg("genSqlSubstring: null pwheel; punting");
      return null;
    }

    String result = "{" + pwheel.paramName + " " + currentCell + " ";

    if (invertTok) {
      result += currentRawUpperVal + " " + currentScaledUpperVal;
    } else {
      result += currentRawLowerVal + " " + currentScaledLowerVal;
    }

    result += "}";

    return result;
  }



 ////////////////////  getSqlSubstring /////////////////////////////

  public String genSqlSubstring() {

    String result = "";

   // handle discrete params

    if (discreteParam == true) {

      String param, value;

      if (pwheel == null) {
        dbg("Problem in getSqlSubstring -- null pwheel!");
	return result;
      }

      try {
        if (pwheel.selectedVal == -1) {
          dbg("genSqlSubstring: selectedVal is null; ignoring");
	  return "";
        } 

        param = pwheel.valsName;
        value = pwheel.getVal(pwheel.selectedVal);

	if (boolParam == false) {

          result = "(" + param + " = '" + value + "')";

	} else {

          result = "(" + param + "_" + value + " = true)";
	}

      } catch (Exception e) {
        dbg("genSqlSubstring exception (d): " + e.toString());
      }

      //dbg("genSqlSubstring: " + result);
      return result;
    }

   // handle continuous params

    if (pwheel == null) {
      dbg("genSqlSubstring: null pwheel; punting");
      return null;
    }

    double val = getScaledUpper();
    String num = pwheel.cleanupNumber(val);

//    dbg("scaledUpper: " + getScaledUpper());
//    dbg("num: " + num);

    if (invertTok == false) {

      if (getScaledUpper() > upperThresh) { // no upper bound
        result = "";

        return result;
      }

      result = "(" + paramName + " < " + num + ")";
      return result;

    } else { // inverted!

      result = "(" + paramName + " > " + num + ")";

      return result;
    }
  }

  public double roundBound(double val) {

    double multiplier = Math.pow(10., boundsSignificantFigures);

    double result = val * multiplier;

    result = Math.round(result) / multiplier;
    return result;
  }

 ////////////////////  getResults /////////////////////////////

  public Vector getResults(BldgDbMgr dbMgr) {

    Vector results = null;

   // handle discrete params

    if (discreteParam == true) {

      if (pwheel == null) {
        dbg("Problem in getSqlSubstring -- null pwheel!");
	return null;
      }

      String param, value;

      try {
        if (pwheel.selectedVal == -1) {
          dbg("genSqlSubstring: selectedVal is null; ignoring");
	  return null;
        } 

        param = pwheel.valsName;
        value = pwheel.getVal(pwheel.selectedVal);

	if (boolParam == false) {

          results = dbMgr.getRecsDiscrete(param, value, false);

	} else {

          results = dbMgr.getRecsDiscrete(param, value, true);
	}

      } catch (Exception e) {
        dbg("getResults exception (d): " + e.toString());
      }

      //dbg("genSqlSubstring: " + result);
      return results;
    }

   // handle continuous params

    if (pwheel == null) {
      dbg("genSqlSubstring: null pwheel; punting");
      return null;
    }

    double val = getScaledUpper();
    String num = pwheel.cleanupNumber(val);

    if (invertTok == false) {

      if (getScaledUpper() > upperThresh) { // no upper bound
        return dbMgr.getGreaterRecs(paramName, 0);
	// HACKED FOR MIN OF ZERO!
      }

      results = dbMgr.getLesserRecs(paramName, num);

    } else { // inverted!

      results = dbMgr.getGreaterRecs(paramName, num);
    }

    return results;
  }
 ////////////////////  getAbs /////////////////////////////

  public double getAbsLower() { return lowerBound; }
  public double getAbsUpper() { return upperBound; }
  public double getAbsRange() { return scaledRange; }

 ////////////////////  getBoolName /////////////////////////////

  public String getBoolName() {

    if (pwheel == null) {
      dbg("getBoolName problem: pwheel == null!");
      return null;
    }
  
    String param = pwheel.valsName;
    String value = pwheel.getVal(pwheel.selectedVal);

    String result = param + "_" + value;
    return result;
  }

 ////////////////////  getScaled /////////////////////////////

  public double getScaledLower() {return currentScaledLowerVal;}
  public double getScaledUpper() {return currentScaledUpperVal;}

  public double getUpperThresh() {return upperThresh;}

 ////////////////////  getRatio /////////////////////////////

  public double getRatioLower() {
    double result = currentRawLowerVal / (double) rawRange;
    return result;
  }

  public double getRatioUpper() {
    double result = currentRawUpperVal / (double) rawRange;
    return result;
  }

 ////////////////////  constructor /////////////////////////////

  public PTokModel(String paramName, String visLabel, ParamWheel pwheel,
                   double lowerBound, double upperBound,
                   int tokId, Color paramColor, Color projectColor) {

    watchdog = new TokMWatchdog();

    this.paramName  = paramName;
    this.visLabel   = visLabel;

    this.pwheel = pwheel;

    this.lowerBound = lowerBound;
    this.upperBound = upperBound;
    scaledRange = upperBound - lowerBound;

    this.tokId = tokId;
    this.paramColor = paramColor;
    this.projectColor = projectColor;
  }
 
 ////////////////////  constructor /////////////////////////////

  public PTokModel(String paramName, String visLabel, ParamWheel pwheel,
                   int tokId, Color paramColor, Color projectColor) {

    watchdog = new TokMWatchdog();

    discreteParam = true;
    this.pwheel = pwheel;

    this.paramName  = paramName;
    this.visLabel   = visLabel;

    this.tokId = tokId;
    this.paramColor = paramColor;
    this.projectColor = projectColor;
  }
 
  
 //////////////////// update Lower Val /////////////////////////////

  public boolean updateLowerVal(int rawVal) {

   if (rawVal == currentRawLowerVal) {return false;}

    currentRawLowerVal    = rawVal;
    currentScaledLowerVal = roundBound(rawVal * scaledRange / rawRange + lowerBound);

    return true;
  }

 ////////////////////  update Upper Val /////////////////////////////

  public boolean updateUpperVal(int rawVal) {

    if (rawVal == currentRawUpperVal) {return false;}

//dbg("updateUpperVal: " + rawVal);

    currentRawUpperVal    = rawVal;
    currentScaledUpperVal = roundBound(rawVal * scaledRange / rawRange + lowerBound);

    return true;
  }

 ////////////////////  isTokActive /////////////////////////////

  public boolean isTokActive() {

    if (watchdog == null) {
      dbg("isTokActive error: watchdog is null!"); 
      return false;
    }

    return watchdog.isTokActive();
  }

 ////////////////////  constructor /////////////////////////////

  public void tokWitnessed() {

    if (watchdog == null) {
      dbg("tokWitnessed error: watchdog is null!"); 
      return;
    }

    watchdog.tokWitnessed();
  }

 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("PTokModel." + (dcnt++) + ": " + s);
  } 
}  

//// END ////

