import os
import subprocess
import time
import json

def install_dependencies_and_create_wallets():
    # Define the paths
    main_directory = os.path.expanduser("~/Desktop/mass minter")
    cloned_minters_directory = os.path.join(main_directory, "cloned minters")
    
    # Get the list of all cloned minter directories, sorted in ascending order
    cloned_folders = sorted([os.path.join(cloned_minters_directory, d) for d in os.listdir(cloned_minters_directory) if os.path.isdir(os.path.join(cloned_minters_directory, d))])
    
    # Initialize a list to hold wallet info for later import
    wallet_info_list = []

    for index, folder in enumerate(cloned_folders):
        print(f"Processing {folder}")
        
        # Commands to run in each terminal
        commands = f"""
        cd '{folder}' &&
        npm install &&
        npm update &&
        node . wallet new > wallet_info.txt
        """
        
        # Use gnome-terminal to open a new terminal and run the commands
        subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"{commands}; exec bash"])
        
        # Add a 5-second delay between launching each terminal instance
        time.sleep(5)
    
    # Wait for all terminal processes to complete by monitoring the wallet_info.txt files
    for folder in cloned_folders:
        wallet_info_path = os.path.join(folder, "wallet_info.txt")
        while not os.path.exists(wallet_info_path):
            print(f"Waiting for {wallet_info_path} to be created...")
            time.sleep(5)
        print(f"{wallet_info_path} has been created.")
    
    # Collect the wallet info into a single file and prepare for import
    main_wallet_file_path = os.path.join(main_directory, "wallet_info.txt")
    with open(main_wallet_file_path, "w") as main_wallet_file:
        for index, folder in enumerate(cloned_folders):
            wallet_json_path = os.path.join(folder, ".wallet.json")
            if os.path.exists(wallet_json_path):
                with open(wallet_json_path, "r") as wallet_json_file:
                    wallet_info = json.load(wallet_json_file)
                    privkey = wallet_info["privkey"]
                    address = wallet_info["address"]
                    
                    # Append the privkey and address to the main wallet info file
                    main_wallet_file.write(f"Folder: {folder}\n")
                    main_wallet_file.write(f"Private Key: {privkey}\n")
                    main_wallet_file.write(f"Address: {address}\n\n")
                    
                    # Store the wallet info for later import
                    wallet_info_list.append((privkey, f"minter_{index + 1}", folder))
                
                print(f"Wallet information from {folder} saved to {main_wallet_file_path}")
            else:
                print(f"Wallet info file not found in {folder}")

    # Automate the import of private keys into the node in each terminal
    for privkey, label, folder in wallet_info_list:
        import_commands = f"""
        cd ~/dogecoin-1.14.7/bin/ &&
        ./dogecoin-cli importprivkey "{privkey}" "{label}" false &&
        cd '{folder}' &&
        exec bash
        """
        subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"{import_commands}"])
        
        # Add a 5-second delay between launching each terminal instance
        time.sleep(5)

    print("All wallets created, saved, and imported successfully.")

# Run the installation and wallet creation function
if __name__ == "__main__":
    install_dependencies_and_create_wallets()
