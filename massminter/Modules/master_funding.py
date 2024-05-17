import os
import subprocess
import time
import json

def run_command_in_terminal(command, cwd):
    subprocess.run(["gnome-terminal", "--", "bash", "-c", f"cd '{cwd}' && {command} && exec bash"])

def create_master_wallet():
    # Define the paths
    main_directory = os.path.expanduser("~/Desktop/mass minter")
    template_folder = os.path.join(main_directory, "minter")
    master_wallet_folder = os.path.join(main_directory, "master wallet")
    env_file_path = os.path.join(main_directory, ".env")
    main_wallet_info_path = os.path.join(main_directory, "wallet_info.txt")
    master_wallet_info_path = os.path.join(main_directory, "master_wallet.txt")
    
    # Clone the template folder to create the master wallet folder
    subprocess.run(["cp", "-r", template_folder, master_wallet_folder])
    subprocess.run(["cp", env_file_path, master_wallet_folder])

    # Install dependencies and create the master wallet
    commands = f"""
    cd '{master_wallet_folder}' &&
    npm install &&
    npm update &&
    node . wallet new > wallet_info.txt
    """
    run_command_in_terminal(commands, master_wallet_folder)
    
    # Wait for the .wallet.json file to be created and populated with valid JSON
    wallet_json_path = os.path.join(master_wallet_folder, ".wallet.json")
    while not os.path.exists(wallet_json_path) or os.path.getsize(wallet_json_path) == 0:
        print(f"Waiting for {wallet_json_path} to be created and populated...")
        time.sleep(5)
    print(f"{wallet_json_path} has been created.")

    # Read the master wallet info from .wallet.json
    while True:
        try:
            with open(wallet_json_path, "r") as wallet_json_file:
                wallet_info = json.load(wallet_json_file)
            break
        except json.JSONDecodeError:
            print("Waiting for valid JSON content in the .wallet.json file...")
            time.sleep(5)

    privkey = wallet_info["privkey"]
    address = wallet_info["address"]

    # Save the master wallet info to master_wallet.txt
    with open(master_wallet_info_path, "w") as master_wallet_file:
        master_wallet_file.write(f"Label: master_wallet\n")
        master_wallet_file.write(f"Private Key: {privkey}\n")
        master_wallet_file.write(f"Address: {address}\n\n")

    # Import the master wallet's private key into the node
    import_commands = f"""
    cd ~/dogecoin-1.14.7/bin/ &&
    ./dogecoin-cli importprivkey "{privkey}" "master_wallet" false &&
    cd '{master_wallet_folder}' &&
    exec bash
    """
    run_command_in_terminal(import_commands, master_wallet_folder)
    
    # Prompt the user to send Dogecoin to the master wallet
    print(f"Send your Doge to the master wallet address: {address}")
    input("Once sent, press Enter to continue...")
    
    # Sync the master wallet and check for a positive balance
    while True:
        sync_commands = f"node . wallet sync"
        result = subprocess.run(sync_commands, cwd=master_wallet_folder, shell=True, capture_output=True, text=True)
        if "positive balance" in result.stdout.lower():  # Adjust this condition based on actual output
            print(f"Balance received: {result.stdout}")
            break
        else:
            print("Balance not received yet. Please wait and try again.")
            time.sleep(10)

    # Prompt the user to split the balance
    input("Press Enter to split the balance among all wallets...")
    
    # Read wallet info from wallet_info.txt
    with open(main_wallet_info_path, "r") as main_wallet_file:
        lines = main_wallet_file.readlines()
    
    # Extract addresses from the wallet info
    addresses = [line.split(": ")[1].strip() for line in lines if line.startswith("Address")]
    
    # Calculate the amount to send to each wallet
    balance = float(result.stdout.split("balance: ")[1].strip())  # Adjust this parsing based on actual output
    amount_per_wallet = balance / len(addresses)
    
    # Send Doge to each wallet
    for address in addresses:
        send_commands = f"""
        cd ~/dogecoin-1.14.7/bin/ &&
        ./dogecoin-cli sendtoaddress "{address}" {amount_per_wallet} &&
        cd '{master_wallet_folder}' &&
        exec bash
        """
        run_command_in_terminal(send_commands, master_wallet_folder)
        time.sleep(5)  # Add a short delay between transactions
    
    print("Doge sent to all wallets.")
    
    # Sync all wallets and verify the balance distribution
    for folder in os.listdir(os.path.join(main_directory, "cloned minters")):
        folder_path = os.path.join(main_directory, "cloned minters", folder)
        sync_commands = f"node . wallet sync"
        run_command_in_terminal(sync_commands, folder_path)
        time.sleep(5)  # Add a short delay between syncs
    
    print("Doge split equally between wallets.")

# Run the function
if __name__ == "__main__":
    create_master_wallet()
