/// Plot test
/// By Brygg Ullmer, MIT Media Lab
/// Begun November 1, 2001
///
/// Based on threading template by Ben Fry (fry@media.mit.edu),
/// 4/18/2001, and WinHelp Java Tutorial: AnimatorApplication.java,
/// Arthur van Hoff

import java.util.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.geom.*;
import java.awt.image.*;

import javax.swing.*;
import java.io.*;

///////////////////////////////////////////////////////////
/////////////////  Experiment Set /////////////////////////
///////////////////////////////////////////////////////////

public class ExperSet { // experiment set

/////////////  MEMBERS ///////////////

  BldgDbMgr      dbMgr = null;
  Hashtable   experSet = null;

  Experiment currentExp = null;

  int currentExpNum = 0;

//  int currentExpNum = 1;

  Logger logger = null;

  int numExpSets = 4;
  int activeExpSet = -1; // active experiment set = AES
  int activeExpIdx = -1; // index of AES
  int activeExpMax = -1; // max idx (len) of AES

  static int[][] expSeq =  // experiment sequences

    {{1, 2},
     {2, 1},
     {10,11,12,13},
     {20,21,22,23}};

  static int[] expLen = {2,2,4,4}; // length of experiment sets

  private int numExperiments = 0;

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////


////////////////////  Score /////////////////////////////

  public ExperSet(BldgDbMgr dbMgr) {

    this.dbMgr = dbMgr;
    experSet   = new Hashtable();

    loadExperiments();
  }


////////////////////  setLogger /////////////////////////////

  public void setLogger(Logger logger) {

    this.logger = logger;

    Enumeration keys = experSet.keys();

    for (; keys.hasMoreElements(); ) {

      Object key = keys.nextElement();
      Experiment exp = (Experiment) experSet.get(key);

      exp.setLogger(logger);
    }
  }

////////////////////  loadExperiments /////////////////////////////

  public void loadExperiments() {

    Experiment expr;
    Criteria   crit1, crit2, crit3, crit4;



  ////////////////////////

//// TRIAL ////

    expr = new Experiment(dbMgr, 1);

    crit1 = new Criteria("max sqft", "sq_foot", 1, 4300, 0, 4300);
    crit2 = new Criteria("max acreage", "acreage", 1, 3, 0, 3);
    crit3 = new Criteria("near A", "distToA", 1, 0, 0, 40);

    expr.addCriteria(crit1);
    expr.addCriteria(crit2);
    expr.addCriteria(crit3);

//    expr.expectedScore = 1.5;
//    expr.expectedScore = .1;
//    expr.expectedScore = .07;
    expr.expectedScore = .08;
    addExperiment(expr);



  ////////////////////////

    expr = new Experiment(dbMgr, 2);

    crit1 = new Criteria("near A", "distToA", 1, 0, 0, 40);
    crit2 = new Criteria("near B", "distToB", 1, 0, 0, 40);
    crit3 = new Criteria("min price", "listing_price", 1, 0, 0, 1200);

    expr.addCriteria(crit1);
    expr.addCriteria(crit2);
    expr.addCriteria(crit3);

//    expr.expectedScore = .15;
//    expr.expectedScore = .315;
    expr.expectedScore = .26;

    addExperiment(expr);

//////////////////////////////////

/// RUN 1/

  ////////////////////////

    expr = new Experiment(dbMgr, 10);

    crit1 = new Criteria("min price", "listing_price", 1, 0, 0, 1200);
    crit2 = new Criteria("max acreage", "acreage", 1, 3, 0, 3);

    expr.addCriteria(crit1);
    expr.addCriteria(crit2);
//    expr.expectedScore = .15;
    expr.expectedScore = .04;

    addExperiment(expr);

  ////////////////////////

    expr = new Experiment(dbMgr, 11);

    crit1 = new Criteria("near A", "distToA", 1, 0, 0, 40);
    crit2 = new Criteria("max sqft", "sq_foot", 1, 4300, 0, 4300);

    expr.addCriteria(crit1);
    expr.addCriteria(crit2);
//    expr.expectedScore = .15;
//    expr.expectedScore = .043;
    expr.expectedScore = .043;
//    expr.expectedScore = .040;

    addExperiment(expr);

  ////////////////////////

    expr = new Experiment(dbMgr, 12);

    crit1 = new Criteria("medium price", "listing_price", 1, 500, 0, 1200);
    crit2 = new Criteria("medium acreage", "acreage", 1, 1.5, 0, 3);
    crit3 = new Criteria("near B", "distToB", 1, 0, 0, 40);

    expr.addCriteria(crit1);
    expr.addCriteria(crit2);
    expr.addCriteria(crit3);
//    expr.expectedScore = 2.5;
//    expr.expectedScore = .03;
//    expr.expectedScore = .09;
//    expr.expectedScore = .17;
      expr.expectedScore = 0;

    addExperiment(expr);

  /////////////////////////

    expr = new Experiment(dbMgr, 13);

    crit1 = new Criteria("medium sqft", "sq_foot", 1, 2000, 0, 4300);
    crit2 = new Criteria("max acreage", "acreage", 1, 3, 0, 3);
    crit3 = new Criteria("price ~= 300", "listing_price", 1, 300, 0, 1200);
    crit4 = new Criteria("near A", "distToA", 1, 0, 0, 40);

    expr.addCriteria(crit1);
    expr.addCriteria(crit2);
    expr.addCriteria(crit3);
    expr.addCriteria(crit4);

//    expr.expectedScore = 2.5;
//    expr.expectedScore = .13;
    expr.expectedScore = .083;

    addExperiment(expr);


/////////////////////////////////////////////////////////////

//////////// RUN 2 /////////////

/// TEST ///

    expr = new Experiment(dbMgr, 20);

    crit1 = new Criteria("min price", "listing_price", 1, 0, 0, 1200);
    crit2 = new Criteria("max sqft", "sq_foot", 1, 4300, 0, 4300);

    expr.addCriteria(crit1);
    expr.addCriteria(crit2);
//    expr.expectedScore = .15;
    expr.expectedScore = .14;
//    expr.expectedScore = .10;

    addExperiment(expr);

  /////////////////////////

    expr = new Experiment(dbMgr, 21);

    crit1 = new Criteria("max acreage", "acreage", 1, 3, 0, 3);
    crit2 = new Criteria("near B", "distToB", 1, 0, 0, 40);

    expr.addCriteria(crit1);
    expr.addCriteria(crit2);
//    expr.expectedScore = 1.5;
//    expr.expectedScore = .1;
//    expr.expectedScore = .07;
    expr.expectedScore = .14;
      

    addExperiment(expr);

  /////////////////////////

    expr = new Experiment(dbMgr, 22);

    crit1 = new Criteria("medium price", "listing_price", 1, 550, 0, 1200);
    crit2 = new Criteria("medium sqft", "sq_foot", 1, 2000, 0, 4300);
    crit3 = new Criteria("near A", "distToA", 1, 0, 0, 40);

    expr.addCriteria(crit1);
    expr.addCriteria(crit2);
    expr.addCriteria(crit3);
//    expr.expectedScore = .15;
//    expr.expectedScore = .166;
//    expr.expectedScore = .18;
//    expr.expectedScore = .001;
//    expr.expectedScore = .05;
//    expr.expectedScore = .15;
      expr.expectedScore = 0;

    addExperiment(expr);

  /////////////////////////

    expr = new Experiment(dbMgr, 23);

    crit1 = new Criteria("min price", "listing_price", 1, 0, 0, 1200);
    crit2 = new Criteria("medium sqft", "sq_foot", 1, 2000, 0, 4300);
    crit3 = new Criteria("acreage ~= 1", "acreage", 1, 1, 0, 3);
    crit4 = new Criteria("near B", "distToB", 1, 0, 0, 40);

    expr.addCriteria(crit1);
    expr.addCriteria(crit2);
    expr.addCriteria(crit3);
    expr.addCriteria(crit4);
//    expr.expectedScore = 2.5;
//    expr.expectedScore = .13;
    expr.expectedScore = .11;

    addExperiment(expr);

   //////////////////////////////////////////////////////////////
   ///////////////////////// ANNA ///////////////////////////////
   //////////////////////////////////////////////////////////////
   
   ////////////2 Parameters////////////////
  
  // 100
 
   expr = new Experiment(dbMgr, 100);
   crit1 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   crit2 = new Criteria("max sqft", "sq_foot", 1, 4300, 0, 4300);
   expr.expectedScore = .033;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   addExperiment(expr);
  

  // 101
 
   expr = new Experiment(dbMgr, 101);
   crit1 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   crit2 = new Criteria("max acreage", "acreage", 1, 3, 0, 3);
   expr.expectedScore = .026; 

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   addExperiment(expr);

   
   expr = new Experiment(dbMgr, 102);
   crit1 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   crit2 = new Criteria("min price", "listing_price", 1, 0, 0, 1200);
   expr.expectedScore = 0.07;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   addExperiment(expr);

   
   expr = new Experiment(dbMgr, 103);
   crit1 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   crit2 = new Criteria("min price", "listing_price", 1, 0, 0, 1200);
   expr.expectedScore = 0.102;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   addExperiment(expr);
   

   expr = new Experiment(dbMgr, 104);
   crit1 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   crit2 = new Criteria("min taxes", "taxes", 1, 0, 0, 5000);
   expr.expectedScore = 0.079;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   addExperiment(expr);

   
   expr = new Experiment(dbMgr, 105);
   crit1 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   crit2 = new Criteria("min taxes", "taxes", 1, 0, 0, 5000);
   expr.expectedScore = 0.105;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   addExperiment(expr);

   
   expr = new Experiment(dbMgr, 106);
   crit1 = new Criteria("min taxes", "taxes", 1, 0, 0, 5000);
   crit2 = new Criteria("max sqft", "sq_foot", 1, 4300, 0, 4300);
   expr.expectedScore = 0.103;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   addExperiment(expr);

   
   expr = new Experiment(dbMgr, 107);
   crit1 = new Criteria("min taxes", "taxes", 1, 0, 0, 5000);
   crit2 = new Criteria("max acreage", "acreage", 1, 3, 0, 3);
   expr.expectedScore = 0.038;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   addExperiment(expr);
   
   
   ////////////3 Parameters/////////////
   
   /*
   ("near A", "distToA", 1, 0, 0, 40);
   ("max acreage", "acreage", 1, 3, 0, 3);
   ("max sqft", "sq_foot", 1, 4300, 0, 4300);
   ("near B", "distToB", 1, 0, 0, 40);
   ("min price", "listing_price", 1, 0, 0, 1200);
   ("min taxes", "taxes", 1, 0, 0, 5000);
   ("medium price", "listing_price", 1, 500, 0, 1200);
   ("medium acreage", "acreage", 1, 1.5, 0, 3);
   ("medium taxes", "taxes", 1, 2500, 0, 5000);
   ("medium sqft", "sq_foot", 1, 2000, 0, 4300);
   */
   
   expr = new Experiment(dbMgr, 200);
   crit1 = new Criteria("min price", "listing_price", 1, 0, 0, 1200);
   crit2 = new Criteria("medium acreage", "acreage", 1, 1.5, 0, 3);
   crit3 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   expr.expectedScore = 0;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   addExperiment(expr);
   
   expr = new Experiment(dbMgr, 201);
   crit1 = new Criteria("min price", "listing_price", 1, 0, 0, 1200);
   crit2 = new Criteria("medium sqft", "sq_foot", 1, 2000, 0, 4300);
   crit3 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   expr.expectedScore = 0;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   addExperiment(expr);
  
 
   expr = new Experiment(dbMgr, 202);
   crit1 = new Criteria("max acreage", "acreage", 1, 3, 0, 3);
   crit2 = new Criteria("max sqft", "sq_foot", 1, 4300, 0, 4300);
   crit3 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   expr.expectedScore = 0.103;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   addExperiment(expr);

   
   expr = new Experiment(dbMgr, 203);
   crit1 = new Criteria("min taxes", "taxes", 1, 0, 0, 5000);
   crit2 = new Criteria("medium acreage", "acreage", 1, 1.5, 0, 3);
   crit3 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   expr.expectedScore = 0;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   addExperiment(expr);
  
 
   expr = new Experiment(dbMgr, 204);
   crit1 = new Criteria("min taxes", "taxes", 1, 0, 0, 5000);
   crit2 = new Criteria("medium acreage", "acreage", 1, 1.5, 0, 3);
   crit3 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   expr.expectedScore = 0;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   addExperiment(expr);
  
 
   expr = new Experiment(dbMgr, 205);
   crit1 = new Criteria("max acreage", "acreage", 1, 3, 0, 3);
   crit2 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   crit3 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   expr.expectedScore = 0.23;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   addExperiment(expr);
  
 
   expr = new Experiment(dbMgr, 206);
   crit1 = new Criteria("max sqft", "sq_foot", 1, 4300, 0, 4300);
   crit2 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   crit3 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   expr.expectedScore = 0.208;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   addExperiment(expr);
  
 
   expr = new Experiment(dbMgr, 207);
   crit1 = new Criteria("min price", "listing_price", 1, 0, 0, 1200);
   crit2 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   crit3 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   expr.expectedScore = 0.246;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   addExperiment(expr);
  
 
   expr = new Experiment(dbMgr, 208);
   crit1 = new Criteria("min taxes", "taxes", 1, 0, 0, 5000);
   crit2 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   crit3 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   expr.expectedScore = 0.234;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   addExperiment(expr);
  
 
   expr = new Experiment(dbMgr, 209);
   crit1 = new Criteria("medium price", "listing_price", 1, 500, 0, 1200);
   crit2 = new Criteria("medium acreage", "acreage", 1, 1.5, 0, 3);
   crit3 = new Criteria("near B", "distToB", 1, 0, 0, 40);
// expr.expectedScore = 0.201;
   expr.expectedScore = 0;



   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   addExperiment(expr);
  
 
   expr = new Experiment(dbMgr, 210);
   crit1 = new Criteria("min price", "listing_price", 1, 0, 0, 1200);
   crit2 = new Criteria("max sqft", "sq_foot", 1, 4300, 0, 4300);
   crit3 = new Criteria("near A", "distToA", 1, 0, 0, 40);
// expr.expectedScore = 0.17;
   expr.expectedScore = 0;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   addExperiment(expr);
  
 
   expr = new Experiment(dbMgr, 211);
   crit1 = new Criteria("medium taxes", "taxes", 1, 2500, 0, 5000);
   crit2 = new Criteria("max acreage", "acreage", 1, 3, 0, 3);
   crit3 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   expr.expectedScore = 0;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   addExperiment(expr);
  
 
   expr = new Experiment(dbMgr, 212);
   crit1 = new Criteria("medium taxes", "taxes", 1, 2500, 0, 5000);
   crit2 = new Criteria("max sqft", "sq_foot", 1, 4300, 0, 4300);
   crit3 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   expr.expectedScore = 0;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   addExperiment(expr);
   
   expr = new Experiment(dbMgr, 213);
   crit1 = new Criteria("min price", "listing_price", 1, 0, 0, 1200);
   crit2 = new Criteria("max acreage", "acreage", 1, 3, 0, 3);
   crit3 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   expr.expectedScore = 0.092;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   addExperiment(expr);

   expr = new Experiment(dbMgr, 214);
   crit1 = new Criteria("min price", "listing_price", 1, 0, 0, 1200);
   crit2 = new Criteria("max acreage", "acreage", 1, 3, 0, 3);
   crit3 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   expr.expectedScore = 0.143;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   addExperiment(expr);

   expr = new Experiment(dbMgr, 215);
   crit1 = new Criteria("min price", "listing_price", 1, 0, 0, 1200);
   crit2 = new Criteria("max sqft", "sq_foot", 1, 4300, 0, 4300);
   crit3 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   expr.expectedScore = 0.187;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   addExperiment(expr);

   expr = new Experiment(dbMgr, 216);
   crit1 = new Criteria("min price", "listing_price", 1, 0, 0, 1200);
   crit2 = new Criteria("max sqft", "sq_foot", 1, 4300, 0, 4300);
   crit3 = new Criteria("near B", "distToB", 1, 0, 0, 40);
//   expr.expectedScore = 0.147;
   expr.expectedScore = 0.2;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   addExperiment(expr);

   expr = new Experiment(dbMgr, 217);
   crit1 = new Criteria("min taxes", "taxes", 1, 0, 0, 5000);
   crit2 = new Criteria("max acreage", "acreage", 1, 3, 0, 3);
   crit3 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   expr.expectedScore = 0.098;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   addExperiment(expr);

   expr = new Experiment(dbMgr, 218);
   crit1 = new Criteria("min taxes", "taxes", 1, 0, 0, 5000);
   crit2 = new Criteria("max acreage", "acreage", 1, 3, 0, 3);
   crit3 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   expr.expectedScore = 0.142;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   addExperiment(expr);

   expr = new Experiment(dbMgr, 219);
   crit1 = new Criteria("min taxes", "taxes", 1, 0, 0, 5000);
   crit2 = new Criteria("max sqft", "sq_foot", 1, 4300, 0, 4300);
   crit3 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   expr.expectedScore = 0.129;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   addExperiment(expr);

   expr = new Experiment(dbMgr, 220);
   crit1 = new Criteria("min taxes", "taxes", 1, 0, 0, 5000);
   crit2 = new Criteria("max sqft", "sq_foot", 1, 4300, 0, 4300);
   crit3 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   expr.expectedScore = 0.167;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   addExperiment(expr);
   /////////////////4 Parameters///////////////
   
   /*
   
   ("near A", "distToA", 1, 0, 0, 40);
   ("max acreage", "acreage", 1, 3, 0, 3);
   ("max sqft", "sq_foot", 1, 4300, 0, 4300);
   ("near B", "distToB", 1, 0, 0, 40);
   ("min price", "listing_price", 1, 0, 0, 1200);
   ("min taxes", "taxes", 1, 0, 0, 5000);
   ("medium price", "listing_price", 1, 500, 0, 1200);
   ("medium acreage", "acreage", 1, 1.5, 0, 3);
   ("medium taxes", "taxes", 1, 2500, 0, 5000);
   ("medium sqft", "sq_foot", 1, 2000, 0, 4300);
   */
   
   expr = new Experiment(dbMgr, 300);
   crit1 = new Criteria("min taxes", "taxes", 1, 0, 0, 5000);
   crit2 = new Criteria("medium acreage", "acreage", 1, 1.5, 0, 3);
   crit3 = new Criteria("max sqft", "sq_foot", 1, 4300, 0, 4300);
   crit4 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   expr.expectedScore = 0;


   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   expr.addCriteria(crit4);
   addExperiment(expr);
   
   expr = new Experiment(dbMgr, 301);
   crit1 = new Criteria("min taxes", "taxes", 1, 0, 0, 5000);
   crit2 = new Criteria("acreage ~= 1", "acreage", 1, 1, 0, 3);
   crit3 = new Criteria("max sqft", "sq_foot", 1, 4300, 0, 4300);
   crit4 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   expr.expectedScore = 0;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   expr.addCriteria(crit4);
   addExperiment(expr);
   
   expr = new Experiment(dbMgr, 302);
   crit1 = new Criteria("min price", "listing_price", 1, 0, 0, 1200);
   crit2 = new Criteria("max acreage", "acreage", 1, 3, 0, 3);
   crit3 = new Criteria("medium sqft", "sq_foot", 1, 2000, 0, 4300);
   crit4 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   expr.expectedScore = 0;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   expr.addCriteria(crit4);
   addExperiment(expr);

   
   expr = new Experiment(dbMgr, 303);
   crit1 = new Criteria("min price", "listing_price", 1, 0, 0, 1200);
   crit2 = new Criteria("acreage ~= 1", "acreage", 1, 1, 0, 3);
   crit3 = new Criteria("max sqft", "sq_foot", 1, 4300, 0, 4300);
   crit4 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   expr.expectedScore = 0;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   expr.addCriteria(crit4);
   addExperiment(expr);

   
   expr = new Experiment(dbMgr, 304);
   crit1 = new Criteria("min taxes", "taxes", 1, 0, 0, 5000);
   crit2 = new Criteria("medium acreage", "acreage", 1, 1.5, 0, 3);
   crit3 = new Criteria("max sqft", "sq_foot", 1, 4300, 0, 4300);
   crit4 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   expr.expectedScore = 0;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   expr.addCriteria(crit4);
   addExperiment(expr);

   
   expr = new Experiment(dbMgr, 305);
   crit1 = new Criteria("min price", "listing_price", 1, 0, 0, 1200);
   crit2 = new Criteria("medium acreage", "acreage", 1, 1.5, 0, 3);
   crit3 = new Criteria("max sqft", "sq_foot", 1, 4300, 0, 4300);
   crit4 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   expr.expectedScore = 0;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   expr.addCriteria(crit4);
   addExperiment(expr);

   
   expr = new Experiment(dbMgr, 306);
   crit1 = new Criteria("min price", "listing_price", 1, 0, 0, 1200);
   crit2 = new Criteria("taxes ~= 1000", "taxes", 1, 1000, 0, 5000);
   crit3 = new Criteria("sqft ~= 1500", "sq_foot", 1, 1500, 0, 4300);
   crit4 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   expr.expectedScore = 0;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   expr.addCriteria(crit4);
   addExperiment(expr);

   
   expr = new Experiment(dbMgr, 307);
   crit1 = new Criteria("price ~= 800", "listing_price", 1, 800, 0, 1200);
   crit2 = new Criteria("med sqft", "sq_foot", 1, 2000, 0, 4300);
   crit3 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   crit4 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   expr.expectedScore = 0;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   expr.addCriteria(crit4);
   addExperiment(expr);
   

   expr = new Experiment(dbMgr, 308);
   crit1 = new Criteria("min price", "listing_price", 1, 0, 0, 1200);
   crit2 = new Criteria("acreage ~= 2", "acreage", 1, 2, 0, 3);
   crit3 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   crit4 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   expr.expectedScore = 0;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   expr.addCriteria(crit4);
   addExperiment(expr);

   expr = new Experiment(dbMgr, 309);
   crit1 = new Criteria("min price", "listing_price", 1, 0, 0, 1200);
   crit2 = new Criteria("max sqft", "sq_foot", 1, 4300, 0, 4300);
   crit3 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   crit4 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   expr.expectedScore = 0.267;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   expr.addCriteria(crit4);
   addExperiment(expr);

   expr = new Experiment(dbMgr, 310);
   crit1 = new Criteria("min taxes", "taxes", 1, 0, 0, 5000);
   crit2 = new Criteria("max sqft", "sq_foot", 1, 4300, 0, 4300);
   crit3 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   crit4 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   expr.expectedScore = 0.273;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   expr.addCriteria(crit4);
   addExperiment(expr);

   expr = new Experiment(dbMgr, 311);
   crit1 = new Criteria("min price", "listing_price", 1, 0, 0, 1200);
   crit2 = new Criteria("max acreage", "acreage", 1, 3, 0, 3);
   crit3 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   crit4 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   expr.expectedScore = 0.209;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   expr.addCriteria(crit4);
   addExperiment(expr);

   expr = new Experiment(dbMgr, 312);
   crit1 = new Criteria("min taxes", "taxes", 1, 0, 0, 5000);
   crit2 = new Criteria("max acreage", "acreage", 1, 3, 0, 3);
   crit3 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   crit4 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   expr.expectedScore = 0.23;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   expr.addCriteria(crit4);
   addExperiment(expr);

   expr = new Experiment(dbMgr, 313);
   crit1 = new Criteria("min price", "listing_price", 1, 0, 0, 1200);
   crit2 = new Criteria("max acreage", "acreage", 1, 3, 0, 3);
   crit3 = new Criteria("max sqft", "sq_foot", 1, 4300, 0, 4300);
   crit4 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   expr.expectedScore = 0.155;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   expr.addCriteria(crit4);
   addExperiment(expr);

   expr = new Experiment(dbMgr, 314);
   crit1 = new Criteria("min taxes", "taxes", 1, 0, 0, 5000);
   crit2 = new Criteria("max acreage", "acreage", 1, 3, 0, 3);
   crit3 = new Criteria("max sqft", "sq_foot", 1, 4300, 0, 4300);
   crit4 = new Criteria("near B", "distToB", 1, 0, 0, 40);
   expr.expectedScore = 0.12;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   expr.addCriteria(crit4);
   addExperiment(expr);

   expr = new Experiment(dbMgr, 315);
   crit1 = new Criteria("min price", "listing_price", 1, 0, 0, 1200);
   crit2 = new Criteria("max acreage", "acreage", 1, 3, 0, 3);
   crit3 = new Criteria("max sqft", "sq_foot", 1, 4300, 0, 4300);
   crit4 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   expr.expectedScore = 0.14;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   expr.addCriteria(crit4);
   addExperiment(expr);

   expr = new Experiment(dbMgr, 316);
   crit1 = new Criteria("min taxes", "taxes", 1, 0, 0, 5000);
   crit2 = new Criteria("max acreage", "acreage", 1, 3, 0, 3);
   crit3 = new Criteria("max sqft", "sq_foot", 1, 4300, 0, 4300);
   crit4 = new Criteria("near A", "distToA", 1, 0, 0, 40);
   expr.expectedScore = 0.138;

   expr.addCriteria(crit1);
   expr.addCriteria(crit2);
   expr.addCriteria(crit3);
   expr.addCriteria(crit4);
   addExperiment(expr);
  }
 

////////////////////  addExperiment /////////////////////////////

  public void addExperiment(Experiment newExp) {

//    experSet.addElement(newExp);

    Integer key = new Integer(newExp.getId());
    experSet.put(key, newExp);

    numExperiments++;
  }

/////////////////  choose Experiment Set ////////////////////

  public void chooseExpSet(int expSet) {

// Brygg & Anna are doing a quick hack for 

/*
    if (expSet < numExpSets && expSet >= 0) {
      activeExpSet = expSet;
    } else {
      dbg("chooseExpSet: bogus num " + expSet);
    }

    activeExpIdx = 0;
    activeExpMax = expLen[activeExpSet];

    int nExpNum = expSeq[activeExpSet][activeExpIdx];
*/

    try {
//      setCurrentExperiment(nExpNum);
      setCurrentExperiment(expSet);

    } catch (Exception e) {
      dbg("chooseExpSet exception: a bogus experiment was likely called");
    }
  }

//////////////////  next Experiment ///////////////////////////

  public int nextExperiment() {
    //currentExpNum++;
    activeExpIdx++;

    if (activeExpIdx > activeExpMax) {
      activeExpIdx = -1;

    } else {

      int nExpNum = expSeq[activeExpSet][activeExpIdx];
      setCurrentExperiment(nExpNum);
    }

    return activeExpIdx;
  }

////////////////////  setCurrentExperiment /////////////////////////////

  public void setCurrentExperiment(int whichExp) {

    currentExpNum = whichExp;
    getExperiment(whichExp);
  }

////////////////////  getExperiment /////////////////////////////

  public Experiment getCurrentExperiment() {
    return currentExp;
  }

////////////////////  getExperiment /////////////////////////////

  public Experiment getExperiment(int whichExp) {

    Integer key = new Integer(whichExp);

    currentExp = (Experiment) experSet.get(key);

    return currentExp;
  }

 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("ExperSet." + (dcnt++) + ": " + s);
  } 
}

//// END ////

