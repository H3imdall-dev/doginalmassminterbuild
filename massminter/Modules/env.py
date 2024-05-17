import os

def update_env_file():
    # Define the path to the .env file
    env_file_path = os.path.expanduser("~/Desktop/mass minter/.env")
    
    # Read the existing .env file content
    with open(env_file_path, "r") as env_file:
        lines = env_file.readlines()
    
    # Prompt the user for the new values
    new_ip = input("Enter the new NODE RPC IP address: ")
    rpc_user = input("Enter your RPC username: ")
    rpc_pass = input("Enter your RPC password: ")
    
    # Loop until a valid fee is entered
    while True:
        try:
            fee_per_kb = int(input("Enter the fee per kb (minimum 10000000): "))
            if fee_per_kb < 10000000:
                raise ValueError("Must be 10m Sats minimum")
            break
        except ValueError as e:
            print(e)
    
    # Update the specific lines in the .env content
    new_lines = []
    for line in lines:
        if line.startswith("NODE_RPC_URL="):
            parts = line.split("//")
            prefix = parts[0] + "//"
            suffix = parts[1].split(":", 1)[1]
            new_line = f"{prefix}{new_ip}:{suffix}\n"
            new_lines.append(new_line)
        elif line.startswith("NODE_RPC_USER="):
            new_lines.append(f"NODE_RPC_USER={rpc_user}\n")
        elif line.startswith("NODE_RPC_PASS="):
            new_lines.append(f"NODE_RPC_PASS={rpc_pass}\n")
        elif line.startswith("FEE_PER_KB="):
            new_lines.append(f"FEE_PER_KB={fee_per_kb}\n")
        else:
            new_lines.append(line)
    
    # Write the updated content back to the .env file without extra newlines
    with open(env_file_path, "w") as env_file:
        for line in new_lines:
            env_file.write(line.strip() + "\n")
    
    print("The .env file has been updated successfully.")

# Run the update function
if __name__ == "__main__":
    update_env_file()
