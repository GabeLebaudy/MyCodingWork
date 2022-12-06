import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.lang.Math;
public class FileObjectData {
	private ArrayList<BatchObjectData> batchObjects;
    private static String FileHeaderOpening = "101"; //Always 101
    private static String OriginatorRoutingNumber = "031908485"; // Originator's Routing Number
    private static String TaxID = "510345302"; // Institution Sending the ACH File.(Routing Number)
    private static String FileIDModifier = "A"; //Usually always A, but needs to change if a new identical file is created.
    private static String ACHFormat = "094101"; //Always this number
    private static String bankReceiving = "Bryn Mawr Trust Company"; //Bank we send the file to.
    private static String companyName = "Fairmount Automation"; //Bank that sends 
    private static String ReferenceCode = "REF00001";
    //End of Header Data: Start of Trailer Data
    private static String FileTrailerOpening = "9"; //Always 9
    private int blockCount; //Number of "blocks" (sets of 10 of records) I.e. 1 block = 10 records
    private int totalEntries = 0; //Will be the length of the batchObject arraylist. 
    private int hashCount = 0; //Number of entry hashes of the entire file.
    private static int totalDebit = 0; //How much will be taken from the company(Always only credit transactions)
    private int totalCredit = 0;
    public FileObjectData() {
		batchObjects = new ArrayList<BatchObjectData>();
	} 
 
	public void addBatchData(BatchObjectData BatchObject) {
		batchObjects.add(BatchObject);	
	}
	
	public String prepareAchString()
	{
		String FileHeaderRecord = "";
		SimpleDateFormat ObjDate = new SimpleDateFormat("yyMMddHHmm");
		Date CurrentDate = new Date();
		FileHeaderRecord += FileHeaderOpening;
		FileHeaderRecord += String.format("%10s", OriginatorRoutingNumber);
		FileHeaderRecord += String.format("%10s", TaxID);
		FileHeaderRecord += ObjDate.format(CurrentDate);
		FileHeaderRecord += FileIDModifier;
		FileHeaderRecord += ACHFormat;
		FileHeaderRecord += String.format("%23s", bankReceiving);
		FileHeaderRecord += String.format("%-23s", companyName);
		FileHeaderRecord += ReferenceCode;
		FileHeaderRecord += System.lineSeparator();	
		for (int i=0; i < batchObjects.size(); i++) {
			FileHeaderRecord += batchObjects.get(i).prepareAchString();
		}
		FileHeaderRecord += this.prepareTrailerRecord();
		int remainder = getRecordCount() % 10;
		if(remainder == 0) {
			//skip
		} else {
			for(int i = 0; i < 10 - remainder;i++) {
				
				FileHeaderRecord += System.lineSeparator() + fillFile();
			} 
		}
		return FileHeaderRecord;
	}
	public String prepareTrailerRecord () {
		String trailerRecord = "";
		trailerRecord += FileTrailerOpening;
		trailerRecord += String.format("%06d", batchObjects.size());
		blockCount = getBlockCount();
		trailerRecord += String.format("%06d", this.blockCount);
		for(int i = 0;i < batchObjects.size();i++) {
			totalEntries += batchObjects.get(i).getRecordCount() - 2;
		}
		trailerRecord += String.format("%08d", totalEntries);
		for(int i = 0;i < batchObjects.size();i++) {
			hashCount += batchObjects.get(i).getBatchHashCount();
		}
		trailerRecord += String.format("%010d", hashCount);
		trailerRecord += String.format("%012d", totalDebit);
		for(int i = 0;i < batchObjects.size();i++) {
			totalCredit += batchObjects.get(i).getCreditAmount();
		}
		trailerRecord += String.format("%012d", totalCredit);
		return trailerRecord;
		
	}
	private int getRecordCount() {
		int recordCount = 2;
		for(int i = 0;i < this.batchObjects.size(); i ++) {
			recordCount += batchObjects.get(i).getRecordCount();
		}
		return recordCount;
	}
	public int getBlockCount() {
		return (int)(Math.ceil((double)(this.getRecordCount()) / 10.0));
	}
	private String fillFile() {
		String padding = "9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999";
		return padding;
	} 
}








