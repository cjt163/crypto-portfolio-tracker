using CSV
using DataFrames
using Statistics

# Get script directory and build absolute paths
script_dir = @__DIR__
project_dir = dirname(script_dir)
data_dir = joinpath(project_dir, "data")

# List of coins to process
coins = ["BTC", "ETH", "SOL", "XRP"]

# Process each coin
for coin in coins
    println("Processing $coin...")

    # Input and output file paths
    input_file = joinpath(data_dir, "$(coin)_history.csv")
    output_file = joinpath(data_dir, "$(coin)_preprocessed.csv")

    # Load historical data
    df = CSV.read(input_file, DataFrame)

    # Sort by date (oldest first)
    sort!(df, :date)

    # Create lagged features
    df.lag1 = [missing; df.price[1:end-1]]
    df.lag2 = [missing; missing; df.price[1:end-2]]
    df.lag3 = [missing; missing; missing; df.price[1:end-3]]

    # Drop rows with missing values (first 3 rows)
    df_clean = dropmissing(df)

    # Save preprocessed data
    CSV.write(output_file, df_clean)

    # Print confirmation
    n_rows = nrow(df_clean)
    println("[OK] Preprocessed $n_rows rows of $coin data")
    println("[OK] Saved to $(coin)_preprocessed.csv")
    println()
end

println("All coins processed successfully!")
