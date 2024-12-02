import java.io.*;

public class IOUtils {
    public static String GetString() throws IOException {
        BufferedReader stringIn = new BufferedReader(new InputStreamReader(System.in));
        return stringIn.readLine();
    }

    public static int GetInt() throws IOException {
        String aux = GetString();
        return Integer.parseInt(aux);
    }

    public static double GetReal() throws IOException {
        String aux = GetString();
        Double d = new Double(aux);
        return d.doubleValue();
    }

    public static void CreateFile(String filePath, StringBuffer bfr) {
        try {
            BufferedWriter fout = new BufferedWriter(new FileWriter(filePath));
            fout.write(bfr.toString());
            fout.close();
        } catch (Exception e) {
            System.out.println(e.getMessage());
            System.out.println("Error saving file.");
            System.out.println("Please check file paths and restart this program.");
            System.exit(1);
        }
    }

    public static void main(String[] args) throws IOException {
        System.out.println(GetInt());
    }
}
