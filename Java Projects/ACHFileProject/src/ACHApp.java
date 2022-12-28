import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
public class ACHApp {
	public static void main(String[] args) throws Exception {
		boolean isCompany = true;
		FileObjectData ObjCreate = new FileObjectData();
		isCompany = setCompanyStatus(false);
		String formattedInvoiceDate = formatInvoiceDate("2021", "12", "30");
		try {
		BatchObjectData batchObject1 = new BatchObjectData("200", isCompany, "ReferenceX", formattedInvoiceDate);
		EntryObjectData entryObject1 = new EntryObjectData("031908485", "9324372", 1.33, "Andres Lebaudy");
		batchObject1.addEntryData(entryObject1);
		BatchObjectData batchObject2 = new BatchObjectData("200", isCompany, "ReferenceY", formattedInvoiceDate);
		EntryObjectData entryObject2 = new EntryObjectData("031908485", "9324372", 2.67, "Andres Lebaudy");
		batchObject2.addEntryData(entryObject2);
		BatchObjectData batchObject3 = new BatchObjectData("200", isCompany, "ReferenceZ", formattedInvoiceDate);
		EntryObjectData entryObject3 = new EntryObjectData("031908485", "9324372", 7.0, "Andres Lebaudy");
		batchObject3.addEntryData(entryObject3);
		ObjCreate.addBatchData(batchObject1);
		ObjCreate.addBatchData(batchObject2);
		ObjCreate.addBatchData(batchObject3);
		String ACHOutput = ObjCreate.prepareAchString();
		System.out.println(ACHOutput);
		try {
			File achFile = new File("C:\\Users\\Gabe\\eclipse-workspace\\ACHFileProject\\achExample.txt");
			if(!achFile.exists()) {
				achFile.createNewFile();
			}
			PrintWriter fileWrite = new PrintWriter(achFile);
			fileWrite.println(ACHOutput);
			fileWrite.close();
		}catch (IOException e) {
			e.printStackTrace();
		}
		} catch (Exception e) {
			System.out.print("You have data that doesn't fit ACH field requirements");
			System.out.print(e);
		}
	}
	private static boolean setCompanyStatus(boolean status) {
		return status;
	}
	private static String formatInvoiceDate(String year, String month, String day) {
		String formattedDate = "";
		formattedDate += year.substring(2, 4);
		formattedDate += month;
		formattedDate += day;
		return formattedDate;
	}
}

