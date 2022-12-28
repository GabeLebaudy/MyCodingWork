import java.util.ArrayList;
import java.util.Date;
import java.util.Calendar;
import java.text.SimpleDateFormat;
public class BatchObjectData {
	private ArrayList<EntryObjectData> entryObjects;
	private static String batchHeaderOpening = "5";
	private String serviceClassCode = "200";// 200 if Mixed debit and credit, 220 if only credit, 225 Only debit.
	private static String companyName = "Fairmount Automa";
	private static String batchHeaderPadding = "                    ";
	private static String companyID = "510345302";
	private String paymentType = "CCD"; //Add a Boolean to switch between PPD or CCD based on batch.
	private String batchDescription = "ReferenceX"; //Change the two invoice variables to what you want as long as it doesnt exceed character limit.
	private String invoiceDate = ""; 
	private String paymentDate = ""; 
	private String julian = "   ";
	private String indicator = "1";
	private static String originatingRoutingNumber = "03190848";
	private static int batchNumber = 0;
	//End of batch header data: Start of batch Trailer Data
	private static String batchOpening = "8";
	private int entryHashCount = 0;
	private static int totalDebitAmount = 0; //Most of the time it will be 0
	private String authentication = "                   "; //8-digit code. Most likely used to verify our authority to send the money.
	private String reserved = "      "; //6 Blanks
	public void addEntryData(EntryObjectData EntryObject) {
		entryObjects.add(EntryObject);	
	}

	public BatchObjectData(String serviceClassCode, boolean isCompany, String batchDescription, String invoiceCreationDate)throws Exception {
		entryObjects = new ArrayList<EntryObjectData>();
		this.serviceClassCode = serviceClassCode;
		if(isCompany == true) {
			this.paymentType = "CCD";
		} else {
			this.paymentType = "PPD";
		}
		this.batchDescription = batchDescription;
		if(invoiceCreationDate.length() != 6) {
			throw new Exception("Date must be formatted yymmdd");
		}
		this.invoiceDate = invoiceCreationDate;
	}
	
	public String prepareAchString()
	{
		String BatchHeaderRecord = "";
		BatchHeaderRecord += batchHeaderOpening;
		BatchHeaderRecord += serviceClassCode;
		BatchHeaderRecord += companyName;
		BatchHeaderRecord += batchHeaderPadding;
		BatchHeaderRecord += String.format("%10s", companyID);
		BatchHeaderRecord += paymentType;
		if(batchDescription.length() > 10) {
			batchDescription = cutBatchDescription(batchDescription);
		}
		BatchHeaderRecord += String.format("%10s", batchDescription);
		BatchHeaderRecord += String.format("%6s", invoiceDate);
		Calendar calendar = Calendar.getInstance();
		calendar.add(Calendar.DAY_OF_YEAR, 2);
		Date tomorrow = calendar.getTime();
		SimpleDateFormat format = new SimpleDateFormat("yyMMdd");
		paymentDate = format.format(tomorrow);
		BatchHeaderRecord += String.format("%6s", paymentDate);
		BatchHeaderRecord += julian;
		BatchHeaderRecord += indicator;
		BatchHeaderRecord += originatingRoutingNumber;
		batchNumber++;
		BatchHeaderRecord += String.format("%07d", batchNumber);
		BatchHeaderRecord += System.lineSeparator();
		for(int i = 0;i < entryObjects.size();i++) { 
			BatchHeaderRecord += entryObjects.get(i).prepareAchString();
		}
		BatchHeaderRecord += this.prepareTrailerString();
		BatchHeaderRecord += System.lineSeparator();
		return(BatchHeaderRecord);
	}
	public String prepareTrailerString() {
		String batchTrailer = "";
		batchTrailer += batchOpening;
		batchTrailer += String.format("%3s", serviceClassCode);
		batchTrailer += String.format("%06d", entryObjects.size());
		for(int i = 0;i < entryObjects.size();i++) {
			entryHashCount += convertRouting(entryObjects.get(i).getRoutingNumber());
		}
		batchTrailer += String.format("%010d", entryHashCount);
		batchTrailer += String.format("%012d", totalDebitAmount);
		batchTrailer += String.format("%012d", getCreditAmount());
		batchTrailer += String.format("%10s", companyID);
		batchTrailer += authentication;
		batchTrailer += reserved;
		batchTrailer += originatingRoutingNumber;
		batchTrailer += String.format("%07d", batchNumber);
		return batchTrailer;
	}
	public int getRecordCount() {
		return entryObjects.size() + 2;
	}
	public int getCreditAmount() {
		int totalPayment = 0;
		for(int i = 0;i < entryObjects.size();i++) {
			totalPayment += entryObjects.get(i).getPayment();
		}
		return totalPayment;
	}
	private int convertRouting(String routingNumber) {
		int tempSum = 0;
		String cutNumber = routingNumber.substring(0, 8);
		tempSum = Integer.valueOf(cutNumber);
		return tempSum;
	}
	public int getBatchHashCount() {
		return entryHashCount;
	}
	public int getOriginatingRoutingNumber() {
		int tempRoutingNumber = 2 * Integer.valueOf(originatingRoutingNumber);
		return tempRoutingNumber;
	}
	private String cutBatchDescription(String description) {
		String tempDescription = description.substring(0, 10);
		return tempDescription;
	}
}
