import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


np.random.seed(42)
# 1. M/M/1 QUEUE SIMULATION
def simulate_mm1(lambda_rate, mu_rate, num_requests=1000):

   
    inter_arrival_times = np.random.exponential(
        1.0 / lambda_rate,
        num_requests
    )
    # Calculate arrival times
    arrival_times = np.cumsum(inter_arrival_times)
    # Generate random service times
    service_times = np.random.exponential(
        1.0 / mu_rate,
        num_requests
    )
    # Create arrays
    start_times = np.zeros(num_requests)
    completion_times = np.zeros(num_requests)
    wait_times = np.zeros(num_requests)
    response_times = np.zeros(num_requests)
    # Process requests one by one
    for i in range(num_requests):

        if i == 0:
            start_times[i] = arrival_times[i]
        else:
            start_times[i] = max(
                arrival_times[i],
                completion_times[i - 1]
            )
        # Calculate waiting time
        wait_times[i] = (
            start_times[i] - arrival_times[i]
        )

        # Calculate completion time
        completion_times[i] = (
            start_times[i] + service_times[i]
        )

        # Calculate response time
        response_times[i] = (
            completion_times[i] - arrival_times[i]
        )

    # Store results in a DataFrame
    df = pd.DataFrame({
        "Request_ID": np.arange(1, num_requests + 1),
        "Arrival_Time_sec": arrival_times,
        "Service_Time_sec": service_times,
        "Wait_Time_sec": wait_times,
        "Response_Time_ms": response_times * 1000
    })

    return df

# 2. SIMULATION PARAMETERS
mu = 100                  # Service rate 
lambda_peak = 90          # Peak arrival rate
num_requests = 1000       # Number of requests

# 3. RUN SIMULATION
sim_df = simulate_mm1(
    lambda_peak,
    mu,
    num_requests
)

# 4. DISPLAY SIMULATION RESULTS
print("\nFirst 10 simulated requests:")
print(sim_df.head(10))

print("\nSimulation Summary:")
print("Average Waiting Time:",
      round(sim_df["Wait_Time_sec"].mean() * 1000, 2),
      "ms")

print("Average Response Time:",
      round(sim_df["Response_Time_ms"].mean(), 2),
      "ms")


# 5. SAVE SIMULATED DATA
sim_df.to_csv(
    "simulated_traffic_data.csv",
    index=False
)

print("\nSimulated data saved as:")
print("simulated_traffic_data.csv")


# 6. ANALYTICAL M/M/1 RESULTS
arrival_rates = [40, 70, 90, 98]

utilization = []
queue_sizes = []
response_times = []
throughput = []

for lam in arrival_rates:

    # Server utilization
    rho = lam / mu

    # Average number of requests waiting in queue
    Lq = (rho ** 2) / (1 - rho)

    # Average response time
    W = 1 / (mu - lam)

    utilization.append(rho * 100)
    queue_sizes.append(Lq)
    response_times.append(W * 1000)
    throughput.append(lam)


# 7. DISPLAY ANALYTICAL RESULTS
results_df = pd.DataFrame({
    "Arrival Rate (req/s)": arrival_rates,
    "Utilization (%)": utilization,
    "Average Queue Size": queue_sizes,
    "Average Response Time (ms)": response_times,
    "Theoretical Throughput (req/s)": throughput
})

print("\nAnalytical M/M/1 Results:")
print(results_df.round(2))



# 8. FIGURE 1 - RESPONSE TIME
arrival_labels = [
    "40 req/s",
    "70 req/s",
    "90 req/s",
    "98 req/s"
]

plt.figure(figsize=(8, 5))

bars = plt.bar(
    arrival_labels,
    response_times,color="skyblue",
    width=0.5
)

plt.bar_label(
    bars,
    labels=[f"{v:.2f} ms" for v in response_times],
    padding=3
)
    


plt.title(
    "Average Response Time by Arrival Rate"
)

plt.xlabel("Arrival Rate")

plt.ylabel(
    "Average Response Time (ms)"
)

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.5
)

plt.tight_layout()

plt.savefig(
    "Figure_1_Response_Time.png",
    dpi=300
)

plt.show()



# 9. FIGURE 2 - QUEUE SIZE
utilization_labels = [
    "40%",
    "70%",
    "90%",
    "98%"
]

plt.figure(figsize=(8, 5))

bars = plt.bar(
    utilization_labels,
    queue_sizes,
    color="lightgreen",
        width=0.5
)

plt.bar_label(
    bars,
    labels=[f"{v:.2f}" for v in queue_sizes],
    padding=3
)
    


plt.title(
    "Average Queue Size by Server Utilization"
)

plt.xlabel(
    "Server Utilization"
)

plt.ylabel(
    "Average Queue Size (requests)"
)

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.5
)

plt.tight_layout()

plt.savefig(
    "Figure_2_Queue_Size.png",
    dpi=300
)

plt.show()



# 10. M/M/2 CALCULATION
lambda_mm2 = 90
servers = 2
mu_per_server = 100

# Utilization per server
rho_mm2 = lambda_mm2 / (
    servers * mu_per_server
)

# Offered load
a = lambda_mm2 / mu_per_server

# Probability of zero customers in the system
P0 = 1 / (
    1
    + a
    + (
        (a ** 2)
        / (2 * (1 - rho_mm2))
    )
)

# Probability 
P_wait = (
    (a ** 2)
    / (2 * (1 - rho_mm2))
) * P0

# Average waiting time in queue
Wq_mm2 = P_wait / (
    servers * mu_per_server - lambda_mm2
)

# Average response time
W_mm2 = Wq_mm2 + (
    1 / mu_per_server
)

# Convert to milliseconds
response_mm2_ms = W_mm2 * 1000


print("\nM/M/2 Results:")
print("Number of Servers:", servers)
print("Arrival Rate:", lambda_mm2, "req/s")
print("Service Rate per Server:",
      mu_per_server, "req/s")
print("Utilization per Server:",
      round(rho_mm2 * 100, 2), "%")
print("Probability of Waiting:",
      round(P_wait, 4))
print("Average Waiting Time:",
      round(Wq_mm2 * 1000, 2), "ms")
print("Average Response Time:",
      round(response_mm2_ms, 2), "ms")



# 11. FIGURE 3 - M/M/1 VS M/M/2
models = [
    "M/M/1",
    "M/M/2"
]

# Calculate M/M/1 response time at 90 requests/second
mm1_lambda = 90
mm1_mu = 100

mm1_response = 1 / (mm1_mu - mm1_lambda)

# Convert seconds to milliseconds
mm1_response_ms = mm1_response * 1000

model_response_times = [
    mm1_response_ms,
    response_mm2_ms
]

plt.figure(figsize=(8, 5))

bars = plt.bar(
    models,
    model_response_times,
    color="salmon",
    width=0.5
)

plt.bar_label(
    bars,
    labels=[f"{v:.2f} ms" for v in model_response_times],
    padding=3
)
    

plt.title(
    "M/M/1 and M/M/2 Response Time Comparison"
)

plt.xlabel(
    "Queueing Model"
)

plt.ylabel(
    "Average Response Time (ms)"
)

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.5
)

plt.tight_layout()

plt.savefig(
    "Figure_3_MM1_vs_MM2.png",
    dpi=300
)

plt.show()



# 12. PERFORMANCE IMPROVEMENT


mm1_response = 100

improvement = (
    (mm1_response - response_mm2_ms)
    / mm1_response
) * 100

print("\nPerformance Improvement:")
print(
    "Response Time Reduction:",
    round(improvement, 2),
    "%"
)

# 13. COMPLETION MESSAGE

print("\n======================================")
print("Simulation completed successfully!")
print("CSV data and graphs have been generated.")
print("======================================")