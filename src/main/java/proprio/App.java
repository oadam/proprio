package proprio;

import org.flywaydb.core.Flyway;

/**
 * The main app of the application.
 *
 */
public final class App {
    /** Private to prevent instanciation. */
    private App() {
    }

    /**
     * The main method of the app.
     *
     * @param args
     *            Command line arguments
     */
    public static void main(final String[] args) {
        // Create the Flyway instance
        Flyway flyway = new Flyway();

        // Point it to the database
        flyway.setDataSource("jdbc:sqlite:target/proprio.db", "sa", null);

        // Start the migration
        flyway.migrate();

        System.out.println("Hello World!");
    }
}
