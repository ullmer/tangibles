// By Brygg Ullmer, MIT Media Lab
// Begun May 14, 2001

import java.net.*;
import java.io.*;
import java.sql.*;
import java.util.*;

//////////////////////////////////////////////////////
/////////////////// Param Wheel Val /////////////////////
//////////////////////////////////////////////////////

public class ParamWheelVal {

//////////////////// fields /////////////////////

  public String name;
  public int    id;

/////////////////////// dbg ///////////////////////

  public static int dcnt;
  public static void dbg(String s) {
    System.out.println("ParamWheelVal[" + (dcnt++) + "] " + s);
  }
}

/// END ///

 
