import java.io.*;
import java.util.Random;

public class MeshGenerator {
    private final int rows;
    private final int cols;
    private final int mapCap;
    private final boolean isConstCap;
    private final StringBuffer bfr = new StringBuffer();
    private final Random rand = new Random();

    private static MeshGenerator defaultMeshGenerator() {
        return new MeshGenerator(3, 4, 1, true);
    }

    public MeshGenerator(int rows, int cols, int maxCapacity, boolean isConstCap) {
        this.rows = rows;
        this.cols = cols;
        this.mapCap = maxCapacity;
        this.isConstCap = isConstCap;
    }

    public void generate() {
        // the s to first column links
        for (int i = 1; i <= rows; i++) {
            bfr.append(String.format("s v%d %d\n", getNodeId(i, 1), getCapacity())); // (%d,1)
        }

        // left to right links across the rows
        for (int j = 1; j <= cols - 1; j++) {
            for (int i = 1; i <= rows; i++) {
                bfr.append(String.format("v%d v%d %d\n",  getNodeId(i, j), getNodeId(i, j + 1), getCapacity()));
            }
        }

        // two-way top to bottom links on the columns
        for (int j = 1; j <= cols; j++) {
            for (int i = 1; i <= rows - 1; i++) {
                bfr.append(String.format("v%d v%d %d\n", getNodeId(i, j), getNodeId(i + 1, j), getCapacity()));
                bfr.append(String.format("v%d v%d %d\n", getNodeId(i + 1, j), getNodeId(i, j), getCapacity()));
            }
        }

        // last column to t links
        for (int i = 1; i <= rows; i++) {
            bfr.append(String.format("v%d t %d\n", getNodeId(i, cols), getCapacity()));
        }
    }

    private int getCapacity() {
        return isConstCap ? mapCap : rand.nextInt(mapCap) + 1;
    }

    private int getNodeId(int x, int y) {
        return (x - 1) * cols + y;
    }

    private void toFile(String fileName) {
        IOUtils.CreateFile("Mesh/" + fileName, this.bfr);
    }

    public static void main(String[] args) throws IOException {
        MeshGenerator mesh;
        System.out.println("\n\n---------------------------------------------------");
        System.out.print("Use default value? (0: false, 1: true)\n (Default setting: #row: 3, #col: 4, const capacity: 1): \t");
        if (IOUtils.GetInt() == 1) {
            mesh = defaultMeshGenerator();
        } else {
            System.out.print("Enter the number of rows: \t");
            int m = IOUtils.GetInt();

            System.out.print("Enter the number of columns: \t");
            int n = IOUtils.GetInt();

            System.out.print("Enter maximum capacity: \t");
            int capacity = IOUtils.GetInt();

            System.out.print("Is the capacity be constant (0: false, 1: true) : \t");
            boolean isConstCap = IOUtils.GetInt() == 1;

            mesh = new MeshGenerator(m, n, capacity, isConstCap);
        }

        System.out.print("Enter the output file name: \t");
        String fileName = IOUtils.GetString() + ".txt";
        System.out.println("------------------- Generating Graph ------------------------");

        mesh.generate();
        mesh.toFile(fileName);
        System.out.println("\nDONE!");
    }
}
