import java.io.*;

public class BipartiteGraph {
    public static void main(String[] args) throws Exception {
        int n, m, maxCapacity, i, j, minCapacity;
        double maxProbability, value, x;
        System.out.println("\n\n---------------------------------------------------");
        System.out.print("Enter number of nodes on the source side: ");
        n = IOUtils.GetInt();

        System.out.print("Enter number of nodes on the sink side: ");
        m = IOUtils.GetInt();

        System.out.print("Enter max probability: ");
        maxProbability = IOUtils.GetReal();

        if (maxProbability > 1) {
            System.out.println("Max probability should be less than or equal to 1");
            return;
        }

        System.out.print("Enter minimum capacity: ");
        minCapacity = IOUtils.GetInt();

        System.out.print("Enter maximum capacity: ");
        maxCapacity = IOUtils.GetInt();

        String directory = System.getProperty("user.dir");
        System.out.print("Enter the output file name: ");
        String fileName = IOUtils.GetString() + ".txt";
        System.out.println("------------------- Generating Graph ------------------------");

        try {
            PrintWriter outFile = new PrintWriter(new FileWriter(new File("Bipartite/", fileName)));

            double[][] edge = new double[n][m];
            for (i = 0; i < n; i++) {
                for (j = 0; j < m; j++) {
                    value = Math.random();
                    if (value <= maxProbability)
                        edge[i][j] = value;
                    else
                        edge[i][j] = 0;
                }
            }

            System.out.println("-----------------------------------------");
            System.out.println("Source\tSink\tCapacity");
            System.out.println("-----------------------------------------");

            //computing the edges out of source
            for (i = 0; i < n; i++) {
                x = Math.random();
                //Compute a capacity in range of [minCapacity, maxCapacity]
                value = Math.floor(minCapacity + (x * (maxCapacity - minCapacity + 1)));
                System.out.println("s" + "\tl" + (i + 1) + "\t" + (int) value);
                outFile.println("s" + "\tv" + (i + 1) + "\t" + (int) value);
            }
            for (i = 0; i < n; i++) {
                for (j = 0; j < m; j++) {
                    if (edge[i][j] > 0) {
                        edge[i][j] = Math.floor(minCapacity + (edge[i][j] * (maxCapacity - minCapacity + 1)));
                        System.out.println("l" + (i + 1) + "\tr" + (j + 1) + "\t" + (int) edge[i][j]);
                        //computing for the vertices between source and sink and writing them to the output file
                        outFile.println("v" + (i + 1) + "\tv" + (j + 1 + n) + "\t" + (int) edge[i][j]);
                    }
                }
            }
            //computing the edges into the sink
            for (j = 0; j < m; j++) {
                x = Math.random();
                value = Math.floor(minCapacity + (x * (maxCapacity - minCapacity + 1)));
                System.out.println("r" + (j + 1) + "\t" + "t" + "\t" + (int) value);
                outFile.println("v" + (j + 1 + n) + "\t" + "t" + "\t" + (int) value);
            }

            System.out.println("\n\nOutput is created at: \t" + directory + "\\" + fileName);
            outFile.close();
        } catch (Exception ex) {
            System.out.println(ex);
        }
    }
}