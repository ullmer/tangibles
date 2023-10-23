/// Data logger
/// By Brygg Ullmer
/// Begun April 11, 2002

import java.io.*;
import java.util.*;

////////////////////////////////////////////////
////////////////// Logger //////////////////////
////////////////////////////////////////////////

public class Logger {

  FileWriter file;
  String filename;

  String loggerId;

  String expIterFile = "expID";

  boolean constantFlush = false;

  Calendar cal;
  Date d;

  long firstTime = -1, currentTime = -1;

/////////////////// constructor /////////////////////////  

  public Logger(String progName) {

    cal = Calendar.getInstance();
    d   = cal.getTime();

    loggerId = getExperimentId();

    dbg("SESSION: " + loggerId);

    filename = "log/" + progName + "." + loggerId;

    try {
      file = new FileWriter(filename, true); // append, in case it exists
    } catch (Exception e) {

      dbg("constructor exception on creating file " + filename);
      dbg(e.toString());
    }

    firstTime = System.currentTimeMillis();

    logString("start " + getDate() + " " + getTime());

    try {
      file.flush();
    } catch (Exception e) {}
  } 
  
/////////////////// finalize /////////////////////////  

  protected void finalize() throws Throwable {

    super.finalize();

    dbg("finalize");

    file.flush();
    file.close();
  }

/////////////////// flush /////////////////////////  

  public void flush() { 
    try {
      file.flush();
    } catch (Exception e) {}
  }

/////////////////// doubleChar /////////////////////////  

  private String dc(int val) { // pad single-digit numbers with 0

    String result = "" + val;

    if (result.length() == 2) {return result;}
    result = "0" + result;

    return result;
  }

/////////////////// get Date/Time /////////////////////////  

  public String getDate() {
    String year = "" + cal.get(Calendar.YEAR);
    String month = dc(cal.get(Calendar.MONTH) + 1);
    String day   = dc(cal.get(Calendar.DAY_OF_MONTH));

    String date = year + "-" + month + "-" + day;
    return date;
  }

  public String getTime() {
    String time = dc(cal.get(Calendar.HOUR_OF_DAY))   + ":" + 
                  dc(cal.get(Calendar.MINUTE)) + ":" + 
		  dc(cal.get(Calendar.SECOND));

    return time;
  }

/////////////////// logString /////////////////////////  

  public void logStr(String str) { logString(str); }

  public void logString(String str) {

//  dbg("logging: " + str);

    long currentTime = System.currentTimeMillis();

//  long diffTime = currentTime - firstTime;
//  String outstr = diffTime + "\t" + str + "\n";

    String outstr = currentTime + "\t" + str + "\n";

    try {
      file.write(outstr, 0, outstr.length());

      if (constantFlush) {file.flush();}

    } catch (Exception e) {
      dbg("logString: exception " + e.toString());
    }
  }

///////////////////// getExperimentId ///////////////////////

  public String getExperimentId() { // returns a four-character string

   try {

    // Check if file exists

     File checkId = new File(expIterFile); 
     boolean fileExists = checkId.exists();

    // If it exists, read it

     int num = 0;

     if (fileExists) {
       FileReader reader = new FileReader(expIterFile); 

       num = readNum(reader);

       dbg("readNum: " + num);

       if (num == -1) {
         dbg("getExperimentId: failure with read; unsure, punting");
	 System.exit(0);
       }
     }

    // Increment
     num++; 

    // Save it
     FileWriter writer = new FileWriter(expIterFile);
     writeNum(writer, num);

     String valstr = idnum2str(num);
     return valstr;

    } catch (Exception e) {
      dbg("getExperimentId exception: " + e.toString());
      System.exit(0);
      return null;
    }
  }

///////////////////// getNum ///////////////////////

  private int readNum(FileReader f) { // returns digits until CR/LF


    try {
      if (f.ready() == false) {
        dbg("readNum: reader isn't ready; punting");
        System.exit(0 );
      }

      char buffer[]  = new char[10];

      int len = f.read(buffer, 0, 9);
      f.close();

      int idx;

      for (idx=0; idx<len; idx++) {
        if (buffer[idx] < '0' || buffer[idx] > '9') {break;}
      }

      String str = new String(buffer, 0, idx);
      int result = Integer.parseInt(str);
      return result;

    } catch (Exception e) {

      dbg("readNum exception: " + e.toString());
      return -1;
    }
  }

///////////////////// idnum2str ///////////////////////

  private String idnum2str(int val) {

    String valstr;

    if (val < 10) {
      valstr = "00" + val;
    } else if (val < 100) {
      valstr = "0" + val;
    } else {
      valstr = "" + val;
    }

    return valstr;

  }
///////////////////// getNum ///////////////////////

  private void writeNum(FileWriter f, int val) { // returns digits until CR/LF

    String valstr = "" + val;

    try {
      f.write(valstr);
      f.close();
    } catch (Exception e) {

      dbg("getNum exception: " + e.toString());
    }
  }

///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("Logger." + (dcnt++) + ": " + s);
  } 
}

/// END ///

