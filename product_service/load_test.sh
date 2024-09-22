# Define the endpoint
ENDPOINT="http://127.0.0.1:8000/api/users/login/?profile"

# Perform the load test for each username
for username in "frusha12334234"; do
  # Create a temporary JSON payload file
  echo "{\"username\": \"$username\", \"password\": \"password123\"}" > post_data.json

  # Run Apache Benchmark
  ab -n 1000 -c 100 -s 60 -p post_data.json -T application/json "$ENDPOINT"
done

# Remove the temporary payload file
rm -f post_data.json