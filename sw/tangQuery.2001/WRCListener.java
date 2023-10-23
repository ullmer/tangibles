// Event interface to DbThread
// Brygg Ullmer, MIT Media Lab
// Begun April 28, 2001

// @author  Brygg Ullmer
// @version v0.1

public interface WRCListener {

  public void processTokEntrance(int rackId, int cellId, int tokId);
  public void processTokExit    (int rackId, int cellId, int tokId);

  public void processTokRot (int rackId, int cellId, int val);
  public void processAdjacencies (int rackId, String adjStr);

}

//// END ////

