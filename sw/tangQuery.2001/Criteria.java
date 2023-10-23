/// Scoring criteria
/// By Brygg Ullmer
/// Begun May 7, 2002

import java.lang.reflect.*;


public class Criteria {

  Field  field = null;
  String fieldName = null; 
  String dispStr = null;

  int fieldType = 1; // 1 == double, 2 == int

  double target    = 0;

  double minVal, maxVal, range;

///////////////////// Eval by Criteria /////////////////////////

  public Criteria(String dispStr, String fieldName, int fieldType,
                  double target, double minVal, double maxVal) {

    BldgRecord br = new BldgRecord();
    setField(br, fieldName, fieldType);

    this.dispStr = dispStr;
    this.target = target;
    this.range  = range;

    this.minVal = minVal;
    this.maxVal = maxVal;
    this.range = maxVal - minVal;
  } 

///////////////////// Eval by Criteria /////////////////////////

  public double evalByCriteria(double val) {

    if (val > maxVal)  {return -1;}
    if (val <= minVal) {return -1;} // <= kills "zeros"

    double result = Math.abs(val - target) / range;
    return result;
  } 

///////////////////// Eval by Criteria /////////////////////////
  
  public double evalByCriteria (BldgRecord br) {

    double result = -1;

    switch (fieldType) {
      case 1: 
        double dval = br.getFloat(field);
	result = evalByCriteria(dval);
	break;
	
      case 2: 
        int ival = br.getInt(field);
	result = evalByCriteria(ival);
	break;

      default:
        dbg("evalByCriteria: don't recognize fieldType; results bogus");
    }
    return result;
  }

///////////////////// setField /////////////////////////
  
  public void setField (BldgRecord br, String fieldName, int fieldType) {

    this.fieldName = fieldName;
    field = br.brGetField(fieldName);
  }

/////////////////////// dbg ///////////////////////

  private static int dcnt;
  public static void dbg(String s) {
    System.out.println("BldgDbMgr[" + (dcnt++) + "] " + s);
  }
}

/// END ///

