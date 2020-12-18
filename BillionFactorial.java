import org.optimizationBenchmarking.utils.math.functions.special.Gamma;
import org.optimizationBenchmarking.utils.math.functions.special.GammaLn;

import java.math.*;
import java.util.*;
import java.text.DecimalFormat;

class BillionGamma {

	
    
    
	public static void main(String[] args) {
		System.out.print("Enter value for factorial: ");
		Scanner input = new Scanner(System.in);
		double comparenumber;
        
		comparenumber=436117076640000000L;
        String comparison="the age of the universe in seconds";

		double value = input.nextInt();
		
		double logresult =  GammaLn.INSTANCE.computeAsDouble(value+1);

        System.out.println("Natural Log of " + value + "! is " + logresult);
        System.out.println();

        
        
        double comparelog=java.lang.Math.log(comparenumber); 
        
        System.out.println("Natural Log of " + comparison + "=" + comparenumber + " is: " + comparelog + "\n\n");
        
        double difference=comparelog-logresult;

        String status;
        double multiplier;
        if (difference > 0) {
        	   status="smaller";
               multiplier=comparelog/logresult;
        }
        else {
        	   status="bigger";
               multiplier=logresult/comparelog;
        }
        
        DecimalFormat decimalformat = new DecimalFormat("###,###,###,###,###,###,###,###");

        String friendlyvalue=decimalformat.format(multiplier);
        
        
        System.out.println("ln(Your Number " + value + "!)=" + logresult);
        System.out.println("Is a power of " + friendlyvalue + " " + status + " than (" + comparison + "=" + comparenumber + ")");
        System.out.println("Because ln(" + comparenumber + ")=" + comparelog + ".");

        
        
        
        
		//System.out.println(value + "! is " + factorial(value));
		//System.out.println("Digit count is " + count(factorial(value)));
	}

	static long count(BigInteger k){ //Count all digits
		double factor = Math.log(2)/Math.log(10);
		int count = (int)(factor*k.bitLength()+1);
		if(BigInteger.TEN.pow(count-1).compareTo(k)>0){
			return count-1;
		}
		return count;
	}
	public static BigInteger factorial(long n) {//compute factorial
		 BigInteger result = BigInteger.ONE;
		 for (int i = 1; i <= n; i++)
		 result = result.multiply(new BigInteger(i+""));

		return result;
		 }
}


	