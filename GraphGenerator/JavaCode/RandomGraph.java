import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Random;


public class RandomGraph {
    private final int vertices;
    private final int dense;
    private final int minCapacity;
    private final int maxCapacity;
    private final Random random = new Random();

    private static RandomGraph DefaultRandomGraph() {
        return new RandomGraph(500, 80, 1, 2500);
    }

    public RandomGraph(int vertices, int dense, int minCapacity, int maxCapacity) {
        this.vertices = vertices;
        this.dense = dense;
        this.minCapacity = minCapacity;
        this.maxCapacity = maxCapacity;
    }

    public static void main(String[] args) throws IOException {
        RandomGraph graph;

        System.out.println("\n\n---------------------------------------------------");
        System.out.print("Use default value? (0: false, 1: true)\n (Default setting: #row: 3, #col: 4, const capacity: 1): \t");
        if (IOUtils.GetInt() == 1) {
            graph = DefaultRandomGraph();
        } else {
            System.out.print("Enter the number of vertices: \t");
            int v = IOUtils.GetInt();

            System.out.print("Enter the value of dense: \t");
            int d = IOUtils.GetInt();

            System.out.print("Enter minimum capacity: \t");
            int minCapacity = IOUtils.GetInt();

            System.out.print("Enter maximum capacity: \t");
            int maxCapacity = IOUtils.GetInt();

            if (minCapacity > maxCapacity) {
                System.out.println("\nFAIL!");
                System.out.println("Max must be greater than or equal to min.");
            }

            graph = new RandomGraph(v, d, minCapacity, maxCapacity);
        }

        System.out.print("Enter the output file name: \t");
        String fileName = IOUtils.GetString() + ".txt";
        System.out.println("------------------- Generating Graph ------------------------");

        graph.generate(fileName);
        System.out.println("\nDONE!");
    }


    private void generate(String fileName) {
        int[][] Graph = new int[vertices][vertices];

        for (int n = 0; n < vertices; n++) {
            for (int m = n + 1; m < vertices; m++) {
                int randomInt = (random.nextInt((maxCapacity - minCapacity + 1)) + minCapacity);

                int k = (int) (1000.0 * Math.random() / 10.0);
                int b = (k < dense) ? 1 : 0;
                if (b == 0) {
                    Graph[n][m] = Graph[m][n] = b;
                } else {
                    Graph[n][m] = Graph[m][n] = randomInt;
                }
            }
        }

        try {
            File outputfile = new File("Random/", fileName);
            PrintWriter output = new PrintWriter(new FileWriter(outputfile));

            for (int x = 0; x < Graph.length; x++) {
                if (x == 0) {
                    for (int y = 0; y < Graph[x].length; y++) {
                        String value = String.valueOf(Graph[x][y]);
                        if (y != 0) {
                            if (!value.equals("0")) {
                                output.print("s v" + y + " " + value + "\r\n");
                            }
                        }
                    }
                } else {
                    if (x == Graph.length - 1) {
                        for (int y = 0; y < Graph[x].length; y++) {
                            String value = String.valueOf(Graph[x][y]);
                            if (y != 0) {
                                if (!value.equals("0")) {
                                    output.print("v" + y + " t " + value + "\r\n");
                                }
                            }
                        }
                    } else {
                        for (int y = 0; y < Graph[x].length; y++) {
                            String value = String.valueOf(Graph[x][y]);
                            if (y != 0) {
                                if (!value.equals("0")) {
                                    output.print("v" + x + " v" + y + " " + value + "\r\n");
                                }
                            }
                        }
                    }
                }

            }
            output.close();
        } catch (IOException e) {
            System.err.println("Error opening file" + e);
        }
    }
}
