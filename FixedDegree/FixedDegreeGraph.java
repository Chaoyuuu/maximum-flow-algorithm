import java.io.*;
import java.util.*;

public class FixedDegreeGraph {
    private final Random gen = new Random();
    private final StringBuffer bfr = new StringBuffer();
    private static final String NL = "\n";

    public static void main(String[] args) throws IOException {
        System.out.println("\n\n---------------------------------------------------");
        System.out.print("Enter the number of vertices in the graph: \t");
        int v = IOUtils.GetInt();

        System.out.print("Enter the number of edges leaving each node: \t");
        int e = IOUtils.GetInt();

        if (v < e) {
            System.out.println("\nFAIL!");
            System.out.println("The number of vertices must exceed the number of edges leaving each node.");
            return;
        }

        System.out.print("Enter minimum capacity: \t");
        int minCapacity = IOUtils.GetInt();

        System.out.print("Enter maximum capacity: \t");
        int maxCapacity = IOUtils.GetInt();

        if (minCapacity > maxCapacity) {
            System.out.println("\nFAIL!");
            System.out.println("Max must be greater than or equal to min.");
            return;
        }

        System.out.print("Enter the output file name: \t");
        String fileName = IOUtils.GetString() + ".txt";
        System.out.println("------------------- Generating File ------------------------");

        FixedDegreeGraph graph = new FixedDegreeGraph();
        graph.generate(v, e, minCapacity, maxCapacity);
        graph.toFile(fileName);
        System.out.println("\nDONE!");
    }

    /**
     * This method creates a 3 token representation of a graph.
     *
     * @param v   The number of vertices in the graph
     * @param e   The number of edges leaving each vertice
     * @param min The lowerbound on the capacity value of each edge
     * @param max The upperbound on the capacity value of each edge
     * @return A string buffer, each line contains 3 tokens corresponding
     * to a directed edge: the tail, the head, and the capacity.
     */
    public void generate(int v, int e, int min, int max) {
        int i;
        int j;
        int head;
        int c;
        SortedSet<Integer> s;

        //Add distinguished node s
        j = 1;
        s = new TreeSet<>();
        while (j <= e) {
            head = gen.nextInt(v) + 1;
            if (!s.contains(head)) {
                s.add(head);
                c = min + gen.nextInt(max - min + 1);
                bfr.append("s" + " v" + head + " " + c + NL);
                j++;
            }
        }

        //Add distinguished node t
        j = 1;
        s = new TreeSet<>();
        while (j <= e) {
            int tail = gen.nextInt(v) + 1;
            if (!s.contains(tail)) {
                s.add(tail);
                c = min + gen.nextInt(max - min + 1);
                bfr.append("v" + tail + " " + "t" + " " + c + NL);
                j++;
            }
        }

        //Add internal nodes
        for (i = 1; i <= v; i++) {
            s = new TreeSet<>();
            s.add(i);
            j = 1;
            while (j <= e) {
                head = gen.nextInt(v) + 1;
                if (!s.contains(head)) {
                    s.add(head);
                    c = min + gen.nextInt(max - min + 1);
                    bfr.append("v" + i + " v" + head + " " + c + NL);
                    j++;
                }
            }
        }
    }

    private void toFile(String fileName) {
        IOUtils.CreateFile("FixedDegree/" + fileName, bfr);
    }
}
