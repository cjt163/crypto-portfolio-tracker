using CSV
using DataFrames
using MLJ
using MLJLinearModels
using Statistics

# Get script directory and build absolute paths
script_dir = @__DIR__
project_dir = dirname(script_dir)
data_dir = joinpath(project_dir, "data")

# Load LinearRegressor model once
LinearRegressor = @load LinearRegressor pkg=MLJLinearModels

# List of coins to forecast
coins = ["BTC", "ETH", "SOL", "XRP"]

# Process each coin
for coin in coins
    println("\nForecasting $coin...")

    # Load preprocessed data
    input_file = joinpath(data_dir, "$(coin)_preprocessed.csv")
    df = CSV.read(input_file, DataFrame)

    # Split into features (X) and target (y)
    X = select(df, [:lag1, :lag2, :lag3])
    y = df.price

    # Split into train (80%) and test (20%)
    n = nrow(df)
    train_size = floor(Int, 0.8 * n)
    X_train = X[1:train_size, :]
    y_train = y[1:train_size]
    X_test = X[train_size+1:end, :]
    y_test = y[train_size+1:end]

    # Create and train the model
    model = LinearRegressor()
    mach = machine(model, X_train, y_train)
    fit!(mach, verbosity=0)

    # Predict on test set and calculate MAE
    y_pred = predict(mach, X_test)
    mae = mean(abs.(y_pred .- y_test))
    println("[OK] Model trained with MAE: $mae")

    # Forecast next 7 days
    last_prices = df.price[end-2:end]
    forecasts = Float64[]

    for day in 1:7
        features = DataFrame(lag1=last_prices[3], lag2=last_prices[2], lag3=last_prices[1])
        pred = predict(mach, features)[1]
        push!(forecasts, pred)
        last_prices = [last_prices[2], last_prices[3], pred]
    end

    # Save forecast to CSV
    output_file = joinpath(data_dir, "$(coin)_forecast.csv")
    forecast_df = DataFrame(day=1:7, predicted_price=forecasts)
    CSV.write(output_file, forecast_df)

    println("[OK] 7-day forecast saved to $(coin)_forecast.csv")
end

println("\nAll forecasts generated successfully!")
