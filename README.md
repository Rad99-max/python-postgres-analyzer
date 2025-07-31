# python-postgres-analyzer
A Python script that connects to a  PostgreSQL database to generate a report on the longest films.

## How to Use
1.  Clone the repository:
    ```
    git clone https://github.com/Rad99-max/python-postgres-analyzer.git
    ```
2.  Navigate to the project directory:
    ```
    cd python-postgres-analyzer
    ```
3.  Create a `.env` file with your database credentials. See `.env.example` for reference.
4.  Install the required libraries:
    ```
    pip install -r requirements.txt
    ```
5.  Run the script:
    ```
    python save_CSV_interact_1.py --limit 5 --output report.csv
    ```