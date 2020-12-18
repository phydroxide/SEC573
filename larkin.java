import jmathlib.*;
import java.math.*;
import java.util.*;


class Factorial {

	public static void main(String[] args) {
		System.out.print("Enter value for factorial: ");
		Scanner input = new Scanner(System.in);
		int value = input.nextInt();
		System.out.println(value + "! is " + factorial(value));

		System.out.println("Digit count is " + count(factorial(value)));
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
