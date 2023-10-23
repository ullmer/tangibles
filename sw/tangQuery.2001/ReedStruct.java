/// Query UI code 
/// By Brygg Ullmer, MIT Media Lab
/// Begun April 20, 2001
///
/// Based on threading template by Ben Fry (fry@media.mit.edu),
/// 4/18/2001, and WinHelp Java Tutorial: AnimatorApplication.java,
/// Arthur van Hoff

import java.util.*;
import java.io.*;

///////////////////////////////////////////////////////////
////////////////////  ReedStruct /////////////////////////////
///////////////////////////////////////////////////////////

public class ReedStruct {

/////////////  fields ///////////////

  public int byteOrder;     // HI_ORDER (1) or LO_ORDER (0);
  public int previousState;
  public int currentState;

  public int transition;   // packing of previousState + currentState

  public int whichPad;
  public int whichPos;

///////////////////// print ///////////////////////

  public void print() {
    dbg("order "        +  byteOrder + ", " +
        "previousState " + Integer.toBinaryString(previousState) + ", " +
        "currentState "      + Integer.toBinaryString(currentState) + ", " +
        "transition "        + Integer.toBinaryString(transition) + ", " +
        "whichPad " + whichPad + ", " +       
        "whichPos " + whichPos);
  }

///////////////////// Debug ///////////////////////

  public static int dcnt;

  static public void dbg(String s) {

    System.out.println("ReedStruct." + (dcnt++) + ": " + s);
  } 
}

//// END ////

