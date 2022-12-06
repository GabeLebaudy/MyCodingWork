
public class EntryObjectData {
	private static String entryRecordOpening = "6";
	private static String entryTransactionCode = "22"; //Different Numbers identify the type of transaction that will take place in the entry record.
	private String RoutingNumber; //Recipients Routing Number 
	private String AccountNumber; //Recipients Account Number
	private int payment; 
	private String IdNumber = "111-22-3333"; //SSN Goes here
	private String receiverName;
	private String addendaIndicator = "0";
	private static String originatingRoutingNumber = "03190848";
	private static int traceNumber = 1;
	public EntryObjectData(String routing, String AccountN, double PaymentAmt, String receiver)throws Exception{
		if(routing.length() != 9) {
			throw new Exception("Your routing number is too long");
		}
		RoutingNumber = routing;
		if(AccountN.length() >= 18) {
			throw new Exception("Your account number is too long");
		}
		this.AccountNumber = AccountN;
		this.payment = (int)(PaymentAmt * 100);
		this.receiverName = receiver;
	}

	public String prepareAchString() {
		String entryRecord = "";
		entryRecord += entryRecordOpening;
		entryRecord += entryTransactionCode;
		entryRecord += String.format("%9s", this.RoutingNumber);
		entryRecord += String.format("%-17s", this.AccountNumber);
		entryRecord += String.format("%010d", this.payment);
		entryRecord += String.format("%-15s", IdNumber);
		if(receiverName.length() > 22) {
			receiverName = cutReceiverName(receiverName);
		}
		entryRecord += String.format("%-22s", this.receiverName);
		entryRecord += "  ";
		entryRecord += addendaIndicator;
		entryRecord += originatingRoutingNumber;
		entryRecord += String.format("%07d", traceNumber);
		traceNumber++;
		entryRecord += System.lineSeparator();
		return (entryRecord);
	}
	public int getPayment() {
		return this.payment;
	}
	public String getRoutingNumber() {
		return this.RoutingNumber;
	}
	private String cutReceiverName(String name) {
		String tempName = name.substring(0, 22);
		return tempName;
	}
	
}
